import urllib.request as req
import json

competion_id = 433
base_link = 'http://api.football-data.org/v1/'
competion_url = base_link + 'competitions/' + str(competion_id) + '/'
f = req.urlopen(competion_url + 'leagueTable')
json_str = f.read().decode('utf-8')
standings = json.loads(json_str)

for standing in standings['standing']:
    print(standing['teamName'] +
          ((40 - len(standing['teamName'])) * ' ' +
           str(standing['points'])))

print("\n\nGames to go:")
games_str = req.urlopen(competion_url + 'fixtures').read().decode('utf-8')
games = json.loads(games_str)['fixtures']
for game in games:
    if game['status'] == 'TIMED' or game['status'] == 'SCHEDULED':
        print(game['homeTeamName'] + " - " + game['awayTeamName'])
