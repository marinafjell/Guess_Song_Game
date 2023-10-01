import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from random import seed
from random import shuffle
import webbrowser
import requests

os.environ['SPOTIPY_CLIENT_ID'] = 'SPOTIPY_CLIENT_ID'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'SPOTIPY_CLIENT_SECRET'
os.environ['SPOTIPY_REDIRECT_URI'] = 'SPOTIPY_REDIRECT_URI'

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

print('Welcome to the "Guess Song" game! In this game you need to listen to a 30-second song preview and '
      'guess the name of the song and/or artist/band.')
print('If you get both right - artist and title you get 2 points. '
      'If you get only one of them right you get 1 point and 0 if you get none.')
print('The winner is the person who gets the highest score.')

while True:
    try:
        players_num = int(input('How many players will be playing? '))
        if players_num > 0:
            break
    except ValueError:
        print('Enter number more than 0')
        pass

players_names = []
for player in range(players_num):
    name = input('Enter the name of the player #' + str(player + 1) + ': ')
    players_names.append(name)

print(
    "If you want to play with your playlist, enter the playlist's URL (it should be PUBLIC) "
    "(for example - https://open.spotify.com/playlist/37i9dQZF1E4lycTEBBywvE?si=653ab38e95494bb3) ")
pl_choice = input("or enter '1' to continue ")
if pl_choice == '1':
    print("Enter the country's code: 'US' - USA, 'DE' - Germany, 'CZ' - Czech Republic, 'AU' - Australia. "
          "Or any other country:'AD', 'AR', 'AT', 'BE', 'BO', 'BR', 'BG', 'CA', 'CL', 'CO', 'CR'")
    print("'CY', 'DK', 'DO', 'EC', 'SV', 'EE', 'FI', 'FR', 'DE', 'GR', 'GT', 'HN', 'HK', "
          "'HU', 'IS', 'ID', 'IE', 'IT', 'JP', 'LV', 'LI', 'LT', 'LU', 'MY', 'MT', 'MX'")
    country = input("'MC', 'NL', 'NZ', 'NI', 'NO', 'PA', 'PY', 'PE', 'PH', 'PL', 'PT', 'SG', 'ES', "
                    "'SK', 'SE', 'CH', 'TW', 'TR', 'GB', 'US', 'UY' ")
    while True:
        try:
            category = sp.categories(country=country, limit=50)
            break
        except:
            country = input("Enter the country's code: ")
            pass

    print('Here are categories:')

    cat_count = 0
    spotify_categories = []
    for i in category['categories']['items']:
        cat_count += 1
        cat_nameid = []
        print(cat_count, i['name'])
        cat_nameid.append(i['name'])
        cat_nameid.append(i['id'])
        spotify_categories += [cat_nameid]
    print("------------------")

    while True:
        try:
            cat_choice = int(input('Enter the number of the chosen category: '))
            break
        except ValueError:
            pass

    cat_playlists = sp.category_playlists(spotify_categories[cat_count - 1][-1], country=country, limit=50)

    pl_count = 0
    playlists = []
    for i in cat_playlists['playlists']['items']:
        pl_count += 1
        pl_nameid = []
        print(pl_count, i['name'])
        pl_nameid.append(i['name'])
        pl_nameid.append(i['id'])
        playlists += [pl_nameid]
    print("------------------")


    while True:
        try:
            pl_num = int(input('Enter the number of the chosen playlist: '))
            break
        except ValueError:
            pass
    results = sp.playlist_items(playlists[pl_num - 1][-1], market=country)

else:
    while True:
        try:
            results = sp.playlist_items(pl_choice)
            break
        except:
            pl_choice = input('Enter the link to a PUBLIC playlist: ')
            pass


print('Please wait for songs to load...')

track = []
all_tracks = []
i = 0
for item in results['items']:
    if item['track'] is not None:
        url = item['track']['preview_url']
        if item['track']['preview_url'] is not None:
            i += 1
            page = requests.head(url)
            if page.status_code == 404:
                continue
            track = [i, item['track']['artists'][0]['name']]

            if len(item['track']['artists']) > 1:
                for j in item['track']['artists'][1:]:
                    track.append(j['name'])
            track.append(item['track']['name'])
            track.append(item['track']['preview_url'])
            all_tracks += [track]

seed(1)
shuffle(all_tracks)
scores = [0] * len(players_names)
count = 0
how_many_tracks = len(all_tracks)
if players_num > 1:
    how_many_tracks = (len(all_tracks) // len(players_names)) * len(players_names)
for i in all_tracks[:how_many_tracks]:
    if count == len(players_names):
        count = 0
    if input(players_names[count] + ", press 'enter' when you're ready or 'x' to finish the game ") == 'x':
        break
    for _ in players_names:
        song_name = ', '.join(i[1:-2])
        song_title = i[-2]
        webbrowser.open(i[-1])
        n = input("Do you know this song? (1 - Yes / Not sure, 2 - No): ")
        while n != "1" and n != "2":
            n = input("Do you know this song? (1 - Yes / Not sure, 2 - No): ")
        if n == '1':
            answer = input(
                'Did you say ' + song_name + ' - ' + song_title + "? (1 - Only song's artist, "
                                                                  "2 - Only song's title, 3 - Both, 4 - None): ")
            while answer != "1" and answer != "2" and answer != '3' and answer != '4':
                answer = input(
                    'Did you say ' + song_name + ' - ' + song_title + "? (1 - Only song's artist, "
                                                                      "2 - Only song's title, 3 - Both, 4 - None): ")
            if answer == '1' or answer == '2':
                scores[count] += 1
            elif answer == '3':
                scores[count] += 2
        elif n == '2':
            print('It was ' + song_name + ' - ' + song_title)

        count += 1
        break

print('Here are results:')
for i, j in zip(players_names, scores):
    print(i + ', you earned ' + str(j) + ' point(s)')
