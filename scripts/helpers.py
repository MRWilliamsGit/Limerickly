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