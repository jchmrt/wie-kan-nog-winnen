import urllib.request as req
import json

competion_id = 433
base_link = 'http://api.football-data.org/v1/'
f = req.urlopen(base_link + 'competitions/' + str(competion_id) + '/leagueTable')
json_str = f.read().decode('utf-8')
standings = json.loads(json_str)


for standing in standings['standing']:
    print(standing["teamName"]
          + ((40 - len(standing['teamName'])) * ' '
             + str(standing['points'])))

