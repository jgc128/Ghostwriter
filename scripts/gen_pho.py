#import sys


class GenPho( object ):
    def __init__(self, CMUDict):
        self.myDict = CMUDict
        self.vowel = frozenset(['a','e','i','o','u','y'])
        self.consonant = frozenset(['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','z'])
        self.voiced = frozenset(['b','d','v','g','j','l','m','n','r','w','z'])
        self.front = frozenset(['e','i','y'])
        self.suffix = frozenset(['er','e','es','ed','ing','ely'])
        self.sibilant = frozenset(['s','c','g','z','x','j','ch','sh'])
        self.nonpal = frozenset(['t','s','r','d','l','z','n','j','th','ch','sh'])

    def get_pho( self , word ):
        cmu = self.myDict[word]
        if cmu != None:
            return cmu
        else:
            return self.get_oov_pho( '' , word , [] )

    def get_oov_pho(self, before, after, phoList):
        #phoList = []
        if after == '':
            return phoList
        
        elif after[0] == 'a':
            if len(after) == 1:
                phoList.append('AX')
                return phoList
            elif len(before) == 0 and len(after) >= 3 and after[1:3] == 'ro':
                phoList += ['AX','R']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 3 and after[1] == 'r' and self.pound(after[2]):
                phoList += ['EH','R']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(before) == 1 and len(after) >= 3 and self.star(before[0]) and after[1] == 's' and self.pound(after[2]):
                phoList += ['EY', 'S']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 3 and after[1:3] == 'wa':
                phoList.append('AX')
                return self.get_oov_pho(last+after[:1], after[1:], phoList)
            elif len(after) >= 2 and after[1] == 'w':
                phoList.append('AO')
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 3 and after[1:3] = 'NY' and set(before).intersection(self.vowel) == set([]):
                phoList += ['EH', 'N', 'IY']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(after) >= 4 and self.star(after[1]) and self.plus(after[2]) and self.pound(after[3]):
                phoList.append('EY')
                return self.get_oov_pho(last+after[:1], after[1:], phoList)
            elif len(before) >= 1 and set(before).intersection(self.vowel) != set([]) and len(after) >= 4 and after[1:4] == 'lly':
                phoList += ['AX', 'L', 'IY']
                return self.get_oov_pho(last+after[:4], after[4:], phoList)
            elif len(before) == 0 and len(after) >= 3 and after[1] == 'l' and self.pound(after[2]):
                phoList += ['AX', 'L']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 5 and after[1:5] == 'gain':
                phoList += ['AX', 'G', 'EH', 'N']
                return self.get_oov_pho(last+after[:5], after[5:], phoList)
            elif len(before) >= 1 and len(after) >= 3 and set(before).intersection(self.vowel) != set([]) and after[1] == 'g' and after[2] == 'e':
                phoList += ['IH', 'JH']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 4 and self.star(after[1]) and self.plus(after[2]) and set(after[3:]).intersection(self.vowel) != set([]):
                phoList.append('AE')
                return return self.get_oov_pho(last+after[:1], after[1:], phoList)
            elif len(after) == 3 and set(before).intersection(self.vowel) == set([]) and self.star(after[1]) and self.plus(after[2]):
                phoList.append('EY')
                return self.get_oov_pho(last+after[:1], after[1:], phoList)
            elif len(after) >= 3 and self.star(after[1]) and self.percent(after[2:]):
                phoList.append('EY')
                return self.get_oov_pho(last+after[:1], after[1:], phoList)
            elif len(before) == 0 and len(after) >= 3 and after[1:3] == 'rr':
                phoList += ['AX', 'R']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(after) >= 3 and after[1:3] =='rr':
                phoList += ['AE', 'R']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif set(before).intersection(self.vowel) == set([]) and len(after) == 2 and after[1] == 'r':
                phoList += ['AA', 'R']
                return phoList
            elif len(after) == 2 and after[1] == 'r':
                phoList.append('ER')
                return phoList
            elif len(after) >= 2 and after[1] == 'r':
                phoList += ['AA', 'R']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 3 and after[1:3] == 'ir':
                phoList += ['EH', 'R']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(after) >= 2 and after[1] == 'i':
                phoList.append('EY')
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 2 and after[1] == 'y':
                phoList.append('EY')
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 2 and after[1] == 'u':
                phoList.append('AO')
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) == 2 and set(before).intersection(self.vowel) != set([]) and after[1] == 'l':
                phoList += ['AX', 'L']
                return phoList
            elif len(after) == 3 and set(before).intersection(self.vowel) != set([]) and after[1:] == 'ls':
                phoList += ['AX', 'L', 'Z']
                return phoList
            elif len(after) >= 3 and after[1:3] == 'lk':
                phoList += ['AO', 'K']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(after) >= 3 and after[1] == 'l' and self.star(after[2]):
                phoList += ['AO', 'L']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif set(before).intersection(self.vowel) == set([]) and len(after) >= 4 and after[1:4] == 'ble':
                phoList += ['EY', 'B', 'AX', 'L']
                return self.get_oov_pho(last+after[:4], after[4:], phoList)
            elif len(after)>= 4 and after[1:4] == 'ble':
                phoList += ['AX', 'B', 'AX', 'L']
                return self.get_oov_pho(last+after[:4], after[4:], phoList)
            elif len(after) >= 4 and after[1:3] == 'ng' and self.plus(after[3]):
                phoList += ['EY', 'N', 'JH']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            else:
                phoList.append('AE')
                return self.get_oov_pho(last+after[:1], after[1:], phoList)
                
        elif after[0] == 'b':
            if len(before) == 0 and len(after) >= 4 and after[1] == 'e' and self.star(after[2]) and self.pound(after[3]):
                phoList += ['B', 'IH']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 5 and after[1:5] == 'eing':
                phoList += ['B', 'IY', 'IH', 'NX']
                return self.get_oov_pho(last+after[:5], after[5:], phoList)
            elif len(before) == 0 and len(after) >= 4 and after[1:3] == 'us' and self.pound(after[4]):
                phoList += ['B', 'IH', 'Z']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(after) >= 4 and after[1:4] == 'uil':
                phoList += ['B', 'IH', 'L']
                return self.get_oov_pho(last+after[:4], after[4:], phoList)
            else:
                phoList.append('B')
                return self.get_oov_pho(last+after[:1], after[1:], phoList)

        elif after[0] == 'c':
            if len(before) == 0 and len(after) >= 3 and after[1] == 'h' and self.star(after[2]):
                phoList.append('K')
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(before) >= 2 and len(after) >= 2 and self.star(before[-2]) and before[-1] == 'e' and after[1] == 'h':
                phoList.append('K')
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 2 and after[1] == 'h':
                phoList.append('CH')
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(before) == 1 and before[0] == 's' and len(after) >= 3 and after[1] == 'i' and self.pound(after[2]):
                phoList += ['S', 'AY']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif after >= 3 and after[1:3] == 'ia':
                phoList.append('SH')
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif after >= 3 andafter[1:3] == 'io':
                phoList.append('SH')
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif after >= 4 and after[1:4] == 'ien':
                phoList.append('SH')
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 2 and self.plus(after[1]):
                phoList.append('S')
                return self.get_oov_pho(last+after[:1], after[1:], phoList)
            elif len(after) >= 2 and after[1] == 'k':
                phoList.append('K')
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 4 and after[1:3] == 'om' and self.percent(after[3:]):
                phoList += ['K', 'AH', 'M']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            else:
                phoList.append('K')
                return self.get_oov_pho(last+after[:1], after[1:], phoList)

        elif after[0] == 'd':
            if set(before).intersection(self.vowel) != set([]) and len(after) == 3 and after[1:3] == 'ed':
                phoList += ['D', 'IH', 'D']
                return phoList
            elif len(before) >= 2 and before[-1] == 'e' and self.dot(before[-2]) and len(after) == 1:
                phoList.append('D')
                return phoList
            elif len(before) >= 3 and len(after) == 1 and before[-1] == 'e' and self.star(before[-2]) and set(before[:-2]).intersection(self.vowel) != set([]):
                phoList.append('T')
                return phoList
            elif len(before) == 0 and len(after) >= 4 and after[1] == 'e' and self.star(after[2]) and self.pound(after[3]):
                phoList += ['D', 'IH']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(before) == 0 and len(after) >= 4 and after[1:4] == 'oes':
                phoList += ['D', 'AH', 'Z']
                return self.get_oov_pho(last+after[:4], after[4:], phoList)
            elif len(before) == 0 and len(after) >= 5 and after[1:5] == 'oing':
                phoList += ['D', 'UW', 'IH', 'NX']
                return self.get_oov_pho(last+after[:5], after[5:], phoList)
            elif len(before) == 0 and len(after) >= 3 and after[1:3] =='ow':
                phoList += ['D', 'AW']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(after) >= 3 and after[1:3] == 'ua':
                phoList += ['JH', 'UW']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            else:
                phoList.append('D')
                return self.get_oov_pho(last+after[:1], after[1:], phoList)

        elif after[0] == 'e':
            if len(before) >= 1 and len(after) == 1 and set(before).intersection(self.vowel) != set([]):
                return phoList
            elif len(before) >= 1 and len(after) == 1 and self.star(before[-1]):
                return pholist
            elif set(before).intersection(self.vowel) == set([]) and len(after) == 1:
                return phoList.append('IY')
            elif len(before) >= 1 and len(after) == 2 and after[1] == 'd' and self.pound(before[-1]):
                return phoList.append('D')
            elif len(before) >= 1 and len(after) == 2 and set(before).intersection(self.vowel) != set([]) and after[1] == 'd':
                return self.get_oov_pho(last+after[:1], after[1:], phoList)
            elif len(after) >= 4 and after[1:4] == 'ver':
                phoList += ['EH', 'V']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 3 and self.star(after[1]) and self.percent(after[2:]):
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('IY'))
            elif len(after) >= 4 and after[1:3] == 'ri' and self.pound(after[3]):
                phoList += ['IY', 'R', 'IY']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(after) >= 3 and after[1:3] == 'ri':
                phoList += ['EH', 'R', 'IH']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(before) >= 1 and len(after) >= 3 and set(before).intersection(self.vowel) != set([]) and after[1] == 'r' and self.pound(after[2]):
                return self.get_oov_pho(last+after[:2], after[2:], phoList.append('ER'))
            elif len(after) >= 3 and after[1] == 'r' and self.pound(after[2]):
                phoList += ['EH', 'R']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 2 and after[1] == 2:
                return self.get_oov_pho(last+after[:2], after[2:], phoList.append('ER'))
            elif len(before) == 0 and len(after) >= 4 and after[1:4] == 'ven':
                phoList += ['IY', 'V', 'EH', 'N']
                return self.get_oov_pho(last+after[:4], after[4:], phoList)
            elif len(before) >= 1 and len(after) == 2 and set(before).intersection(self.vowel) != set([]) and after[1] == 'w':
                return self.get_oov_pho(last+after[:1], after[1:], phoList)
            elif len(before) >= 1 and len(after) >= 2 and self.at1(before[-1]) and after[1] == 'w':
                return self.get_oov_pho(last+after[:2], after[2:], phoList.append('UW'))
            elif len(before) >= 2 and len(after) >= 2 and self.at2(before[-2:]) and after[1] == 'w':
                return self.get_oov_pho(last+after[:2], after[2:], phoList.append('UW'))
            elif len(after) >= 2 and after[1] == 'w':
                phoList += ['Y', 'UW']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 2 and after[1] == 'o':
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('IY'))
            elif len(before) >= 2 and len(after) == 2 and self.amp1(before[-1]) and set(before[:-1]).intersection(self.vowel) != set([]) and after[1] == 's':
                phoList += ['IH', 'Z']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(before) >= 3 and len(after) == 2 and self.amp2(before[-2:]) and set(before[:-2]).intersection(self.vowel) != set([]) and after[1] == 's':
                phoList+= ['IH', 'Z']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(before) >= 1 and len(after) == 2 and set(before).intersection(self.vowel) != set([]) and after[1] == 's':
                return self.get_oov_pho(last+after[:1], after[1:], phoList)
            elif len(before) >= 1 and len(after) == 3 and set(before).intersection(self.vowel) != set([]) and after[1:3] == 'ly':
                phoList += ['L', 'IY']
                return phoList
            elif len(before) >= 1 and len(after) >= 5 and set(before).intersection(self.vowel) != set([]) and after[1:5] == 'ment':
                phoList += ['M', 'EH', 'N', 'T']
                return self.get_oov_pho(last+after[:5], after[5:], phoList)
            elif len(after) >= 4 and after[1:4] == 'ful':
                phoList += ['F', 'UH', 'L']
                return self.get_oov_pho(last+after[:4], after[4:], phoList)
            elif len(after) >= 2 and after[1] == 'e':
                return self.get_oov_pho(last+after[:2], after[2:], phoList.append('IY'))
            elif len(after) >= 4 and after[1:4] == 'arn':
                phoList += ['ER', 'N']
                return self.get_oov_pho(last+after[:4], after[4:], phoList)
            elif len(before) == 0 and len(after) >= 4 and after[1:3] == 'ar' and self.star(after[3]):
                return self.get_oov_pho(last+after[:3], after[3:], phoList.append('ER'))
            elif len(after) >= 3 and after[1:3] == 'ad':
                phoList += ['EH', 'D']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(before) >= 1 and len(after) == 2 and set(before).intersection(sel.vowel) != set([]) and after[1] == 'a':
                phoList += ['IY', 'AX']
                return phoList
            elif len(after) >= 4 and after[1:4] == 'asu':
                return self.get_oov_pho(last+after[:2], after[2:], phoList.append('EH'))
            elif len(after) >= 2 and after[1] == 'a':
                return self.get_oov_pho(last+after[:2], after[2:], phoList.append('IY'))
            elif len(after) >= 4 and after[1:4] == 'igh':
                return self.get_oov_pho(last+after[:4], after[4:], phoList.append('EY'))
            elif len(after) >= 2 and after[1] == 'i':
                return self.get_oov_pho(last+after[:2], after[2:], phoList.append('IY'))
            elif len(before) == 0 and len(after) >= 3 and after[1:3] == 'ye':
                return self.get_oov_pho(last+after[:3], after[3:], phoList.append('AY'))
            elif len(after) >= 2 and after[1] == 'y':
                return self.get_oov_pho(last+after[:2], after[2:], phoList.append('IY'))
            elif len(after) >= 2 and len(after) >= 2 and after[1] =='u':
                phoList += ['Y', 'UW']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            else:
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('EH'))

        elif after[0] == 'f':
            if len(after) >= 3 and after[1:3] == 'ul':
                phoList += ['F', 'UH', 'L']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            else:
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('F'))

        elif after[0] == 'g':
            if len(after) >= 3 and after[1:3] == 'iv':
                phoList += ['G', 'IH', 'V']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(before) == 0 and len(after) >= 3 and after[1] == 'i' and self.star(after[2]):
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('G'))
            elif len(after) >= 3 and after[1:3] == 'et':
                phoList += ['G', 'EH']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(before) >= 2 and len(after) >= 4 and before[-2:] == 'su' and after[1:4] == 'ges':
                phoList += ['G', 'JH', 'EH', 'S']
                return self.get_oov_pho(last+after[:4], after[4:], phoList)
            elif len(after) >= 2 and after[1] == 'g':
                return self.get_oov_pho(last+after[:2], after[2:], phoList.append('G'))
            elif len(before) >= 2 and self.pound(before[-1]) and set(before[:-1]).intersection(self.consonant) == set(['b']):
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('G'))
            elif len(after) >= 2 and self.plus(after[1]):
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('JH'))
            elif len(after) >= 5 and after[1:5] == 'reat':
                phoList += ['G', 'R', 'EY', 'T']
                return self.get_oov_pho(last+after[:5], after[5:], phoList)
            elif len(before) >= 1 and self.pound(before[-1]) and after[1] == 'h':
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            else:
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('G'))

        elif after[0] == 'h':
            if len(after) >= 3 and len(before) == 0 and after[1:3] == 'av':
                phoList += ['HH', 'AE', 'V']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(before) == 0 and len(after) >= 4 and after[1:4] == 'ere':
                phoList += ['HH', 'IY', 'R']
                return self.get_oov_pho(last+after[:4], after[4:], phoList)
            elif len(before) == 0 and len(after) >= 4 and after[1:4] == 'our':
                phoList += ['AW', 'ER']
                return self.get_oov_pho(last+after[:4], after[4:], phoList)
            elif len(after) >= 3 and after[1:3] == 'ow':
                phoList += ['HH', 'AW']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(after) >= 2 and self.pound(after[1]):
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('HH'))
            else:
                return self.get_oov_pho(last+after[:1], after[1:], phoList)

        elif after[0] == 'i':
            if len(before) == 0: and len(after) >= 2 and after[1] == 'n':
                phoList += ['IH', 'N']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 3 and after[1:3] == 'nd':
                phoList += ['AY', 'N']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 3 and after[1:3] == 'er':
                phoList += ['IY', 'ER']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(before) >= 2 and len(after) == 3 and before[-1] == 'r' and set(before[:-1]).intersection(self.vowel) != set([]) and after[1:3] == 'ed':
                phoList += ['IY', 'D']
                return phoList
            elif len(after) == 3 and after[1:3] == 'ed':
                phoList += ['AY', 'D']
                return phoList
            elif len(after) >= 3 and after[1:3] == 'en':
                phoList += ['IY', 'EH', 'N']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(after) >= 3 and after[1:3] == 'et':
                phoList += ['AY', 'EH']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 2 and set(before).intersection(self.vowel) == set([]) and self.percent(after[1:]):
                return phoList.append('AY')
            elif len(after) >= 2 and self.percent(after[1:]):
                return phoList.append('IY')
            elif len(after) >= 2 and after[1] == 'e':
                return self.get_oov_pho(last+after[:2], after[2:], phoList.append('IY'))
            elif len(after) >= 4 and self.star(after[1]) and self.plus(after[2]) and set(after[3:]).intersection(self.vowel) != set([]):
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('IH'))
            elif len(after) >= 3 and after[1] == 'r' and self.pound(after[2]):
                phoList += ['AY', 'R']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 3 and after[1] == 'z' and self.percent(after[2:]):
                phoList += ['AY', 'Z']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 3 and after[1] == 's' and self.percent(after[2:]):
                phoList+= ['AY', 'Z']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 3 and after[1] == 'd' and self.percent(after[2:]):
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('AY'))
            elif len(before) >= 2 and len(after) >= 3 and self.star(before[-1]) and self.plus(before[-2]) and self.star(after[1]) and self.plus(after[2]):
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('IH'))
            elif len(after) >= 3 and after[1] == 't' and self.percent(after[2:]):
                return self.get_oov_pho(last+after[:2], after[2:], phoList.append('AY'))
            elif len(before) >= 2 and len(after) >= 3 and self.star(before[-1]) and set(before[:-1]).intersection(self.vowel) != set([]) and self.star(after[1]) and self.plus(after[2]):
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('IH'))
            elif len(after) >= 3 and self.star(after[1]) and self.plus(after[2]):
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('AY'))
            elif len(after) >= 2 and after[1] == 'r':
                return self.get_oov_pho(last+after[:2], after[2:], phoList.append('ER'))
            elif len(after) >= 3 and after[1:3] == 'gh':
                return self.get_oov_pho(last+after[:3], after[3:], phoList.append('AY'))
            elif len(after) >= 3 and after[1:3] == 'ld':
                phoList += ['AY', 'L', 'D']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif and len(after) == 3 and after[1:3] == 'gn':
                phoList += ['AY', 'N']
                return phoList
            elif len(after) >= 4 and after[1:3] == 'gn' and self.star(after[3]):
                phoList += ['AY', 'N']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(after) >= 4 and after[1:3] == 'gn'and self.percent(after[3:]):
                phoList+= ['AY', 'N']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(after) >= 4 and after[1:4] == 'que':
                phoList += ['IY', 'K']
                return self.get_oov_pho(last+after[:4], after[4:], phoList)
            else:
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('IH'))

        elif after[0] == 'j':
            return self.get_oov_pho(last+after[:1], after[1:], phoList.append('JH'))

        elif after[0] == 'k':
            if len(before) == 0 and len(after) >= 2 and after[1] == 'n':
                return self.get_oov_pho(last+after[:1], after[1:], phoList)
            else:
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('K'))

        elif after[0] == 'l':
            if len(after) >= 4 and after[1:3] == 'oc' and self.pound(after[3]):
                phoList += ['L', 'OW']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(before) >= 1 and before[-1] == 'l':
                return self.get_oov_pho(last+after[:1], after[1:], phoList)
            elif len(before) >= 2 and len(after) >= 2 and self.star(before[-1]) and set(before[:-1]).intersection(self.vowel) != set([]) and self.percent(after[1:]):
                phoList += ['AX', 'L']
                return self.get_oov_pho(last+after[:1], after[1:], phoList)
            elif len(after) >= 4 and after[1:4] == 'ead':
                phoList += ['L', 'IY', 'D']
                return self.get_oov_pho(last+after[:4], after[4:], phoList)
            else:
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('L'))

        elif after[0] == 'm':
            if len(after) >= 3 and after[1:3] == 'ov':
                phoList += ['M', 'UW', 'V']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            else:
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('M'))

        elif after[0] == 'n':
            if len(before) >= 1 and len(after) >= 3 and before[-1] == 'e' and after[1] == 'g' and self.plus(after[2]):
                phoList += ['N', 'JH']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 3 and after[1:3] == 'gr':
                phoList += ['NX', 'G']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 3 and after[1] == 'g' and self.pound(after[2]):
                phoList += ['NX', 'G']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 4 and after[1:3] == 'gl' and self.percent(after[3:]):
                phoList += ['NX', 'G', 'AX', 'L']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(after) >= 2 and after[1] == 'G':
                return self.get_oov_pho(last+after[:2], after[2:], phoList.append('NX'))
            elif len(after) >= 2 and after[1] == 'k':
                phoList += ['NX', 'K']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            else:
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('N'))

        elif after[0] == 'o':
            if len(after) == 2 and after[1] == 'f':
                phoList += ['AX', 'V']
                return phoList
            elif len(after) >= 6 and after[1:6] == 'rough':
                phoList += ['ER', 'OW']
                return self.get_oov_pho(last+after[:6], after[6:], phoList)
            elif len(before) >= 1 and len(after) == 2 and set(before).intersection(self.vowel) != set([]) and after[1] == 'r':
                return phoList.append('ER')
            elif len(before) >= 1 and len(after) == 3 and set(before).intersection(self.vowel) != set([]) and after[1:3] == 'rs':
                phoList += ['ER', 'Z']
                return phoList
            elif len(after) >= 2 and after[1] == 'r':
                phoList += ['AO', 'R']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(before) == 0 and len(after) >= 3 and after[1:3] == 'ne':
                phoList += ['W', 'AH', 'N']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(after) >= 2 and after[1] == 'w':
                return self.get_oov_pho(last+after[:2], after[2:], phoList.append('OW'))
            elif len(before) == 0 and len(after) >= 4 and after[1:4] == 'ver':
                phoList += ['OW', 'V', 'ER']
                return self.get_oov_pho(last+after[:4], after[4:], phoList)
            elif len(after) >= 2 and after[1] == 'v':
                phoList += ['AH', 'V']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 3 and self.star(after[1]) and self.percent(after[2:]):
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('OW'))
            elif len(after) >= 4 and self.star(after[1]) and after[2:4] == 'en':
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('OW'))
            elif len(after) >= 4 and self.star(after[1]) and after[2] == 'i' and self.pound(after[3]):
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('OW'))
            elif len(after) >= 3 and after[1:3] == 'ld':
                phoList += ['OW', 'L']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 5 and after[1:5] == 'ught':
                phoList += ['AO', 'T']
                return self.get_oov_pho(last+after[:5], after[5:], phoList)
            elif len(after) >= 4 and after[1:4] == 'ugh':
                phoList += ['AH', 'F']
                return self.get_oov_pho(last+after[:4], after[4:], phoList)
            elif len(before) == 0 and len(after) >= 2 and after[1] == 'u':
                return self.get_oov_pho(last+after[:2], after[2:], phoList.append('AW'))
            elif len(before) >= 1 and len(after) >= 4 and before[-1] == 'h' and after[1:3] == 'us' and self.pound(after[3]):
                return self.get_oov_pho(last+after[:2], after[2:], phoList.append('AW'))
            elif len(after) >= 3 and after[1:3] == 'us':
                phoList += ['AX', 'S']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(after) >= 3 and after[1:3] == 'ur':
                phoList += ['AO', 'R']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(after) >= 4 and after[1:4] == 'uld':
                phoList += ['UH', 'D']
                return self.get_oov_pho(last+after[:4], after[4:], phoList)
            elif len(before) >= 1 and len(after) >= 4 and self.star(before[-1]) and after[1] == 'u' and self.star(after[2]) and after[3] == 'l':
                return self.get_oov_pho(last+after[:2], after[2:], phoList.append('AH'))
            elif len(after) >= 3 and after[1:3] == 'up':
                pholist += ['UW', 'P']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(after) >= 2 and after[1] == 'u':
                return self.get_oov_pho(last+after[:2], after[2:], phoList.append('AW'))
            elif len(after) >= 2 and after[1] == 'y':
                return self.get_oov_pho(last+after[:2], after[2:], phoList.append('OY'))
            elif len(after) >= 4 and after[1:4] == 'ing':
                phoList += ['OW', 'IH', 'NX']
                return self.get_oov_pho(last+after[:4], after[4:], phoList)
            elif len(after) >= 2 and after[1] == 'i':
                return self.get_oov_pho(last+after[:2], after[2:], phoList.append('OI'))
            elif len(after) >= 3 and after[1:3] == 'or':
                phoList += ['AO', 'R']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(after) >= 3 and after[1:3] == 'ok':
                pholist += ['UH', 'K']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(after) >= 3 and after[1:3] == 'od':
                phoList += ['UH', 'D']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(after) >= 2 and after[1] == 'o':
                return self.get_oov_pho(last+after[:2], after[2:], phoList.append('UW'))
            elif len(after) >= 2 and after[1] == 'e':
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('OW'))
            elif len(after) == 1:
                return phoList.append('OW')
            elif len(after) >= 2 and after[1] == 'a':
                return self.get_oov_pho(last+after[:2], after[2:], phoList.append('OW'))
            elif len(before) == 0 and len(after) >= 4 and after[1:4] == 'nly':
                phoList += ['OW', 'N', 'L', 'IY']
                return self.get_oov_pho(last+after[:4], after[4:], phoList)
            elif len(before) == 0 and len(after) == 4 and after[1:4] == 'nce':
                phoList += ['W', 'AH', 'N', 'S']
                return self.get_oov_pho(last+after[:4], after[4:], phoList)
            elif len(after) >= 3 and after[1:3] == 'nt':
                phoList += ['OW', 'N', 'T']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(before) >= 1 and len(after) >= 2 and before[-1] == 'c' and after[1] == 'n':
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('AA'))
            elif len(after) >= 3 and after[1:3] == 'ng':
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('AO'))
            elif len(before) >= 1 and len(after) >= 2 and self.star(before[-1]) and set(before).intersection(self.vowel) == set([]) and after[1] == 'n':
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('AH'))
            elif len(before) >= 1 and len(after) >= 2 and before[-1] == 'i' and after[1] == 'n':
                phoList += ['AX', 'N']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(before) >= 1 and len(after) == 2 and set(before).intersection(self.vowel) != set([]) and after[1] == 'n':
                phoList += ['AX', 'N']
                return phoList
            elif len(before) >= 2 and len(after) >= 2 and self.star(before[-1]) and after[1] == 'n' and set(before[:-1]).intersection(self.vowel) != set([]):
                phoList += ['AX', 'N']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) == 3 and after[1:3] == 'st':
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('OW'))
            elif len(after) >= 3 and after[1] == 'f' and self.star(after[2]):
                phoList += ['AO', 'F']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(after) >= 5 and after[1:5] == 'ther':
                phoList += ['AH', 'DH', 'ER']
                return self.get_oov_pho(last+after[:5], after[5:], phoList)
            elif len(after) == 3 and after[1:3] == 'ss':
                phoList += ['AO', 'S']
                return phoList
            elif len(before) >= 2 and len(after) >= 2 and self.star(before[-1]) and set(before[:-1]).intersection(self.vowel) != set([]) and after[1] == 'm':
                phoList += ['AH', 'M']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            else:
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('AA'))

        elif after[0] == 'p':
            if len(after) >= 2 and after[1] == 'h':
                return self.get_oov_pho(last+after[:2], after[2:], phoList.append('F'))
            elif len(after) >= 4 and after[1:4] == 'eop':
                phoList += ['P', 'IY', 'P']
                return self.get_oov_pho(last+after[:4], after[4:], phoList)
            elif len(after) >= 3 and after[1:3] == 'ow':
                phoList += ['P', 'AW']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(after) == 3 and after[1:3] == 'ut':
                phoList += ['P', 'UH', 'T']
                return phoList
            else:
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('P'))

        elif after[0] == 'q':
            if len(after) >= 4 and after[1:4] == 'uar':
                phoList += ['K', 'W', 'AO', 'R']
                return self.get_oov_pho(last+after[:4], after[4:], phoList)
            elif len(after) >= 2 and after[1] == 'u':
                phoList += ['K', 'W']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            else:
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('K'))

        elif after[0] == 'r':
            if len(before) == 0 and len(after) >= 4 and after[1] == 'e' and self.star(after[2]) and self.pound(after[3]):
                phoList += ['R', 'IY']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            else:
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('R'))

        elif after[0] == 's':
            if len(after) >= 2 and after[1] == 'h':
                return self.get_oov_pho(last+after[:2], after[2:], phoList.append('SH'))
            elif len(before) >= 1 and len(after) >= 4 and self.pound(before[-1]) and after[1:4] == 'ion':
                phoList += ['ZH', 'AX', 'N']
                return self.get_oov_pho(last+after[:4], after[4:], phoList)
            elif len(after) >= 4 and after[1:4] == 'ome':
                phoList += ['S', 'AH', 'M']
                return self.get_oov_pho(last+after[:4], after[4:], phoList)
            elif len(before) >= 1 and len(after) >= 4 and self.pound(before[-1]) and after[1:3] == 'ur' and self.pound(after[3]):
                phoList += ['ZH', 'ER']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(after) >= 4 and after[1:3] == 'ur' and self.pound(after[3]):
                phoList += ['SH', 'ER']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(before) >= 1 and len(after) >= 3 and self.pound(before[-1]) and after[1] == 'u' and self.pound(after[2]):
                phoList += ['ZH', 'UW']
                return self.get_oov_pho(last+after[:2], after[2:], phoList)
            elif len(before) >= 1 and len(after) >= 4 and self.pound(before[-1]) and after[1:3] == 'su' and self.pound(after[3]):
                phoList += ['SH', 'UW']
                return self.get_oov_pho(last+after[:3], after[3:], phoList)
            elif len(before) >= 1 and len(after) == 3 and self.pound(before[-1]) and after[1:3] == 'ed':
                phoList += ['Z', 'D']
                return phoList
            elif len(before) >= 1 and len(after) >= 2 and self.pound(before[-1]) and self.pound(after[1]):
                return self.get_oov_pho(last+after[:1], after[1:], phoList.append('Z'))
            elif len(after) >= 4 and after[1:4] == 'aid':
                phoList += ['S', 'EH', 'D']
                return self.get_oov_pho(last+after[:4], after[4:], phoList)
            elif len(before) >= 1 and len(after) >= 4 and self.star(before[-1]) and after[1:4] == 'ion':
                phoList += ['SH', 'AX', 'N']
                return self.get_oov_pho(last+after[:4], after[4:], phoList)
            elif len(after) >= 2 and after[1] == 's':
                return self.get_oov_pho(last+after[:1], after[1:], phoList)
            elif len(before) >= 1 and len(after) == 1 and self.dot(before[-1]):
                return phoList.append('Z')
            elif len(before) >= 3 and len(after) == 1 and before[-1] == 'e' and self.dot(before[-2]) and set(before[:-2]).intersection(self.vowel) != set([]):
                return phoList.append('Z')
            elif len(before) >= 4 and len(after) == 1 and self.pound(before[-1]) and self.pound(before[-2]) and self.findConsAfterVowel(before[:-2]):
                phoList.append('Z')
                return phoList
            elif len(before) >=3 and len(after) == 1 and self.pound(before[-1]) and self.findConsAfterVowel(before[:-1]):
                phoList.append('S')
                return phoList
            elif len(before) >= 1 and before[-1] == 'u' and len(after) == 1:
                phoList.append('S')
                return phoList
            elif len(before) >= 1 and len(after) == 1 and self.pound(before[-1]) and set(before[:-1]).intersection(set(self.vowel)) == set([]):
                phoList.append('Z')
                return phoList
            elif len(before) == 0 and len(after) >= 3 and after[1:3] == 'ch':
                phoList += ['S', 'K']
                return self.get_oov_pho(before+after[:3], after[3:], phoList)
            elif len(after) >= 3 and after[1] == 'c' and self.plus(after[2]):
                return self.get_oov_pho(before+after[:1], after[1:], phoList)
            elif len(before) >= 1 and self.pound(before[-1]) and len(after) >= 2 and after[1] == 'm':
                phoList += ['Z', 'M']
                return self.get_oov_pho(before+after[:2], after[2:], phoList)
            elif len(before) >=1 and self.pound(before[-1]) and len(after) >= 2 and after[1] == 'n':
                phoList+= ['Z', 'AX', 'N']
                return self.get_oov_pho(before+after[:2], after[2:], phoList)
            else:
                phoList.append('S')
                return self.get_oov_pho(before+after[:1], after[1:], phoList)
            
        elif after[0] == 't':
            if len(after) == 2 and after[1] == 'o':
                phoList += ['T', 'UW']
                return phoList
            elif len(after) == 4 and after[1:] == 'hat':
                phoList += ['DH', 'IH', 'S']
                return phoList
            elif len(before) == 0 and len(after) >= 4 and after[1:4] == 'hey':
                phoList += ['DH', 'EY']
                return self.get_oov_pho(before+after[:4], after[4:], phoList)
            elif len(before) == 0 and len(after) >= 5 and after[1:5] == 'here':
                phoList += ['DH', 'EH', 'R']
                return self.get_oov_pho(before+after[:5], after[5:], phoList)
            elif len(after) >= 4 and after[1:4] == 'her':
                phoList += ['DH', 'ER']
                return self.get_oov_pho(before+after[:4], after[4:], phoList)
            elif len(after) >= 5 and after[1:5] == 'heir':
                phoList += ['DH', 'EH', 'R']
                return self.get_oov_pho(before+after[:5], after[5:], phoList)
            elif len(after) == 5 and after[1:5] == 'hese':
                phoList += ['DH', 'IY', 'Z']
                return phoList
            elif len(before) == 0 and len(after) >= 4 and after[1:4] == 'hen':
                phoList += ['DH', 'EH', 'N']
                return self.get_oov_pho(before+after[:4], after[4:], phoList)
            elif len(after) >= 7 and after[1:7] == 'hrough':
                phoList += ['TH', 'R', 'UW']
                return self.get_oov_pho(before+after[:7], after[7:], phoList)
            elif len(after) >= 5 and after[1:5] == 'hose':
                phoList += ['DH', 'OW', 'Z']
                return self.get_oov_pho(before+after[:5], after[5:], phoList)
            elif len(after) == 6 and after[1:] == 'hough':
                phoList += ['DH', 'OW']
                return phoList
            elif len(before) == 0 and len(after) >= 4 and after[1:4] == 'hus':
                phoList += ['DH', 'AH', 'S']
                return self.get_oov_pho(before+after[:4], after[4:], phoList)
            elif len(after) >= 2 and after[1] == 'h':
                phoList.append('TH')
                return self.get_oov_pho(before+after[:2], after[2:], phoList)
            elif len(before) >= 1 and len(after) == 3 and set(before).intersection(set(self.vowel)) != set([]) and after[1:] == 'ed':
                phoList += ['T', 'IH', 'D']
                return phoList
            elif len(before) >= 1 and len(after) >= 4 and before[-1] == 's' and after[1] == 'i' and self.pound(after[2]) and after[3] == 'n':
                phoList.append('CH')
                return self.get_oov_pho(before+after[:2], after[2:], phoList)
            elif len(after) >= 3 and after[1:3] == 'io':
                phoList.append('SH')
                return self.get_oov_pho(before+after[:2], after[2:], phoList)
            elif len(after) >= 3 and after[1:3] == 'ia':
                phoList.append('SH')
                return self.get_oov_pho(before+after[:2], after[2:], phoList)
            elif len(after) >= 4 and after[1:4] == 'ien':
                phoList += ['SH', 'AX', 'N']
                return self.get_oov_pho(before+after[:4], after[4:], phoList)
            elif len(after) >= 4 and after[1:3] == 'ur' and self.pound(after[3]):
                phoList += ['CH', 'ER']
                return self.get_oov_pho(before+after[:3], after[3:], phoList)
            elif len(after) >= 3 and after[1:3] == 'ua':
                phoList += ['CH', 'UW']
                return self.get_oov_pho(before+after[:2], after[2:], phoList)
            elif len(before) == 0 and len(after) >= 3 and after[1:3] == 'wo':
                phoList += ['T', 'UW']
                return self.get_oov_pho(before+after[:3], after[3:], phoList)
            else:
                phoList.append('T')
                return self.get_oov_pho(before+after[:1], after[1:], phoList)

        elif after[0] == 'u':
            if len(before) == 0 and len(after) >= 3 and after[1:3] == 'ni':
                phoList += ['Y', 'UW', 'N']
                return self.get_oov_pho(before+after[:2], after[2:], phoList)
            elif len(before) == 0 and len(after) >= 2 and after[1] == 'n':
                phoList += ['AH', 'N']
                return self.get_oov_pho(before+after[:2], after[2:], phoList)
            elif len(before) == 0 and len(after) >= 4 and after[1:4] == 'pon':
                phoList += ['AX', 'P', 'AO', 'N']
                return self.get_oov_pho(before+after[:4], after[4:], phoList)
            elif len(before) >= 1 and self.amp1(before[-1]) and len(after) >= 3 and after[1] == 'r' and self.pound(after[2]):
                phoList += ['UH', 'R']
                return self.get_oov_pho(before+after[:2], after[2:], phoList)
            elif len(before) >= 2 and self.amp2(before[-2:]) and len(after) >= 3 and after[1] =='r' and self.pound(after[2]):
                phoList+= ['UH', 'R']
                return self.get_oov_pho(before+after[:2], after[2:], phoList)
            elif len(after) >= 3 and after[1] =='r' and self.pound(after[2]):
                phoList+= ['Y', 'UH', 'R']
                return self.get_oov_pho(before+after[:2], after[2:], phoList)
            elif len(after) >= 2 and after[1] == 'r':
                phoList.append('ER')
                return self.get_oov_pho(before+after[:2], after[2:], phoList)
            elif len(after) == 2 and self.star(after[1]):
                phoList.append('AH')
                return self.get_oov_pho(before+after[:1], after[1:], phoList)
            elif len(after) >= 3 and self.star(after[1]) and self.star(after[2]):
                phoList.append('AH')
                return self.get_oov_pho(before+after[:1], after[1:], phoList)
            elif len(after) >= 2 and after[1] == 'y':
                phoList.append('AY')
                return self.get_oov_pho(before+after[:2], after[2:], phoList)
            elif len(before) == 1 and before[-1] == 'g' and len(after) >= 2 and self.pound(after[1]):
                return self.get_oov_pho(before+after[:1], after[1:], phoList)
            elif len(before) >= 1 and before[-1] == 'g' and self.percent(after[1:]):
                return self.get_oov_pho(before+after[:1], after[1:], phoList)
            elif len(before) >= 1 and before[-1] == 'g' and len(after) >= 2 and self.pound(after[1]):
                phoList.append('W')
                return self.get_oov_pho(before+after[:1], after[1:], phoList)
            elif len(before) >= 2 and before[-1] == 'n' and self.pound(before[-2]):
                phoList += ['Y', 'UW']
                return self.get_oov_pho(before+after[:1], after[1:], phoList)
            elif len(before) >= 2 and self.amp2(before[-2:]):
                phoList.append('UW')
                return self.get_oov_pho(before+after[:1], after[1:], phoList)
            elif len(before) >= 1 and self.amp1(before[-1]):
                phoList.append('UW')
                return self.get_oov_pho(before+after[:1], after[1:], phoList)
            else:
                return self.get_oov_pho(before+after[:1], after[1:], phoList)

        elif after[0] == 'v':
            if len(after) >= 4 and after[1:4] == 'iew':
                phoList += ['V', 'Y', 'UW']
                return self.get_oov_pho(before+after[:4], after[4:], phoList)
            else:
                phoList.append('V')
                return self.get_oov_pho(before+after[:1], after[1:], phoList)

        elif after[0] == 'w':
            if len(before) == 0 and len(after) >= 4 and after[1:4] == 'ere':
                phoList += ['W', 'ER']
                return self.get_oov_pho(before+after[:4], after[4:], phoList)
            elif len(after) >= 3 and after[1:3] == 'as':
                phoList += ['W', 'AA']
                return self.get_oov_pho(before+after[:2], after[2:], phoList)
            elif len(after) >= 3 and after[1:3]== 'at':
                phoList+= ['W', 'AA']
                return self.get_oov_pho(before+after[:2], after[2:], phoList)
            elif len(after) >= 5 and after[1:5] == 'here':
                phoList += ['WH', 'EH', 'R']
                return self.get_oov_pho(before+after[:5], after[5:], phoList)
            elif len(after) >= 4 and after[1:4] == 'hat':
                phoList += ['WH', 'AA', 'R']
                return self.get_oov_pho(before+after[:4], after[4:], phoList)
            elif len(after) >= 4 and after[1:4] == 'hol':
                phoList += ['HH', 'OW', 'L']
                return self.get_oov_pho(before+after[:4], after[4:], phoList)
            elif len(after) >= 3 and after[1:3] == 'ho':
                phoList += ['HH', 'UW']
                return self.get_oov_pho(before+after[:3], after[3:], phoList)
            elif len(after) >= 2 and after[1] == 'h':
                phoList.append('WH')
                return self.get_oov_pho(before+after[:2], after[2:], phoList)
            elif len(after) >= 3 and after[1:3] == 'ar':
                phoList += ['W', 'AO', 'R']
                return self.get_oov_pho(before+after[:3], after[3:], phoList)
            elif len(after) >= 3 and after[1:3] == 'or':
                phoList += ['W', 'ER']
                return self.get_oov_pho(before+after[:3], after[3:], phoList)
            elif len(after) >= 2 and after[1] == 'r':
                phoList.append('R')
                return self.get_oov_pho(before+after[:2], after[2:], phoList)
            else:
                phoList.append('R')
                return self.get_oov_pho(before+after[:1], after[1:], phoList)

        elif after[0] == 'x':
            phoList += ['K', 'S']
            return self.get_oov_pho(before+after[:1], after[1:], phoList)
            
        elif after[0] == 'y':
            if len(after) >= 5 and after[1:5] == 'oung':
                phoList += ['Y', 'AH', 'NX']
                return self.get_oov_pho(before+after[:5], after[5:], phoList)
            elif len(before) == 0 and len(after) >= 3 and after[1:3] == 'ou':
                phoList += ['Y', 'UW']
                return self.get_oov_pho(before+after[:3], after[3:], phoList)
            elif len(before) == 0 and len(after) >= 3 and after[1:3] == 'es':
                phoList += ['Y', 'EH', 'S']
                return self.get_oov_pho(before+after[:3], after[3:], phoList)
            elif len(before) == 0:
                phoList.append('Y')
                return self.get_oov_pho(before+after[:1], after[1:], phoList)
            elif len(before) >= 2 and len(after) == 1 and self.star(before[-1]) and set(before[:-1]).intersection(set(self.vowel)) != set([]):
                phoList.append('IY')
                return self.get_oov_pho(before+after[:1], after[1:], phoList)
            elif len(before) >=2 and len(after) >= 2 and self.star(before[-1])and set(before[:-1]).intersection(set(self.vowel)) != set([]) and after[1] == 'i':
                phoList.append('IY')
                return self.get_oov_pho(before+after[:1], after[1:], phoList)
            elif len(after) == 1 and set(before).intersection(self.vowel) == set([]):
                phoList.append('AY')
                return self.get_oov_pho(before+after[:1], after[1:], phoList)
            elif len(after) >= 2 and set(before).intersection(self.vowel) == set([]) and self.pound(after[1]):
                phoList.append('AY')
                return self.get_oov_pho(before+after[:1], after[1:], phoList)
            elif len(after) >= 4 and set(before).intersection(self.vowel) == set([]) and self.star(after[1]) and self.plus(after[2]) and set(after[3:]).intersection(self.vowel) != set([]):
                phoList.append('IH')
                return self.get_oov_pho(before+after[:1], after[1:], phoList)
            elif len(after) >= 3 and set(before).intersection(self.vowel) == set([]) and self.star(after[1]) and set(after[2:]).intersection(self.vowel) != set([]):
                phoList.append('AY')
                return self.get_oov_pho(before+after[:1], after[1:], phoList)
            else:
                phoList.append('IH')
                return self.get_oov_pho(before+after[:1], after[1:], phoList)

        elif after[0] == 'z':
            phoList.append('Z')
            return self.get_oov_pho(before+after[:1], after[1:], phoList)
        
        return phoList

    def pound( self , charSeq ):
        if charSeq[0] in self.vowel:
            return True
        else:
            return False

    def star( self , charSeq ):
        if charSeq[0] in self.consonant:
            return True
        else:
            return False

    def dot( self , charSeq ):
        if charSeq[0] in self.voiced:
            return True
        else:
            return False

    def dollar( self , charSeq ):
        if len(charSeq) > 1:
            if charSeq[0] in self.consonant and charSeq[1] in 'ie':
                return True
            else:
                return False
        else:
            return False

    def percent( self , charSeq ):
        if charSeq in self.suffix:
            return True
        else:
            return False

    def amp1( self , charSeq ):
        if charSeq[0] in self.sibilant:
            return True
        else:
            return False

    def amp2( self , charSeq ):
        if charSeq[0:2] in self.sibilant:
            return True
        else:
            return False
                        

    def at1( self , charSeq ):
        if charSeq[0] in self.nonpal:
            return True
        else:
            return False

    def at2( self , charSeq ):
        if charSeq[0:2] in self.nonpal:
            return True
        else:
            return False

    def plus( self , charSeq ):
        if charSeq[0] in self.front:
            return True
        else:
            return False
                
    def findConsAfterVowel( self , charSeq ):
        for c in enumerate(charSeq):
            if c[1] in self.vowel:
                for d in charSeq[c[0]+1:]:
                    if d in self.consonant:
                        return True
        return False
