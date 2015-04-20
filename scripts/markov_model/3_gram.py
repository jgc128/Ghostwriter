from collections import defaultdict
from random import choice

class NGramModel( object ):
    """pass in processed, tokenized lyrics including startVerse, endLine, endVerse tokens"""
    def __init__( self , lyrics ):
        self.n = 3
        self.startList = []
        self.nGramList = defaultdict(lambda:[])
        self.nGramBackoffList = defaultdict(lambda:[])
        self.nGramCount = defaultdict(lambda:defaultdict(lambda:0))
        self.nGramBackoffCount = defaultdict(lambda:defaultdict(lambda:0))
        self.highestCount = defaultdict(lambda:None)
        self.highestBackoffCount = defaultdict(lambda:None)
        tokenCount = len(lyrics)
        nGrams = []
        i = 0
        while i < tokenCount - 2:
            nGrams.append(lyrics[i:i+3])
            i += 1

        """
        for ng in nGrams:
            self.nGramCount[str(ng[:-1])][str(ng[-1])] += 1
            self.nGramBackoffCount[str(ng[:-2])][str(ng[-1])] += 1
            if ng[0] == '<startVerse>' and ng[1] != '<endVerse>':
                self.startList.append(ng[1])
        self.highestStart = Counter(self.startList).most_common(1)[0][0]
        for ngKey in self.nGramCount.keys():
            ngMax = 0
            for token in self.nGramCount[ngKey].keys():
                if self.nGramCount[ngKey][token] > ngMax:
                    self.highestCount[ngKey] = token
                    ngMax = self.nGramCount[ngKey][token]
        for ngKey in self.nGramBackoffCount.keys():
            ngMax = 0
            for token in self.nGramBackoffCount[ngKey].keys():
                if self.nGramBackoffCount[ngKey][token] > ngMax:
                    self.highestBackoffCount[ngKey] = token
                    ngMax = self.nGramBackoffCount[ngKey][token]
        """
                    
        for ng in nGrams:
            if ng == ['<endLine>', '<endVerse>', '<startVerse>']:
                continue
            self.nGramList[str(ng[:-1])].append(ng[-1])
            self.nGramBackoffList[str(ng[:-2])].append(ng[-1])
            if ng[0] == '<startVerse>' and ng[1] != '<endVerse>':
                self.startList.append(ng[1])
                                

    def genNextToken( self , history ):
        if len(history) != self.n-1 and history != ['<startVerse>']:
            raise ValueError('Input history needs to be length '+str(self.n-1))
        elif history == ['<startVerse>']:
            return choice(self.startList)
        else:
            if self.nGramList[str(history)] != []:
                return choice(self.nGramList[str(history)])
            else:
                return choice(self.nGramBackoffList[str(history[:-1])])
            
                                                                        
            
        
