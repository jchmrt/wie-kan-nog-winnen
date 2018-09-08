# Wie kan nog winnen is a collection of utilities to calculate and
# display what places teams of the Eredivisie can reach if everything
# goes perfectly.
# Copyright (C) 2017  Jochem Raat
# Copyright (C) 2017  Marien Raat

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import urllib.request as req
import json
import simulation_team
import schedule as s
import highest_place_finder
import lowest_place_finder
import league_state
from key import API_KEY


class StatsUpdater:
    def __init__(self, competition_id, api_key):
        self.competition_id = competition_id
        self.api_key = api_key

    def retrieve_current_competition_state(self):
        base_url = 'http://api.football-data.org/v2/'
        competition_url = (base_url + 'competitions/' +
                           str(self.competition_id) + '/')
        standings_url = competition_url + 'standings'
        schedule_url = competition_url + 'matches'
        teams_url = competition_url + 'teams'

        self.standings_data = self.load_standings_data(standings_url)
        self.schedule_data = self.load_json_from_url(schedule_url)
        self.teams_data = self.load_json_from_url(teams_url)

        self.get_logo_urls()

    def load_standings_data(self, standings_url):
        raw_data = self.load_json_from_url(standings_url)
        all_standings = raw_data['standings']

        for standing in all_standings:
            if standing['type'] == 'TOTAL':
                return standing['table']

        raise ValueError('No TOTAL standings table found')

    def load_json_from_url(self, url):
        json_request = req.Request(url, headers={'X-Auth-Token': self.api_key})
        json_file = req.urlopen(json_request)
        json_str = json_file.read().decode('utf-8')
        return json.loads(json_str)

    def get_logo_urls(self):
        self.logo_urls = {}

        for team in self.teams_data['teams']:
            # Because of a bug in the dataset we use, the url for the logo of
            # VVV Venlo is not valid. As a temporary fix, we insert our own
            # correct url here.
            if team['name'] == 'VVV Venlo':
                self.logo_urls[team['name']] = 'https://upload.wikimedia.org/' +\
                                'wikipedia/en/6/60/VVV-Venlo_logo.svg'
            elif team['name'] == 'VBV De Graafschap':
                self.logo_urls[team['name']] = 'https://upload.wikimedia.org/' +\
                                'wikipedia/commons/2/28/VBV_De_Graafschap_Doetinchem.svg'
            elif team['name'] == 'FC Emmen':
                self.logo_urls[team['name']] = 'https://upload.wikimedia.org/' +\
                                'wikipedia/en/8/83/FC_Emmen_logo.svg'
            elif team['name'] == 'Fortuna Sittard':
                self.logo_urls[team['name']] = 'https://upload.wikimedia.org/' +\
                                'wikipedia/en/2/2d/Fortuna_Sittard_logo.svg'
            elif team['name'] == 'AZ':
                self.logo_urls[team['name']] = 'https://upload.wikimedia.org/' +\
                                'wikipedia/commons/e/e0/AZ_Alkmaar.svg'
            elif team['name'] == 'NAC Breda':
                self.logo_urls[team['name']] = 'https://upload.wikimedia.org/' +\
                                'wikipedia/commons/c/c9/Logo_NAC_Breda.png'
            elif team['name'] == 'ADO Den Haag':
                self.logo_urls[team['name']] = 'https://upload.wikimedia.org/' +\
                                'wikipedia/en/a/ad/ADO_Den_Haag_logo.svg'
            else:
                self.logo_urls[team['name']] = team['crestUrl']

            # Replace all http URLs with https:
            # if self.logo_urls[team['name']][:4] == 'http' and\
            #    self.logo_urls[team['name']][:5] != 'https':
            #     self.logo_urls[team['name']] =\
            #         ('https' +
            #          self.logo_urls[team['name']][4:])

    def calculate_stats(self):
        simulation_teams = self.create_simulation_teams()
        schedule = self.create_schedule()

        state = league_state.LeagueState(schedule, simulation_teams)
        low_finder = lowest_place_finder.LowestPlaceFinder(state.copy())
        high_finder = highest_place_finder.HighestPlaceFinder(state.copy())
        self.team_places = []

        for team in simulation_teams:
            highest_place = high_finder.find_highest_place(team)
            lowest_place = low_finder.find_lowest_place(team)
            logo_url = self.logo_urls[team.team_name]
            self.team_places.append({'teamName': team.team_name,
                                     'bestPlace': highest_place,
                                     'worstPlace': lowest_place,
                                     'currentPlace': team.current_place,
                                     'logoUrl': logo_url})
            print(str(team.current_place) + ": " +
                  ((4 - len(str(team.current_place))) * ' ') +
                  team.team_name + ((40 - len(team.team_name)) * ' ') +
                  str(highest_place) + ' - ' + str(lowest_place))

    def create_simulation_teams(self):
        simulation_teams = []

        for standing in self.standings_data:
            simulation_teams.append(
                simulation_team.SimulationTeam(standing['team']['name'],
                                               standing['points'],
                                               standing['position']))

        return simulation_teams

    def create_schedule(self):
        games_data = self.schedule_data['matches']
        schedule = s.Schedule()

        for game_data in games_data:
            if game_data['status'] != 'FINISHED':
                schedule.add_game(game_data['homeTeam']['name'],
                                  game_data['awayTeam']['name'])

        return schedule

    def save_stats(self):
        with open('site/stats.json', 'w') as stats_file:
            json.dump(self.team_places, stats_file)

    def update_stats(self):
        self.retrieve_current_competition_state()
        self.calculate_stats()
        self.save_stats()


competition_id = 2003            # Eredivisie

stats_updater = StatsUpdater(competition_id, API_KEY)
stats_updater.update_stats()
