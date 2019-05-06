#!/usr/bin/python3
import json
import urllib.request
import os

NICKNAME = 'Chess_fenix'
CURRENT_DATE = '06052019'
VARIANT = 'chess'
FIRST_YEAR = 2014

last_year = int(CURRENT_DATE) % 10000
last_month = (int(CURRENT_DATE) // 10000) % 100

pgn_dir = '{0}.pgn'.format(NICKNAME)
pgi_dir = '{0}.pgi'.format(NICKNAME)
ini_dir = '{0}.ini'.format(NICKNAME)

if os.path.lexists(pgn_dir):
    os.remove(pgn_dir)

if os.path.lexists(pgi_dir):
    os.remove(pgi_dir)

if os.path.lexists(ini_dir):
    os.remove(ini_dir)

pgn_file = open(pgn_dir, 'wb')

for year in range(FIRST_YEAR, last_year + 1):
    for month in range(1, 13):
        if year == last_year and month > last_month:
            break

        if month < 10:
            url = 'https://api.chess.com/pub/player/{0}/games/{1}/0{2}'.format(NICKNAME, year, month)
        else:
            url = 'https://api.chess.com/pub/player/{0}/games/{1}/{2}'.format(NICKNAME, year, month)

        temp_dir = '{0}_{1}_{2}.json'.format(NICKNAME, month, year)

        f = open(temp_dir, 'wb')
        with urllib.request.urlopen(url) as response:
            s = response.read()
            f.write(s)
        f.close()

        f = open(temp_dir, 'r')
        d = json.loads(f.read())
        f.close()

        list_games = d['games']
        print('{0}.{1} Found games: {2}'.format(month, year, len(list_games)))

        for game in list_games:
            if game['rules'] == VARIANT:
                pgn_file.write(game['pgn'].encode('utf-8'))
                pgn_file.write("\n\n".encode('utf-8'))

        os.remove(temp_dir)

pgn_file.close()
