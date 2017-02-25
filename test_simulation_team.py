import unittest
import schedule as schedule_module
import simulation_team as simulation_team_module

TEAMS = ['team1', 'fc soccer', '$$FC^%weird)\'ch"aracters',
         'FC doesnt play']
POINTS = [34, 53, 10, 32]

GAMES = [(TEAMS[0], TEAMS[1]),
         (TEAMS[0], TEAMS[2]),
         (TEAMS[1], TEAMS[2]),
         (TEAMS[2], TEAMS[0])]


class SimulationTeamTest(unittest.TestCase):
    def setUp(self):
        self.schedule = schedule_module.Schedule()
        for (team_1, team_2) in GAMES:
            self.schedule.add_game(team_1, team_2)
        self.simulation_team = simulation_team_module.SimulationTeam(
            TEAMS[0], POINTS[0])

    def test_create_simulation_team(self):
        team = simulation_team_module.SimulationTeam(
            TEAMS[1], POINTS[1])
        self.assertEquals(POINTS[1], team.points,
                          """The points should be equal to the one given
                          in the constructor.""")
        self.assertEquals(TEAMS[1], team.team_name,
                          """The name should be equal to the one given
                          in the constructor.""")

    def test_win_game(self):
        points_before = self.simulation_team.points
        self.simulation_team.win_game()
        points_after = self.simulation_team.points
        self.assertEquals(3, points_after - points_before,
                          """win_game should add 3 to the points of an
                          team""")

    def test_tie_game(self):
        points_before = self.simulation_team.points
        self.simulation_team.tie_game()
        points_after = self.simulation_team.points
        self.assertEquals(1, points_after - points_before,
                          """tie_game should add 1 to the points of an
                          team""")

    def test_get_max_points(self):
        future_games = len(self.schedule.get_games_with(
            self.simulation_team.team_name))
        expected_points = future_games * 3 + self.simulation_team.points
        self.assertEquals(expected_points,
                          self.simulation_team.get_max_points(self.schedule),
                          """The max points should be three times the
                          future games plus the current points""")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(
        SimulationTeamTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
