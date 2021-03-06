from transformers import RobertaForMaskedLM, RobertaTokenizer
import torch
import string
import requests


class limerickly():

    def __init__(self,
        model=None,
        tokenizer=None,
        limerick=None,
        rk=None
    ):
        if rk == None:
            self.rk=5

        if model == None:
            self.model = RobertaForMaskedLM.from_pretrained('roberta-base')
        
        if tokenizer == None:
            self.tokenizer = RobertaTokenizer.from_pretrained('roberta-base')

        if limerick == None:
            self.limerick =[]
    
    # params: word and how many rhymes to return,
    # returns: rhymes as list
    def get_rhymes(self, word, many):

        out = requests.get(
            "https://api.datamuse.com/words", params={"rel_rhy": word}
        ).json()
        words = [_["word"] for _ in out]

        return words[:many]
    
    # quick thing to just add line to the limerick in self
    def add_line(self,line):
        self.limerick.append(line)

    # params: how many ideas to return
    # returns: list of possible line pairs with mask placeholders for missing words
    def prep_sentences(self, num):

        #get what line we are on
        lines = len(self.limerick)

        #different scheme for if on last line
        if lines != 4:
            #get the latest line
            line = self.limerick[lines-1]
        else:
            #get the third latest line
            line = self.limerick[lines-3]

        #get the lenth of the line
        lenline = len(line.split())
        #get last word
        line = line.strip(string.punctuation)
        last = line.split()[-1]

        print(last)
        #get rhymes for latest word
        rhymes = self.get_rhymes(last, num)

        #put together a set of new lines with mask placeholders
        l=[]
        ideas = "<mask> " * (lenline-1)
        for r in rhymes:
            idea = self.limerick[lines-1] +" "+ideas + r
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
            print(result)
            if len(set.intersection(set(result), set(string.punctuation)))==0:
                done = result
                break

        return(done)

    # params: the line with multiple <mask>
    # returns: the line with the first and last mask replaced
    def get_prediction_multiple(self,this):
        #markers for error catching
        ffound = False

        #tokenize
        token_ids = self.tokenizer.encode(text=this, return_tensors='pt')
        masked_position = (token_ids.squeeze() == self.tokenizer.mask_token_id).nonzero()
        masked_pos = [mask.item() for mask in masked_position ]

        #get predictions
        with torch.no_grad():
            output = self.model(token_ids)
        last_hidden_state = output[0].squeeze()

        #pull out top predicted words
        list_of_list =[]
        for index,mask_index in enumerate(masked_pos):
            mask_hidden_state = last_hidden_state[mask_index]
            idx = torch.topk(mask_hidden_state, k=self.rk, dim=0)[1]
            words = [self.tokenizer.decode(i.item()).strip() for i in idx]
            list_of_list.append(words)

        #replace first mask with the first predicted word (not punctuation or too long)
        for w in list_of_list[0]:
            if len(set.intersection(set(w), set(string.punctuation)))==0 & len(w) < 10:
                new = this.replace("<mask>", w, 1)
                ffound = True
                break
        
        #if acceptable word was not found, increase number of predictions and break out of function
        #since this function is called inside a loop, it will re-run with a larger pool of predictions
        if ffound == False:
            self.rk=self.rk+5
            return(this)

        #replace last mask with last predicted word (not punctuation or too long)
        #note that if no acceptable word is found, it will be run from the top and caught by ffound
        new = new[::-1]
        for w in list_of_list[-1]:
            if len(set.intersection(set(w), set(string.punctuation)))==0 & len(w) < 10:
                w = w[::-1]
                new = new.replace(">ksam<", w, 1)
                break
        new = new[::-1]

        #return line
        return(new)
    
    # params: how many ideas to return
    # returns: list of possible line pairs
    def get_sentences(self, num):

        #get list of masked lines (different rhyme each)
        sen = self.prep_sentences(num)
        
        #for each line
        for s in sen:
            #predict the words a bit at a time from until there are no masks left
            while s.count("<mask>")>0:
                #if there is only one left, just do the whole line
                if s.count("<mask>")<2:
                    new = self.get_prediction(s)
                    done = s.split("<mask>")[0] + new + s.split("<mask>")[-1]
                    s = done
                #if there are more, do the first and last mask
                else:
                    #replace first mask with prediction
                    this = s.split("<mask>")[0] + "<mask>"
                    new = self.get_prediction(this)
                    s = s.replace("<mask>", new, 1)
                    #replace last mask with prediction
                    this = "<mask>" + s.split("<mask>")[-1]
                    new = self.get_prediction(this)
                    s = s.replace(this, new + s.split("<mask>")[-1])

    #params: how many rhymes to get
    #returns: list of choices for second line
    def get_sentences2(self, num):

        #get list of masked lines (different rhyme each)
        sen = self.prep_sentences(num)
        
        #initialize list of choices, first line is blank to indicate not chosen in app
        choices = [" "]

        #for each line
        for s in sen:
            #predict the first and last mask until there are no masks left
            while s.count("<mask>")>0:
                s = self.get_prediction_multiple(s)
            
            #add the second line to the list of options
            s = s.replace(self.limerick[len(self.limerick)-1], '')
            choices.append(s)
        
        #return options
        return(choices)

