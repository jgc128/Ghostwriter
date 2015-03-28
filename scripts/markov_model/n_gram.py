from collections import defaultdict

class NGramModel( object ):
    """pass in processed, tokenized lyrics including startVerse, endLine, endVerse tokens"""
    def __init__( self , lyrics ):
        self.n = 3
        self.nGramCount = defaultdict(lambda:defaultdict(lambda:0))
        self.nGramBackoffCount = defaultdict(lambda:defaultdict(lambda:0))
        self.highestCount = defaultdict(lambda:None)
        self.highestBackoffCount = defaultdict(lambda:None)
        tokenCount = len(lyrics)
        nGrams = []
        while i < tokenCount - 2:
            nGrams.append(lyrics[i:i+3])
        for ng in nGrams:
            self.nGramCount[ng[:-1]][ng[-1]] += 1
            self.nGramBackoffCount[ng[:-2]][ng[-1]] += 1
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

    def genNextToken( self , history ):
        if len(history) != self.n-1 and history != ['<startVerse>']:
            """make wrong history error"""
        else:
            if self.highestCount[history] != None:
                return self.highestCount[history]
            else:
                return self.highestBackoffCount[history[:-1]]
            
                                                                        
            
        
