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

class HighestPlaceFinder:
    def __init__(self, league_state):
        self.league_state = league_state

    def find_highest_place(self, simulation_team):
        my_team = simulation_team.copy()
        current_state = self.league_state.copy()
        self.my_max_points = my_team.get_max_points(current_state.schedule)

        self.win_games(my_team, current_state)

        return self.find_best_place_from(current_state)

    def find_best_place_from(self, state):
        self.eliminate_games_with_heuristics(state)

        if not state.schedule.games\
           or self.get_place(state) == state.highest_place:
            return self.get_place(state)

        game = state.schedule.games[0]
        state.schedule.games.remove(game)

        state_win_home = state.copy()
        state_win_home.find_simulation_team(game[0]).win_game()
        best_place_win_home = self.find_best_place_from(state_win_home)

        state_tie = state.copy()
        state_tie.find_simulation_team(game[0]).tie_game()
        state_tie.find_simulation_team(game[1]).tie_game()
        best_place_tie = self.find_best_place_from(state_tie)

        state_win_away = state.copy()
        state_win_away.find_simulation_team(game[1]).win_game()
        best_place_win_away = self.find_best_place_from(state_win_away)

        return min([best_place_win_home,
                    best_place_tie,
                    best_place_win_away])

    def eliminate_games_with_heuristics(self, state):
        self.let_unpassable_teams_win(state)
        self.let_lower_teams_win(state)

    def let_unpassable_teams_win(self, state):
        # This part lets all the teams that we are sure we can't
        # surpass anymore win everything.
        for team in state.simulation_teams:
            if team.points > self.my_max_points:
                self.win_games(team, state)
                # We can't pass this team, so we necessarily end a
                # place lower.
                state.highest_place += 1

    def let_lower_teams_win(self, state):
        # This part lets all the teams who can't pass our team in the
        # rankings anymore (when we play perfectly) win from everyone who is
        # left.
        found = True
        while found:
            found = False
            for team in state.simulation_teams:
                ammount_of_games_with =\
                    len(state.schedule.get_games_with(team.team_name))

                if team.get_max_points(state.schedule) <=\
                   self.my_max_points and (ammount_of_games_with > 0):
                    self.win_games(team, state)
                    found = True

    def win_games(self, team, state):
        games_with = state.schedule.get_games_with(team.team_name)

        for game in games_with:
            team.win_game()
            state.schedule.remove_game(game)

    def get_place(self, state):
        place = 1
        for team in state.simulation_teams:
            if team.get_max_points(state.schedule) > self.my_max_points:
                place += 1
        return place
