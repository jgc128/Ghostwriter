from common_lib.parse_lyrics import parse_lyrics
from markov_model.n_gram import NGramModel
from os import listdir


allLyrics = []
lyricDir = '../data/hirjee_brown_songs'
for lyricFile in listdir(lyricDir):
    #print lyricFile.split('-')
    if lyricFile.split('-')[0] == 'eminem':
        #print parse_lyrics(lyricDir+'/'+lyricFile)
        allLyrics += parse_lyrics(lyricDir+'/'+lyricFile)


#allLyrics = parse_lyrics('song.txt')
#print allLyrics
ghostwriter = NGramModel( allLyrics )
#print 'start: '+ghostwriter.highestStart
#print ghostwriter.nGramCount[str(['knew','i'])]
history = ['<startVerse>']
#counter = 0
outfile = open('ghost-lyrics', 'a')
#while counter < 200:
current = ''
while current != '<endVerse>':
    nextToken = ghostwriter.genNextToken( history )
    if nextToken != '<endLine>' and nextToken != '<endVerse>':
        outfile.write(nextToken+' ')
    else:
        outfile.write('\n')
    #if nextToken == '<endLine>':
    current = nextToken
    history = history[-1:] + [nextToken]
    #counter += 1

outfile.write('\n')
outfile.close()

