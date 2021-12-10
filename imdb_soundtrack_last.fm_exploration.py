import prototype
import requests
from imdb import IMDb
from bs4 import BeautifulSoup, SoupStrainer

def get_soundtrackIMDB(confirmed_movieID):
    soundtrack_artist_array = []

    imdb_soundtrackURL = "https://m.imdb.com/title/tt" + str(confirmed_movieID) + "/soundtrack/"
    print("IMDB soundtrack url ::")
    print(imdb_soundtrackURL + "\n")
    request = requests.get(imdb_soundtrackURL)

    target = SoupStrainer(('ul', {'class': 'ipl-content-list'}))
    soup = BeautifulSoup(request.text, 'html.parser', parse_only=target)

    # go through song listings
    for list in soup.find_all("ul", class_="ipl-content-list"):
        for item in list:
            flag = 0
            for line in item:
                if flag == 1:
                    # adding the next string with flag to capture artists
                    if str(line.contents[0]) not in soundtrack_artist_array:
                        soundtrack_artist_array.append(str(line.contents[0]))
                    flag = 0
                if ("Performed by " in line) and (len(line) < 17):
                    # line before needed has been found
                    flag = 1
                elif ("Performed by " in line) and (len(line) >= 17):
                    # these are hard coded entries, get only the artist, no whitespace/other texts
                    artist = line[14:-1]
                    if str(artist) not in soundtrack_artist_array:
                        soundtrack_artist_array.append(str(artist))
                else:
                    continue
    print("soundtrack_artist_array ::")
    print(soundtrack_artist_array)
    print("\n==============================\n")
    return soundtrack_artist_array

def main():
    #print("status :: " + str(check_connections()))

    user_movie = input('Please enter a movie name // ')
    print("\n==============================\n")

    # create an instance of IMDb
    IMDB_instance = IMDb()

    # array of movieIDs associated with the search
    movieID = []

    movie_name_search = IMDB_instance.search_movie(user_movie)

    for movie_name in range(0, len(movie_name_search)):
        found_movieID = movie_name_search[movie_name].movieID
        movieID.append(found_movieID)
        found_movieInfo = IMDB_instance.get_movie(found_movieID)
        # make choices human friendly
        choice = str(movie_name + 1)
        # noted some movies within the database are "in development" the year released is not available
        try:
            movie_year = str(found_movieInfo['year'])
        except:
            movie_year = "N/A"
        movie_title = str(movie_name_search[movie_name]['title'])
        # noted some movies within the database do not have the 'directors' place set up
        try:
            movie_firstdirectorlisted = str(found_movieInfo['directors'][0]['name'])
        except:
            movie_firstdirectorlisted = "N/A"
        print("CHOICE " + choice + " :: " + movie_title + " -- " + movie_year + " -- " + movie_firstdirectorlisted)
        found_movieID = movie_name_search[movie_name].movieID
        movieID.append(found_movieID)

    print("\n==============================\n")
    if len(movieID) == 0:
        print("Movies with this title can not be found at this time, please try again. Restarting ...")
        print("\n==============================\n")
        user_movie_confirm = None
        main()
    else:
        user_movie_confirm = input('Enter CHOICE # as multiple movies with this title have been found // ')
        print("\n==============================\n")

    if user_movie_confirm != None:
        # un-normalize the index back to array
        confirmed_movieID = movieID[int(user_movie_confirm) - 1]

        # capture artists of sound track in array
        artist_array = get_soundtrackIMDB(confirmed_movieID)

        # process these with the other application, only youtube urls (why the 1 as param)
        for artist in artist_array:
            prototype.get_similarArtists(artist, 1)

    else:
        exit(0)

if __name__ == "__main__":
    main()
