from __future__ import print_function
import os
import argparse
import subprocess

rhyme_analizer_jar = '/data1/nlp-data/ghostwriter/rhyme_analizer/RhymeAnalizer.jar'

def run_command(cmd, arguments):
	params = []
	params.append(cmd)
	if isinstance(arguments, list):
		params.extend(arguments)
	else:
		params.append(arguments)
		
	return subprocess.check_output(params)
	
	
def get_lyrics_stat(filename):
	cmd = 'java'
	arguments = ['-jar', rhyme_analizer_jar, filename]
	output = run_command(cmd, arguments)
	
	result = {}
	for line in output.split('\n'):
		dv = line.split(':')
		
		if len(dv) == 2:
			key = dv[0].strip()
			value = float(dv[1].strip())
			result[key] = value
			
	return result

	
if __name__ == "__main__":
	# parse commandline arguments
	parser = argparse.ArgumentParser(description='Print statistics about lyrics')
	parser.add_argument("filename", help='Path to the file with lyrics')
	args = parser.parse_args()	
	
	statistics = get_lyrics_stat(args.filename)
	for k in statistics.keys():
		print(k, statistics[k])

