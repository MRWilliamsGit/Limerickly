import requests
import datamuse as dm

from transformers import RobertaTokenizer, RobertaForMaskedLM
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
        
        if tokenizer == None:
            self.tokenizer = RobertaTokenizer.from_pretrained('roberta-base')

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
            #print(idea)

        return l
    
    # params: how many ideas to return
    # returns: list of possible line pairs
    def get_sentences(self, num):

        sen = self.prep_sentences(num)
        sendone = []
        
        for s in sen:
            token_ids = self.tokenizer.encode(text=s, return_tensors='pt')
            masked_position = (token_ids.squeeze() == self.tokenizer.mask_token_id).nonzero()
            masked_pos = [mask.item() for mask in masked_position ]

            with torch.no_grad():
                output = self.model(token_ids)

            last_hidden_state = output[0].squeeze()

            list_of_list =[]
            for index,mask_index in enumerate(masked_pos):
                mask_hidden_state = last_hidden_state[mask_index]
                idx = torch.topk(mask_hidden_state, k=5, dim=0)[1]
                words = [self.tokenizer.decode(i.item()).strip() for i in idx]
                list_of_list.append(words)
                #print ("Mask ",index+1,"Guesses : ",words)
            
            best_guess = ""
            for j in list_of_list:
                best_guess = best_guess+" "+j[0]
            
            print(best_guess + " "+ s.split()[-1])
            #sendone.append[best_guess]

        #print(sendone)

