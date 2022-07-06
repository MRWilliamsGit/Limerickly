#this version did one mask at a time alternating first and last

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
        
        #call API for rhymes
        api = dm.Datamuse()
        rhymes = api.words(rel_rhy=word, max=many)

        #get just the rhymes as a list
        r = []
        for i in rhymes:
            r.append(i['word'])
        
        #return rhymes
        return r
    
    # quick thing to just add line to the limerick in self
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

        #number of options to grab
        x = 5

        #tokenize and get result
        this_t = self.tokenizer(text=this, return_tensors='pt')
        with torch.no_grad():
            output = self.model(**this_t).logits

        #convert predicted tokens to a list of top x predicted entries
        mask_token_index = (this_t.input_ids == self.tokenizer.mask_token_id)[0].nonzero(as_tuple=True)[0]
        hmmm = output[0, mask_token_index]
        predicted_token_ids = hmmm.topk(x,axis=-1)[1].squeeze(1)
        predicted_token_ids = predicted_token_ids.squeeze(1)[0]

        #decode and examine each
        #pick the first entry that is not a punctuation mark
        done = ''
        for p in predicted_token_ids:
            result = self.tokenizer.decode(p)
            if len(set.intersection(set(result), set(string.punctuation)))==0:
                done = result
                break

        return(done)

    
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
                #if there is only one left, just do the whole line
                if s.count("<mask>")<2:
                    new = self.get_prediction(s)
                    done = s.split("<mask>")[0] + new + s.split("<mask>")[-1]
                    s = done
                    print(done)
                #if there are more, do the first and last mask
                else:
                    #replace first mask with prediction
                    this = s.split("<mask>")[0] + "<mask>"
                    print(this)
                    new = self.get_prediction(this)
                    s = s.replace("<mask>", new, 1)
                    print(s)
                    #replace last mask with prediction
                    this = "<mask>" + s.split("<mask>")[-1]
                    print(this)
                    new = self.get_prediction(this)
                    s = s.replace(this, new + s.split("<mask>")[-1])
                    print(s)


