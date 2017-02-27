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


class SimulationTeam:
    # A SimulationTeam represents a Team in a simulation. It stores
    # the team name (to identify the team) and the current score the
    # team has in the simulation.

    def __init__(self, team_name, points):
        self.team_name = team_name
        self.points = points

    def win_game(self):
        self.points += 3

    def tie_game(self):
        self.points += 1

    def get_max_points(self, schedule):
        """Returns the maximum attainable points this team can still
        win with this Schedule."""
        future_games = schedule.get_games_with(self.team_name)
        max_future_points = len(future_games) * 3
        return self.points + max_future_points

    def copy(self):
        t = SimulationTeam(copy.copy(self.team_name), copy.copy(self.points))
        return t
