# imdb_last.fm_soundtrack_exploration
from a movie title, sound track artists are given to last.fm similarArtist algo to give YouTube urls, example output is found within the files.

## important note
This program will be working while in the terminal, it take a decent amount of time to process, will need to look into why, or maybe figure out how to lower the time of processing, added use of SoupStrainer, however the Youtube links gathering takes time, go get a coffee!

## Python libraries needed
requests, json, bs4, imdb

## set up -- create last.fm API account
1. Go to last.fm site and fill out information for generating an API key, [Create_API_account](https://www.last.fm/api/account/create). You don't really need to place a callback URL or an application homepage -- did not utilize features that required these things.
2. Next screen, assumed everything checked out okay by last.fm, the 'API key' and 'Shared secret' will be given.
3. Place your 'API key' within the ```prototype.py```, line begins with ``API_KEY= ''``, fill between the ' '. Place the 'Registered to' name as the ``USER_AGENT = ''``, fill between the ' '. 
4. Save, you are ready to explore!

## running
1. THIS IS STILL A WORK-IN-PROCESS-PROGRAM.
2. Navigate to your directory which will hold this repository through terminal of choice.
3. Depending on your python PATH variable set up, you could be using 'python' or 'python3', figure this out before proceeding the user could also house another variable other than these for python running more info? check out [Source 1](http://net-informations.com/python/intro/path.html) and [Source 2](https://geek-university.com/python/add-python-to-the-windows-path/). Run (prototype.py).
```  
$python imdb_soundtrack_last.fm_exploration.py
```  
--or --
```  
$python3 imdb_soundtrack_last.fm_exploration.py
```
4. You will be prompted to enter a movie name.
```
Please enter a movie name //
```
5. Program will output at max 20 choices to pick from which are similar to the given movie name (if there is not a closely related movie title to given, the program will give an error message and prompt the user to enter a movie title again).
6. You will be prompted to enter a choice number.
```
Enter CHOICE # as multiple movies with this title have been found //
```
7. Program will present the user with an imdb link to soundtrack listsing and an array of the soundtrack artists (duplicates will not be within this array).
8. Processing with the prototype.py functions will begin for each artist.
9. The program will output for each of the artsist within the soudtrack listing:
    - array of similar artists (current limit is 20 artists)
    - dictionary of YouTube urls of top tracks per similar artist (current limit is 5 tracks)

## sources
- https://imdbpy.readthedocs.io/en/latest/usage/data-interface.html
- https://buildmedia.readthedocs.org/media/pdf/imdbpy/latest/imdbpy.pdf
