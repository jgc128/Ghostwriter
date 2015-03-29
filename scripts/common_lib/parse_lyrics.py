from nltk import word_tokenize
from re import sub

def parse_lyrics( lyricFilePath ):
    headerFields = ['Artist', 'Album', 'Song', 'Typed by']
    lyricsTokens = []
    for line in open(lyricFilePath).readlines():
        if line.split(':')[0] in headerFields or line[0] == '[':
            continue
        elif len(line) >= 6 and line.lower()[:6] == 'chorus':
            continue
        else:
            lineStrip = line.strip('\n')
            lineNoParens = sub(r'\([^)]*\)', '', lineStrip)
            if lineNoParens == '' and lineStrip != lineNoParens:
                continue
            tokens = word_tokenize(sub(r'([^\s\w]|_)+', '', lineNoParens).lower())
            if tokens == []:    
                lyricsTokens += ['<endVerse>', '<startVerse>']
            else:
                tokens.append('<endLine>')
                lyricsTokens += tokens
    if lyricsTokens[-1] == '<startVerse>':
        del lyricsTokens[-1]
    if lyricsTokens[0] == '<endVerse>':
        del lyricsTokens[0]
    if lyricsTokens[-1] != '<endVerse>':
        lyricsTokens.append('<endVerse>')
    if lyricsTokens[0] != '<startVerse>':
        lyricsTokens.insert(0,'<startVerse>')
    return lyricsTokens
        
