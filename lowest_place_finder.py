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

class LowestPlaceFinder:
    def __init__(self, league_state):
        self.league_state = league_state

    def find_lowest_place(self, simulation_team):
        my_team = simulation_team.copy()
        current_state = self.league_state.copy()
        self.my_min_points = my_team.points

        self.lose_games(my_team, current_state)


        return self.find_lowest_place_from(current_state)

    def find_lowest_place_from(self, state):
        self.eliminate_games_with_heuristics(state)

        if not state.schedule.games\
           or self.get_place(state) == state.lowest_place:
            return self.get_place(state)

        game = state.schedule.games[0]
        state.schedule.games.remove(game)

        state_win_home = state.copy()
        state_win_home.find_simulation_team(game[0]).win_game()
        best_place_win_home = self.find_lowest_place_from(state_win_home)

        state_tie = state.copy()
        state_tie.find_simulation_team(game[0]).tie_game()
        state_tie.find_simulation_team(game[1]).tie_game()
        best_place_tie = self.find_lowest_place_from(state_tie)

        state_win_away = state.copy()
        state_win_away.find_simulation_team(game[1]).win_game()
        best_place_win_away = self.find_lowest_place_from(state_win_away)

        return max([best_place_win_home,
                    best_place_tie,
                    best_place_win_away])

    def eliminate_games_with_heuristics(self, state):
        self.let_unpassable_teams_lose(state)
        self.let_higher_teams_lose(state)

    def let_unpassable_teams_lose(self, state):
        # This part lets all the teams that we are sure we can't
        # be passed by anymore lose everything.
        for team in state.simulation_teams:
            if team.get_max_points(state.schedule) < self.my_min_points:
                self.lose_games(team, state)
                # We can't pass this team, so we necessarily end a
                # place higher.
                state.lowest_place -= 1

    def let_higher_teams_lose(self, state):
        # This part lets all the teams who already have more points
        # than us lose, since we won't pass them anymore anyway.
        for team in state.simulation_teams:
            if team.points > self.my_min_points:
                self.lose_games(team, state)

    def lose_games(self, team, state):
        games_with = state.schedule.get_games_with(team.team_name)

        for game in games_with:
            if game[0] == team.team_name:
                state.find_simulation_team(game[1]).win_game()
            else:
                state.find_simulation_team(game[0]).win_game()
            state.schedule.remove_game(game)

    def get_place(self, state):
        place = 18
        for team in state.simulation_teams:
            if team.points < self.my_min_points:
                place -= 1
        return place
