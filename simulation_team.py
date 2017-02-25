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
        return points + max_future_points
