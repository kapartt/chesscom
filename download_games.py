#!/usr/bin/python3
import json
import urllib.request
import os
import datetime


def check_first_year(s):
    cnt = len(s)
    for x in s:
        if '0' <= x <= '9':
            cnt -= 1
    return cnt == 0 and 2011 <= int(s) <= datetime.datetime.now().year


def download_and_write(NICKNAME, FIRST_YEAR):
    datenow = datetime.datetime.now()
    VARIANT = 'chess'

    last_year = datenow.year
    last_month = datenow.month

    pgn_dir = '{0}.pgn'.format(NICKNAME)

    if os.path.lexists(pgn_dir):
        pgn_dir = '{0}_new.pgn'.format(NICKNAME)

    pgn_file = open(pgn_dir, 'wb')
    not_found = False

    for year in range(FIRST_YEAR, last_year + 1):
        if not_found:
            break
        for month in range(1, 13):
            if year == last_year and month > last_month or not_found:
                break

            if month < 10:
                url = 'https://api.chess.com/pub/player/{0}/games/{1}/0{2}'.format(NICKNAME, year, month)
            else:
                url = 'https://api.chess.com/pub/player/{0}/games/{1}/{2}'.format(NICKNAME, year, month)

            temp_dir = '{0}_{1}_{2}.json'.format(NICKNAME, month, year)

            f = open(temp_dir, 'wb')
            try:
                with urllib.request.urlopen(url) as response:
                    s = response.read()
                    f.write(s)
            except:
                print('User {0} not found.'.format(NICKNAME))
                f.close()
                os.remove(temp_dir)
                not_found = True
                break
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


print("Greetings from vk.com/chessclubfenix")
cmd_nickname = '\nEnter chess.com nickname:'
cmd_first_year = 'First year (from 2011 to {0}):'.format(datetime.datetime.now().year)
cmd_continue = '\nDo you want to continue with another nickname? (y/n)'

while True:
    print(cmd_nickname)
    NICKNAME = input()

    print(cmd_first_year)
    FIRST_YEAR = input()

    while not check_first_year(FIRST_YEAR):
        print('Incorrect!', cmd_first_year)
        FIRST_YEAR = input()
    FIRST_YEAR = int(FIRST_YEAR)

    download_and_write(NICKNAME, FIRST_YEAR)

    print(cmd_continue)
    ans = input()
    if not (ans == 'y' or ans == 'Y'):
        break
