#import sys
#sys.path.append('theano_lstm')
from util import *
from common_lib.lyrics_database import LyricsDatabase

vocab = Vocab()

myData = LyricsDatabase('/data1/nlp-data/ghostwriter/data/top-selling-rappers-cleaned-json')

allTokens = myData.get_lyrics_from_artist_as_plain_list('jay')

vocab.add_words(allTokens)

verseList = myData.get_lyrics_from_artist_as_list_of_verses('jay')

numerical_lines = []
for v in verseList:
    numerical_lines.append(vocab(v))

#for line in open('sample_text').readlines():
#    vocab.add_words(line.strip("\n").split(" "))

#numerical_lines = []
#for line in open('sample_text').readlines():
#    numerical_lines.append(vocab(line.strip("\n")))
    
numerical_lines, numerical_lengths = pad_into_matrix(numerical_lines)

model = Model(
    input_size=10,
    hidden_size=10,
    vocab_size=len(vocab),
    stack_size=1,
    celltype=LSTM
)

model.stop_on(vocab.word2index["<endVerse>"])

for i in range(100):
    error = model.update_fun(numerical_lines, numerical_lengths)
    if i % 2 == 0:
        print("epoch %(epoch)d, error=%(error).2f" % ({"epoch": i, "error": error}))
    if i % 20 == 0:
        print(vocab(model.greedy_fun(vocab.word2index["<startVerse>"])))
