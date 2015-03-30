#!/usr/bin/python3

import os
import sys
import csv
import requests
import argparse
from bs4 import BeautifulSoup


ohhla_pages_all_cache = {}
ohhla_artist_cache = {}

def warning(*objs):
	print("WARNING: ", *objs, file=sys.stderr)
	# print("WARNING: ", *objs)

# http://stackoverflow.com/a/3668771
def meta_redirect(soup):

    result = soup.find("meta", {"http-equiv": "Refresh"})
    if result:
        wait, text = result["content"].split(";")
        text = text.strip()
        if text.lower().startswith("url="):
            url=text[4:]
            return url
    return None


def download_ohhle_page(page):
    if page.lower().find('ohhla.com/') == -1:
        url = 'http://ohhla.com/' + page
    else:
        url = page

    r = requests.get(url)
    html_doc = r.text

    return html_doc

def soup_ohhla_page(page):
    html_doc = download_ohhle_page(page)
    soup = BeautifulSoup(html_doc)

    redirect = meta_redirect(soup)
    if redirect:
        return soup_ohhla_page(redirect)

    return soup

def get_ohhla_artist_song_links(artist_page):
    soup = soup_ohhla_page(artist_page)

    result = {}

    albums = soup.select('a[href^="YFA_"]')

    if len(albums) == 0:
        return None

    for a_album in albums:
        album_title = a_album.string.lower()

        album_href = a_album.attrs['href']
        sharp_pos = a_album.attrs['href'].find('#')
        if sharp_pos == -1:
            continue
        album_href = album_href[sharp_pos + 1:]

        album_a_near_table = soup.find('a', {'name': album_href})
        if album_a_near_table is None:
            continue

        album_table = album_a_near_table.parent.find('table')

        song_links = album_table.select('a[href^="anonymous/"]')
        song_data = [{'title': s.string.lower(), 'url': s.attrs['href']} for s in song_links if s.string]


        result[album_title] = {'title': album_title, 'songs': song_data}

    return result


def get_ohhla_all_pages_artist(page):
    soup = soup_ohhla_page(page)

    links_container = soup.find("pre")

    results = {}
    for child in links_container.findChildren('a'):
        if 'href' in child.attrs:
            artist = child.string.lower()
            url = child.attrs['href']

            results[artist] = { 'artist': artist, 'url': url }

    return results

def get_ohhla_artist_albums(artist):
    ohhla_page = get_ohhla_artist_page(artist)

    if ohhla_page not in ohhla_pages_all_cache:
        ohhla_pages_all_cache[ohhla_page] = get_ohhla_all_pages_artist(ohhla_page)

    if artist not in ohhla_pages_all_cache[ohhla_page]:
        warning('Artist Not Found: ', artist)
        return None

    if artist not in ohhla_artist_cache:
        album_song_links = get_ohhla_artist_song_links(ohhla_pages_all_cache[ohhla_page][artist]['url'])

        if album_song_links is None:
            warning('Manual Albums: ', artist)
            return None

        ohhla_artist_cache[artist] = album_song_links

    return ohhla_artist_cache[artist]



def get_ohhla_artist_page(artist):
    ohhla_pages = [
        { 'start': 'a', 'end': 'e', 'page': 'all.html' },
        { 'start': 'f', 'end': 'j', 'page': 'all_two.html' },
        { 'start': 'k', 'end': 'o', 'page': 'all_three.html' },
        { 'start': 'p', 'end': 't', 'page': 'all_four.html' },
        { 'start': 'u', 'end': 'z', 'page': 'all_five.html' },
    ]


    artist = artist[0].lower()
    for cat in ohhla_pages:
        if artist >= cat['start'] and artist <= cat['end']:
            return cat['page']

    return ohhla_pages[0]['page']

def read_data(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)

        res = [{'artist': r[0], 'album': r[1]} for r in reader]

    return res


def save_song_text(data_dir, artis, album, song, song_text):
    filename = os.path.join(
        data_dir,
        artis.replace(' ', '_').replace('/','_') + '-' + album.replace(' ', '_').replace('/','_') + '-' +  song.replace(' ', '_').replace('/','_') + '.txt'
    )

    with open(filename, 'w') as song_file:
        song_file.write(song_text)


def download_album_songs(artist, album, songs, data_dir):
    for s in songs:
        print('Downloading: ', s['title'])

        data = soup_ohhla_page(s['url'])

        song_tag = data.find('pre')
        if song_tag is None:
            song_tag = data.find('body')

        song_text = song_tag.get_text()
        save_song_text(data_dir, artist, album, s['title'], song_text)



# parse commandline arguments
parser = argparse.ArgumentParser(description='Download hip hip songs from http://www.ohhla.com/')
parser.add_argument("albums", help='file contains artist & album in csv format')
parser.add_argument("data_dir", help='output directory to save albums & songs')
args = parser.parse_args()

artist_album_data = read_data(args.albums)

for a in artist_album_data:
    artist_name = a['artist'].strip().lower()
    need_album_name = a['album'].strip().lower()

    print('Process:', artist_name, ' - ', need_album_name)

    artist_albums_data = get_ohhla_artist_albums(artist_name)

    if artist_albums_data is None:
        continue

    if need_album_name not in artist_albums_data:
        warning('Album Not Found: ', artist_name, ' - ', need_album_name)
        continue

    songs_data = download_album_songs(artist_name, need_album_name, artist_albums_data[need_album_name]['songs'], args.data_dir)

