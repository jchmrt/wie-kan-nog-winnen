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

import copy


class Schedule:
    def __init__(self):
        self.games = []

    def add_game(self, team_1, team_2):
        self.games.append((team_1, team_2))

    def get_games_with(self, team):
        games_with = []

        for game in self.games:
            if team in game:
                games_with.append(game)

        return games_with

    def remove_game(self, game):
        self.games.remove(game)

    def to_string(self):
        s = ''
        for game in self.games:
            s += game[0] + ' - ' + game[1] + '\n'
        return s

    def copy(self):
        s = Schedule()
        for game in self.games:
            s.games.append((copy.copy(game[0]), copy.copy(game[1])))
        return s
