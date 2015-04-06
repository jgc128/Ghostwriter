import os
import json

class LyricsDatabse(object):
	def __init__(self, data_dir):
		self.__data_dir = data_dir
		self.__lyrics_cache = None
		
	def __create_lyrics_cache(self):
		self.__lyrics_cache = {}
	
		files = os.listdir(self.__data_dir)
		for f in files:
			artist = f.split('-')[0]
			
			if artist not in self.__lyrics_cache:
				self.__lyrics_cache[artist] = []
			
			self.__lyrics_cache[artist].append(f)
		
	def __load_lyric(self, filename):
		path = os.path.join(self.__data_dir, filename)
		with open(path, 'r') as f:
			lyric = json.load(f)
		
		return lyric
		
	def get_lyrics_from_artist(self, artist):
		if self.__lyrics_cache is None:
			self.__create_lyrics_cache()
			
		if artist not in self.__lyrics_cache:
			return None
			
		lyrics_files = self.__lyrics_cache[artist]
		
		lyrics = [self.__load_lyric(f) for f in lyrics_files]
		
		return lyrics
		
		
		
		
	