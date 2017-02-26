class LeagueState:
    def __init__(self, schedule, simulation_teams):
        self.schedule = schedule
        self.simulation_teams = simulation_teams

    def copy(self):
        simulation_teams_copy = []
        for team in self.simulation_teams:
            simulation_teams_copy.append(team.copy())
        l = LeagueState(self.schedule.copy(), simulation_teams_copy)
        return l

    def find_simulation_team(self, team_name):
        for team in self.simulation_teams:
            if team.team_name == team_name:
                return team
