from common_lib.parse_lyrics import parse_lyrics
from markov_model.n_gram import NGramModel
from os import listdir


allLyrics = []

lyricDir = '../data/hirjee_brown_songs'
for lyricFile in listdir(lyricDir):
    #print lyricFile.split('-')
    #if lyricFile.split('-')[0] == 'jay':
    allLyrics += parse_lyrics(lyricDir+'/'+lyricFile)


#allLyrics = parse_lyrics('test-song')
#print allLyrics
nGram = 5
ghostwriter = NGramModel( allLyrics , nGram )
#print 'start: '+ghostwriter.highestStart
#print ghostwriter.nGramCount[str(['knew','i'])]
#print ghostwriter.startList[0][0][str(['<startVerse>'])]


history = ['<startVerse>', 'thug']
#counter = 0
outfile = open('a5', 'a')
#while counter < 200:
current = ''
while current != '<endVerse>':
    nextToken = ghostwriter.genNextToken( history )
    if nextToken == '<startVerse>':
        continue
    if nextToken != '<endLine>' and nextToken != '<endVerse>':
        outfile.write(nextToken+' ')
    else:
        outfile.write('\n')
    #if nextToken == '<endLine>':
    if len(history) < nGram-1:
        history.append(nextToken)
    else:
        history = history[1:] + [nextToken]
    current = nextToken

#outfile.write('\n')
outfile.close()

