#!/usr/bin/python3

import os
import re
import json
import argparse
import itertools
from nltk import word_tokenize


def get_songs_list(path):
    # result = [os.path.join(path, s) for s in os.listdir(path)]
    result = os.listdir(path)
    return result


def parse_song_file(filename, dir):
    
    no_parens_re = re.compile(r'\([^)]*\)')
    strip_special_chars_re = re.compile(r'([^\s\w]|_)+')
    chorus_re = re.compile(r'^[(\[]?(repeat\s)?chorus\:?')

    skips = [
        lambda r : r.startswith('artist:'),
        lambda r : r.startswith('album:'),
        lambda r : r.startswith('song:'),
        lambda r : r.startswith('typed by:'),
        lambda r : r.startswith('chorus'),
        lambda r : r.startswith('(chorus'),
        lambda r : r.startswith('(repeat'),
        lambda r : len(r) > 0 and r[0] == '[',
    ]
    cleans_pre = [
        lambda r : r.strip(),
        lambda r : r.lower(),
    ]
    cleans_post = [
        lambda r : no_parens_re.sub('', r),   
        lambda r : strip_special_chars_re.sub(' ', r),
    ]

    result = []

    with open(os.path.join(dir, filename), 'r') as f:
        data = f.readlines()

    data = [{'original': line, 'transformed': line, 'skip': False, 'tokens': []} for line in data]

    # clean and skip 
    for line in data:
        line['transformed'] = line['original']

        for c in cleans_pre:
            line['transformed'] = c(line['transformed'])

        # check for skip
        line['skip'] = any([s(line['transformed']) for s in skips])

        for c in cleans_post:
            line['transformed'] = c(line['transformed'])

        pass

    # tokenize
    for line in data:
        if not line['skip']:
            line['tokens'] = word_tokenize(line['transformed'])


    state = 'normal'
    for line in data:
        is_skip = line['skip'] == True
        is_break = not is_skip and len(line['tokens']) == 0
        is_chorus = chorus_re.match(line['transformed']) is not None
        
        if is_chorus:
            state = 'chorus'

        if is_break:
            state = 'normal'

        if not is_skip and state == 'normal':
            if len(line['tokens']) > 0:
                line['tokens'].append('<endLine>')
                result.append(line['tokens'])

        if is_break and len(result) > 0 and result[-1] != '<startVerse>':
            result.append('<endVerse>')
            result.append('<startVerse>')


    # clean results
    if result[0] == '<endVerse>':
        del result[0]
    if result[0] != '<endVerse>':
        result.insert(0, '<startVerse>')
    if result[-1] == '<startVerse>':
        del result[-1]
    if result[-1] != '<endVerse>':
        result.append('<endVerse>')


    return result


def save_parsed_song(filename, dir, song_data):
    song_str = json.dumps(song_data, ensure_ascii = False, indent = 4)
    with open(os.path.join(dir, filename), 'w') as f:
        f.write(song_str)
        f.write('\n')

		
		
		
# parse commandline arguments
parser = argparse.ArgumentParser(description='Parse lyrics file and save it to JSON format')
parser.add_argument("lyrics_dir", help='directory with raw lyrics')
parser.add_argument("output_dir", help='output directory to save parsed lyrics')
args = parser.parse_args()



songs = get_songs_list(args.lyrics_dir)


for i, s in enumerate(songs):
    cleaned_song = parse_song_file(s, args.lyrics_dir)
    save_parsed_song(s, args.output_dir, cleaned_song)

    if i % 500 == 0:
        print(i, s)

print('All done!')


