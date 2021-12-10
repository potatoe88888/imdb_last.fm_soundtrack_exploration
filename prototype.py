### SOURCES
# https://www.dataquest.io/blog/last-fm-api-python/
# https://www.w3resource.com/python-exercises/dictionary/python-data-type-dictionary-exercise-49.php
# https://stackoverflow.com/questions/44720682/does-the-lastfm-api-provide-youtube-links
# https://docs.python.org/3/library/functions.html#input

import requests
import json
from bs4 import BeautifulSoup, SoupStrainer

API_KEY = '12a9ed2e87c6978ad67c7e07792f1622'
USER_AGENT = 'bayera88888'
ARTIST_LIMIT = 20
TOP_TRACKS_LIMIT = 5

def lastfm_getData(payload):
    # use a header for last.fm to not block the request [https://www.last.fm/api/intro]
    headers = {'user-agent': USER_AGENT}
    url = 'https://ws.audioscrobbler.com/2.0/'

    # build payload
    payload['api_key'] = API_KEY
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, indent=4)
    print(text)

def get_similarArtists(userInput_artist, onlyYOUTUBE = 0):
    # capture similar artists and urls
    similar_artist_array = []
    results_dict = {}

    # build out payload -- artist name
    request_sa = lastfm_getData({
        'method': 'artist.getSimilar',
        'limit': ARTIST_LIMIT,
        'autocorrect': 1,                           # allows for mis-spells, decently works too!
        'artist': userInput_artist
    })

    # [default] to show both last.fm and YouTube urls
    if onlyYOUTUBE == 0:
        for index_sa in range(0, ARTIST_LIMIT):
            # capture artist name
            response_name_display = request_sa.json()['similarartists']['artist'][index_sa]['name']

            # build out array -- artist name
            similar_artist_array.append(response_name_display)

            # build out dictionary
            results_dict[response_name_display] = {'last.fm_urls': [], 'YouTube_urls': []}
            results_dict[response_name_display]['last.fm_urls'] = [get_topTracksLASTFM(response_name_display)]
            current_lastFM_urls = results_dict[response_name_display]['last.fm_urls']
            results_dict[response_name_display]['YouTube_urls'] = [get_topTracksYOUTUBE(current_lastFM_urls)]

    # show only YouTube links in results dictionary
    if onlyYOUTUBE == 1:
        lastFM_urls_dict = {}
        for index_sa in range(0, ARTIST_LIMIT):
            # capture artist name
            response_name_display = request_sa.json()['similarartists']['artist'][index_sa]['name']

            # build out array -- artist name
            similar_artist_array.append(response_name_display)

            # build out dictionaries, lastFM_urls_dict needed for function parsing, not want to make another function
            results_dict[response_name_display] = {'YouTube_urls': []}
            lastFM_urls_dict[response_name_display] = [get_topTracksLASTFM(response_name_display)]
            current_lastFM_urls = lastFM_urls_dict[response_name_display]
            results_dict[response_name_display]['YouTube_urls'] = [get_topTracksYOUTUBE(current_lastFM_urls)]

    print(userInput_artist)
    print("similar_artist_array ::")
    print(similar_artist_array)
    print("\n==============================\n")
    print("last.fm urls and YouTube urls to explore ::")
    jprint(results_dict)

    return results_dict

def get_topTracksYOUTUBE(current_lastFM_urls):
    top_tracks_array = []

    # needed to go two layers deep to reach each url
    for item in current_lastFM_urls:
        for lastFM_urls in item:
            request = requests.get(lastFM_urls)

            target = SoupStrainer(('a', {'class': 'play-this-track-playlink--youtube'}))
            soup = BeautifulSoup(request.text, 'html.parser', parse_only=target)

            #soup = BeautifulSoup(request.text, 'html.parser')
            # go through all links that are YouTube play
            for link in soup.find_all("a", class_="play-this-track-playlink--youtube"):
                found_url = link.get('href')
                if "youtube.com/watch?v=" in str(found_url):
                    # not to copy duplicates
                    if str(found_url) not in top_tracks_array:
                        top_tracks_array.append(found_url)

    return top_tracks_array

def get_topTracksLASTFM(response_name_display):
    top_tracks_array = []

    for index in range(0, TOP_TRACKS_LIMIT):
        # build out payload -- urls
        request_tt = lastfm_getData({
            'method': 'artist.getTopTracks',
            'limit': TOP_TRACKS_LIMIT,
            'page': 1,
            'autocorrect': 1,                        # allows for mis-spells, decently works too!
            'artist': response_name_display
        })
        # capture TOP_TRACKS_LIMIT amount of urls
        response_url_display = request_tt.json()['toptracks']['track'][index]['url']

        # build out array
        top_tracks_array.append(response_url_display)

    return top_tracks_array

def check_connections():
    # check connection set up -- expect '200'
    r = lastfm_getData({
        'method': 'artist.getSimilar',
        'limit': ARTIST_LIMIT,
        'autocorrect': 1,  # allows for mis-spells, decently works too!
        'artist': 'Cher'
    })

    return r.status_code

def main():
    print("status :: " + str(check_connections()))

    user_artist = input('Please enter an artist // ')
    youtube_flag = input('Would you only like to see youtube links? [\'0\' -- false || \'1\' -- true] // ')
    print("\n==============================\n")

    get_similarArtists(user_artist, int(youtube_flag))

if __name__ == "__main__":
    main()
