import urllib.request as req
import json
import simulation_team
import schedule as s
import highest_place_finder
import league_state

competion_id = 433
base_link = 'http://api.football-data.org/v1/'
competion_url = base_link + 'competitions/' + str(competion_id) + '/'
f = req.urlopen(competion_url + 'leagueTable')
json_str = f.read().decode('utf-8')
standings = json.loads(json_str)

simulation_teams = []

for standing in standings['standing']:
    simulation_teams.append(
        simulation_team.SimulationTeam(standing['teamName'],
                                       standing['points']))

games_str = req.urlopen(competion_url + 'fixtures').read().decode('utf-8')
games = json.loads(games_str)['fixtures']

schedule = s.Schedule()

for game in games:
    if game['status'] == 'TIMED' or game['status'] == 'SCHEDULED':
        schedule.add_game(game['homeTeamName'], game['awayTeamName'])

state = league_state.LeagueState(schedule, simulation_teams)
finder = highest_place_finder.HighestPlaceFinder(state)
for team in simulation_teams:
    place = finder.find_highest_place(team)
    print(team.team_name + ((40 - len(team.team_name)) * ' ') +
          str(place))
