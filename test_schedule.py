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

import unittest
import schedule as schedule_module

TEAMS = ['team1', 'fc soccer', '$$FC^%weird)\'ch"aracters',
         'FC doesnt play']

GAMES = [(TEAMS[0], TEAMS[1]),
         (TEAMS[0], TEAMS[2]),
         (TEAMS[1], TEAMS[2]),
         (TEAMS[2], TEAMS[0])]


class ScheduleTest(unittest.TestCase):
    def setUp(self):
        self.schedule = schedule_module.Schedule()
        for (team_1, team_2) in GAMES:
            self.schedule.add_game(team_1, team_2)

    def test_get_games_with_ammount(self):
        games = self.schedule.get_games_with(TEAMS[1])
        self.assertEquals(2, len(games), """There should be 2 games
        with team 1""")

    def test_get_games_with_no_games(self):
        games = self.schedule.get_games_with(TEAMS[3])
        self.assertEquals(0, len(games), """There should be no games
        with team 3""")

    def test_get_games_with_contains_with_team(self):
        for team in TEAMS:
            games_with = self.schedule.get_games_with(team)
            for game in games_with:
                self.assertIn(team, game, """The team that the games
                are with should always be in the game""")

    def test_add_game(self):
        game = (TEAMS[2], TEAMS[1])
        self.schedule.add_game(game[0], game[1])
        games_with = self.schedule.get_games_with(game[0])
        self.assertIn(game, games_with)

    def test_remove_game(self):
        self.schedule.remove_game(GAMES[2])
        self.assertNotIn(GAMES[2], self.schedule.games,
                         """The game should not be in the games
                         anymore after it has been removed""")

    def test_empty_to_string(self):
        empty_schedule = schedule_module.Schedule()
        self.assertEquals('', empty_schedule.to_string())

    def test_filled_to_string(self):
        self.assertEquals("""team1 - fc soccer
team1 - $$FC^%weird)'ch\"aracters
fc soccer - $$FC^%weird)'ch\"aracters
$$FC^%weird)'ch\"aracters - team1
""", self.schedule.to_string())

    def test_copy(self):
        copy = self.schedule.copy()
        copy.add_game(TEAMS[0], TEAMS[3])

        self.assertEquals([], self.schedule.get_games_with(TEAMS[3]))
        self.assertEquals([(TEAMS[0], TEAMS[3])],
                          copy.get_games_with(TEAMS[3]))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ScheduleTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
