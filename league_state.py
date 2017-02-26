import copy


class LeagueState:
    def __init__(self, schedule, simulation_teams, highest_place = 1):
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
