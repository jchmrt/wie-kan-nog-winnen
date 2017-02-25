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


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ScheduleTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
