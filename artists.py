import os
import sys
import requests
from utilities import uprint, load_json, write_json
import musicbrainzngs as mbz


def main():
    pass

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    import django
    django.setup()
    from app import models

    if len(sys.argv) == 2:
        if sys.argv[1] == 'fetch':
            print('fetching artists from musicbrainz.org...')
            mbz.set_useragent('play music app', '0.1', 'gabrielbusta@gmail.com')

            artists = []
            artists = mbz.search_artists(country='US', limit=100)['artist-list']
            artists.extend(mbz.search_artists(country='MX', limit=100)['artist-list'])
            artists.extend(mbz.search_artists(country='VE', limit=100)['artist-list'])
            artists.extend(mbz.search_artists(country='FR', limit=100)['artist-list'])
            artists.extend(mbz.search_artists(country='JP', limit=100)['artist-list'])
            artists.extend(mbz.search_artists(country='KR', limit=100)['artist-list'])
            artists.extend(mbz.search_artists(country='BR', limit=100)['artist-list'])
            artists.extend(mbz.search_artists(country='CN', limit=100)['artist-list'])
            artists.extend(mbz.search_artists(country='GB', limit=100)['artist-list'])
            artists.extend(mbz.search_artists(country='RU', limit=100)['artist-list'])
            artists.extend(mbz.search_artists(country='IT', limit=100)['artist-list'])
            artists.extend(mbz.search_artists(country='ES', limit=100)['artist-list'])
            artists.extend(mbz.search_artists(country='NG', limit=100)['artist-list'])
            artists.extend(mbz.search_artists(country='ZA', limit=100)['artist-list'])
            artists.extend(mbz.search_artists(country='IN', limit=100)['artist-list'])
            artists.extend(mbz.search_artists(country='CA', limit=100)['artist-list'])
            artists.extend(mbz.search_artists(country='AU', limit=100)['artist-list'])
            artists.extend(mbz.search_artists(country='NZ', limit=100)['artist-list'])
            artists.extend(mbz.search_artists(country='NO', limit=100)['artist-list'])
            artists.extend(mbz.search_artists(country='AR', limit=100)['artist-list'])

            print('saving to artists to artists.json...')
            write_json(artists, './artists.json')

    main()
