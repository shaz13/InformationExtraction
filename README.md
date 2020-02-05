# Information Extraction Utils 

An open-source utils for extracting information from PDF word documents 


### Predicting NLP Entities

1. The utility allows you to extract information from AllenNLP models hosted at https://demo.allennlp.org/semantic-role-labeling
2. Prediction can be performed by `universal_allen_extractor.py` module in scripts folder
3. Refer `python universal_allen_extractor.py --help` for arguments to pass

````
usage: universal_allen_extractor.py [-h] [-m MODEL_PATH] [-html HTML_PATH]
                                    [-o OUTPATH]

Runs Information extracton from AllenNLP Models

optional arguments:
  -h, --help            show this help message and exit
  -m MODEL_PATH, --model_path MODEL_PATH
                        the path to the model/url
  -html HTML_PATH, --html_path HTML_PATH
                        the path to html format
  -o OUTPATH, --outpath OUTPATH
                        the outpath
````


> Note that this repository contains only **utils** and scripts. For more information contact me at shazbyte@gmail.com