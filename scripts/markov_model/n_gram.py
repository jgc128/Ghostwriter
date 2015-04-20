from collections import defaultdict
from random import choice

class NGramModel( object ):
    """pass in processed, tokenized lyrics including startVerse, endLine, endVerse tokens"""
    def __init__( self , lyrics , n=3):
        self.n = n
        self.startList = []
        self.nGramDict = defaultdict(lambda:[])
        self.nGramList = []#defaultdict(lambda:[])
        for j in range(self.n-2):
            self.startList.append([])
            for m in range(j+1):
                self.startList[-1].append(defaultdict(lambda:[]))
            #self.nGramBackoffList.append(defaultdict(lambda:[]))
            #self.startList.append(defaultdict(lambda:[]))
        for a in range(self.n-1):
            self.nGramList.append(defaultdict(lambda:[]))
        tokenCount = len(lyrics)
        nGrams = []
        #i = 0
        for i in range(tokenCount - self.n + 1):
        #while i < tokenCount - self.n + 1:
            nGrams.append(lyrics[i:i+self.n])
            #i += 1
                    
        for ng in nGrams:
            #if len(ng) > 2 and ng[:3] == ['<endLine', '<endVerse>', '<startVerse>']:
            #    continue
            #elif len(ng) >= 2 and ng[:2] == ['<startVerse>', '<endVerse>']:
            #    continue
            #self.nGramDict[str(ng[:-1])].append(ng[-1])
            if '<startVerse>' in ng and ng[0] != '<startVerse>':
                continue
            if '<endVerse>' in ng and ng[-1] != '<endVerse>':
                continue
            for k in range(self.n-1):
                self.nGramList[k][str(ng[:k+1])].append(ng[-1])
                
            #self.nGramBackoffList[str(ng[:-2])].append(ng[-1])
            
            if ng[0] == '<startVerse>':
                for k in range(self.n-2):
                    currentGram = ng[:k+1]
                    for l in range(k+1):
                        self.startList[k][l][str(currentGram[:l+1])].append(ng[k+1])
                             

    def genNextToken( self , history ):
        #print history
        lenHistory = len(history)
        if lenHistory < self.n-1 and history[0] != '<startVerse>':
            raise ValueError('Input history needs to be length '+str(self.n-1))
        elif history[0] == '<startVerse>' and lenHistory < self.n-1:
            for z in range(lenHistory):
                if self.startList[lenHistory-1][lenHistory-z-1][str(history[:lenHistory-z])] != []:
                    return choice(self.startList[lenHistory-1][lenHistory-z-1][str(history[:lenHistory-z])])
                      
        else:
        
            for l in range(self.n-1):
                if self.nGramList[lenHistory-l-1][str(history[:lenHistory-l])] != []:
                    return choice(self.nGramList[lenHistory-l-1][str(history[:lenHistory-l])])
            
                                                                        
            
        
