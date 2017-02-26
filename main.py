import urllib.request as req
import json
import simulation_team
import schedule as s
import highest_place_finder
import league_state
from key import API_KEY


class StatsUpdater:
    def __init__(self, competition_id, api_key):
        self.competition_id = competition_id
        self.api_key = api_key

    def retrieve_current_competition_state(self):
        base_url = 'http://api.football-data.org/v1/'
        competition_url = (base_url + 'competitions/' +
                           str(self.competition_id) + '/')
        standings_url = competition_url + 'leagueTable'
        schedule_url = competition_url + 'fixtures'

        self.standings_data = self.load_json_from_url(standings_url)
        self.schedule_data = self.load_json_from_url(schedule_url)

        self.get_logo_urls();

    def load_json_from_url(self, url):
        json_request = req.Request(url, headers={'X-Auth-Token': self.api_key})
        json_file = req.urlopen(json_request)
        json_str = json_file.read().decode('utf-8')
        return json.loads(json_str)

    def get_logo_urls(self):
        self.logo_urls = {}

        for team in self.standings_data['standing']:
            # Because of a bug in the dataset we use, the url for the logo of
            # AZ Alkmaar is not valid. As a temporary fix, we insert our own
            # correct url here.
            if team['teamName'] == 'AZ Alkmaar':
                self.logo_urls['AZ Alkmaar'] = 'https://upload.wikimedia' +\
                                '.org/wikipedia/commons/e/e0/AZ_Alkmaar.svg'
            else:
                self.logo_urls[team['teamName']] = team['crestURI']

    def calculate_stats(self):
        simulation_teams = self.create_simulation_teams()
        schedule = self.create_schedule()

        state = league_state.LeagueState(schedule, simulation_teams)
        finder = highest_place_finder.HighestPlaceFinder(state)
        self.team_places = []

        for team in simulation_teams:
            place = finder.find_highest_place(team)
            logo_url = self.logo_urls[team.team_name]
            self.team_places.append({'teamName': team.team_name,
                                     'bestPlace': place,
                                     'logoUrl': logo_url})
            print(team.team_name + ((40 - len(team.team_name)) * ' ') +
                  str(place))

    def create_simulation_teams(self):
        teams_data = self.standings_data['standing']
        simulation_teams = []

        for team_data in teams_data:
            simulation_teams.append(
                simulation_team.SimulationTeam(team_data['teamName'],
                                               team_data['points']))

        return simulation_teams

    def create_schedule(self):
        games_data = self.schedule_data['fixtures']
        schedule = s.Schedule()

        for game_data in games_data:
            if game_data['status'] == 'TIMED' or (game_data['status'] ==
                                                  'SCHEDULED'):
                schedule.add_game(game_data['homeTeamName'],
                                  game_data['awayTeamName'])

        return schedule

    def save_stats(self):
        with open('site/stats.json', 'w') as stats_file:
            json.dump(self.team_places, stats_file)

    def update_stats(self):
        self.retrieve_current_competition_state()
        self.calculate_stats()
        self.save_stats()


competition_id = 433            # Eredivisie

stats_updater = StatsUpdater(competition_id, API_KEY)
stats_updater.update_stats()
