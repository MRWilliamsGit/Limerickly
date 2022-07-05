#working to return sets of words but the words are not sentences

import requests
import datamuse as dm

#from transformers import TFBertForMaskedLM, BertTokenizer
from transformers import RobertaForMaskedLM, RobertaTokenizer
#import tensorflow as tf
import torch
import string

class limerickly():

    def __init__(self,
        model=None,
        tokenizer=None,
        limerick=None
    ):
  
        if model == None:
            self.model = RobertaForMaskedLM.from_pretrained('roberta-base')
            #self.model = TFBertForMaskedLM.from_pretrained("bert-large-cased-whole-word-masking")
        
        if tokenizer == None:
            self.tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
            #self.tokenizer = BertTokenizer.from_pretrained("bert-large-cased-whole-word-masking")

        if limerick == None:
            self.limerick =[]
    
    # params: word and how many rhymes to return,
    # returns: rhymes as list
    def get_rhymes(self, word, many):
        
        #load API
        api = dm.Datamuse()

        #call for rhymes
        rhymes = api.words(rel_rhy=word, max=many)

        #get just the rhymes as a list
        r = []
        for i in rhymes:
            r.append(i['word'])
        
        #return rhymes
        return r
    
    # params: new line of limerick
    def add_line(self,line):
        self.limerick.append(line)

    # params: how many ideas to return
    # returns: list of possible line pairs with mask placeholders for missing words
    def prep_sentences(self, num):

        #get what line we are on
        lines = len(self.limerick)
        #get the latest line
        line = self.limerick[lines-1]
        #get the lenth of the latest line
        lenline = len(line.split())
        #get last word
        last = line.split()[-1]
        last = last.replace(string.punctuation, '')

        #get rhymes for latest word
        rhymes = self.get_rhymes(last, num)

        #put together a set of new lines with mask placeholders
        l=[]
        ideas = "<mask> " * (lenline-1)
        for r in rhymes:
            idea = line +", "+ideas + r
            l.append(idea)
    
        return l

    # params: the line with a <mask> that indicates the word to predict
    # returns: the predicted word
    def get_prediction(self,this):

        this_t = self.tokenizer(text=this, return_tensors='pt')
        with torch.no_grad():
            output = self.model(**this_t).logits

        mask_token_index = (this_t.input_ids == self.tokenizer.mask_token_id)[0].nonzero(as_tuple=True)[0]
        #predicted_token_id = output[0, mask_token_index].argmax(axis=-1)
        hmmm = output[0, mask_token_index]
        #predicted_token_id = hmmm.argmax(axis=-1)
        #print(predicted_token_id)
        #print(hmmm.topk(1,axis=-1)[1].squeeze(1))
        predicted_token_id = hmmm.topk(1,axis=-1)[1].squeeze(1)
        #print(predicted_token_id)
        result = self.tokenizer.decode(predicted_token_id)

        return(result)

    
    # params: how many ideas to return
    # returns: list of possible line pairs
    def get_sentences(self, num):

        #get list of masked lines (different rhyme each)
        sen = self.prep_sentences(num)
        sendone = []
        
        #for each line
        for s in sen:
            #predict the words a bit at a time from until there are no masks left
            while s.count("<mask>")>0:
                #if there are only one or two masked words, just do the whole line
                if s.count("<mask>")<3:
                    new = self.get_prediction(s)
                    done = s.partition("<mask>")[0] + new + " " + s.split()[-1]
                    s = done
                    print(done)
                #if there are more, do the first mask
                else:
                    #replace first mask with prediction
                    this = s.partition("<mask>")[0] + "<mask>"
                    new = self.get_prediction(this)
                    s = s.replace("<mask>", new, 1)
                    print(s)

