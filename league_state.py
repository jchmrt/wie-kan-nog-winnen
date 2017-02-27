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


class LeagueState:
    def __init__(self, schedule, simulation_teams, highest_place=1):
        self.schedule = schedule
        self.simulation_teams = simulation_teams
        # Stores the highest place the team can win in this state,
        # used for premature exits
        self.highest_place = highest_place

    def copy(self):
        simulation_teams_copy = []
        for team in self.simulation_teams:
            simulation_teams_copy.append(team.copy())
        l = LeagueState(self.schedule.copy(), simulation_teams_copy,
                        copy.copy(self.highest_place))
        return l

    def find_simulation_team(self, team_name):
        for team in self.simulation_teams:
            if team.team_name == team_name:
                return team
