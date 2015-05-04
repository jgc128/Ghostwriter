import os
import json
import six
from collections import defaultdict

class LyricsDatabase(object):
	def __init__(self, data_dir):
		self.__data_dir = data_dir
		self.__lyrics_cache = None
		
	def __create_lyrics_cache(self):
		self.__lyrics_cache = defaultdict(list)
	
		files = os.listdir(self.__data_dir)
		for f in files:
			artist = f.split('-')[0]
			
			self.__lyrics_cache[artist].append(f)
		
	def load_lyric(self, filename):
		path = os.path.join(self.__data_dir, filename)
		with open(path, 'r') as f:
			lyric = json.load(f)
		
		return lyric
	
	def get_artists_names(self):
		if self.__lyrics_cache is None:
			self.__create_lyrics_cache()
			
		return self.__lyrics_cache.keys()
	
	def get_lyrics_files_from_artist(self, artist):
		availabel_artist = self.get_artists_names()
	
		if artist not in availabel_artist:
			return None
		else:
			return self.__lyrics_cache[artist]

	
	def get_lyrics_from_artist(self, artist):
		lyrics_files = self.get_lyrics_files_from_artist(artist)
		
		lyrics = [self.load_lyric(f) for f in lyrics_files]
		
		return lyrics
		
	def get_lyrics_from_artist_as_plain_list(self, artist):
		lyrics = self.get_lyrics_from_artist(artist)
		
		result = []
		
		for lyric in lyrics:
			for word_or_list in lyric:
				if isinstance(word_or_list, six.string_types):
					result.append(word_or_list)
				else:
					result.extend(word_or_list)
		
		return result
	
	def get_lyrics_from_artist_as_list_of_verses(self, artist):
		lyrics = self.get_lyrics_from_artist(artist)
		
		result = list()
		current_verse = list()
		
		for lyric in lyrics:
			for word_or_list in lyric:
				
				if isinstance(word_or_list, six.string_types):
					current_verse.append(word_or_list)
				else:
					current_verse.extend(word_or_list)
		
				if word_or_list == "<endVerse>":
					result.append(current_verse)
					current_verse = list()

		return result
	
	
		
	