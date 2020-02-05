import re
import os
import sys
import argparse
import json

import pandas as pd
import numpy as np
from allennlp.predictors.predictor import Predictor
from tqdm import tqdm, notebook
from bs4 import BeautifulSoup

def cleanData(text):
    txt = str(text)
    txt = re.sub(r'[^A-Za-z0-9\s]',r'',txt)
    txt = re.sub(r'\n',r' ',txt)
    return txt

def capital_words_spaces(str1):
    return re.sub(r"(\w)([A-Z])", r"\1 \2", str1)


if __name__ == "__main__": 
    my_parser = argparse.ArgumentParser(description='Runs information extracton from AllenNLP models')
    # Add the arguments
    my_parser.add_argument('-m', '--model_path',
                        type=str,
                        default="https://s3-us-west-2.amazonaws.com/allennlp/models/bert-base-srl-2019.06.17.tar.gz",
                        help='the path to the model/URL')
    
    my_parser.add_argument('-html', '--html_path',
                        type=str,
                        help='path to html parsed PDF')
    my_parser.add_argument('-o', '--outpath',
                    type=str,
                    default='./predictions.json',
                    help='output path')   
                                        
    # Execute the parse_args() method
    args = my_parser.parse_args()

    MODEL_PATH = args.model_path
    HTML_PATH = args.html_path
    OUTPUT_PATH = args.outpath

    with open(HTML_PATH, encoding='utf-8') as f:
        content = f.read()
        
    soup = BeautifulSoup(content, 'lxml')
    predictor = Predictor.from_path(MODEL_PATH)

    # Structurizing raw HTML to actionable fields
    print(">> Structuzing raw HTML to dictionary object")
    extracted_info = []
    para_collect = []
    for word in tqdm(soup.findAll('div')):
        if len(word.text) != 0:
            para_collect.append(word.text)
        if 'Page ' in (word.text):
            text =  ' '.join(para_collect[:-1])
            text = re.sub(r" \n ", " ", text)
            page_no = word.text.split(" ")[1]
            if len(text) == 0:
                continue
            tf_dict = {}
            tf_dict['page_no'] = int(page_no)
            tf_dict['infos'] = {}
            tf_dict['props'] = {}
            
            tf_dict['infos']['para'] = text.split("\n ")
            
            sentences = ' '.join(para_collect[:-1])
            sentences = sentences.replace("\n","")
            sentences = sentences.split(". ")
            
            tf_dict['infos']['sentences'] = sentences
            tf_dict['infos']['text'] = text
            tf_dict['props']['total_paras'] = len(text.split("\n "))
            tf_dict['props']['total_chars'] = len(' '.join(para_collect[:-1]))
            tf_dict['props']['total_sentences'] = len(para_collect[:-1])
            extracted_info.append(tf_dict)
            para_collect = []

    # Saving extracted information
    print(">> Exporting dictionary object")
    with open(HTML_PATH.replace(".html",'.json'), 'w') as f:
        json.dump(extracted_info, f)

    # Predicting Entites
    print(">> Extracting information ...")
    predictions_info = []
    for instance in tqdm(extracted_info):
        sentences = instance['infos']['sentences']
        for sent in (sentences): 
            if len(sent) > 10:
                try:
                    predictions = predictor.predict(sentence=sent)   
                    predictions_info.append(predictions)
                except:
                    print(f">> Failed for {sent}")

    print(">> Saving output as JSON Object")
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(predictions_info, f)
    print(">> Done. Completed")
