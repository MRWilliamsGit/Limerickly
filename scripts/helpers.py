import requests
import datamuse as dm

from transformers import TFBertForPreTraining
from transformers import BertTokenizer
import tensorflow as tf

#returns rhymes from datamuse API, which pulls from RhymeZone
def get_rhyme(word, many):

    #load API
    api = dm.Datamuse()

    #call for rhymes
    rhymes = api.words(rel_rhy=word, max=many)

    #get just the rhymes as a list
    l = []
    for r in rhymes:
        l.append(r['word'])
        #print(r['word'])
    
    #return list
    return l

#initializes the model
def get_model():

    print("Downloading Model...")
    model = TFBertForPreTraining.from_pretrained("sshleifer/distilbart-cnn-12-6")
    tokenizer = BertTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
    print("Download Complete")

    return model, tokenizer
