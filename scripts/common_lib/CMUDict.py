from collections import defaultdict
import re

class CMUDict( object ):
    def __init__(self):
        self._data = defaultdict(lambda:None)

        for line in open('/data1/nlp-data/cmu-pronounce-dict/cmudict-0.7b', 'r'):
            lineSplit = line.strip('\n').split(' ')
            if re.match(r'[A-Z]', line[0]) != None and lineSplit[0][-1] != ')':
                self._data[lineSplit[0].lower()] = lineSplit[2:]

    def get_cmu_pho(self, word):
        return self._data[word]
            
