#import sys
#sys.path.append('theano_lstm')
from util import *
from common_lib.lyrics_database import LyricsDatabase
import pickle
import sys

vocab = Vocab()

myData = LyricsDatabase('/usr/cs/grad/doc/ppotash/ghostwriter/data/top-selling-rappers-cleaned-json')

#allTokens = myData.get_lyrics_from_artist_as_plain_list('jay')

#vocab.add_words(allTokens)

verseList = myData.get_lyrics_from_artist_as_list_of_verses('fabolous')

for v in verseList:
    if len(v) < 175:
        continue
    #if len(v) <800:
    vocab.add_words(v)#numerical_lines.append(vocab(v))

#print len(vocab)
#sys.exit()


numerical_lines = []
for v in verseList:
    if len(v) < 175:
        continue
    #if len(v) <800:
    numerical_lines.append(vocab(v))

#print len(numerical_lines)
#sys.exit()
#for line in open('sample_text').readlines():
#    vocab.add_words(line.strip("\n").split(" "))

#numerical_lines = []
#for line in open('sample_text').readlines():
#    numerical_lines.append(vocab(line.strip("\n")))
    
numerical_lines, numerical_lengths = pad_into_matrix(numerical_lines)

model = Model(
    input_size=len(vocab),
    hidden_size=100,
    vocab_size=len(vocab),
    stack_size=2,
    celltype=LSTM
)

model.stop_on(vocab.word2index["<endVerse>"])

bestLyrics = ''
bestEr = float("inf")

for i in range(20000):
    error = model.update_fun(numerical_lines, numerical_lengths)
    if i % 20 == 0:
        print("epoch %(epoch)d, error=%(error).2f" % ({"epoch": i, "error": error}))
    if i % 100 == 0:
        print(vocab(model.greedy_fun(vocab.word2index["<startVerse>"])))
    if error < bestEr:
        bestEr = error
        bestLyrics = vocab(model.greedy_fun(vocab.word2index["<startVerse>"]))
    if i % 1000 == 0:
        with open('fabolous'+str(i), 'w') as f:
            f.write(str(error)+'\n'+str(vocab(model.greedy_fun(vocab.word2index["<startVerse>"]))))

with open('fabolous-expanded', 'w') as f:
    f.write(str(bestLyrics))

"""
with open('model-jay', 'w') as f:
    pickle.dump(model, f)

with open('vocab-jay', 'w') as f:
    pickle.dump(vocab, f)
"""
