class HighestPlaceFinder:
    def __init__(self, league_state):
        self.league_state = league_state

    def find_highest_place(self, simulation_team):
        my_team = simulation_team.copy()
        self.current_state = self.league_state.copy()

        my_max_points = my_team.get_max_points(self.current_state.schedule)

        self.win_games(my_team)

        found = True
        while found:
            found = False
            for team in self.current_state.simulation_teams:
                ammount_of_games_with =\
                    len(self.current_state.schedule.
                        get_games_with(team.team_name))
                if (team.get_max_points(self.current_state.schedule) <=
                    my_max_points)\
                   and (ammount_of_games_with > 0):
                    self.win_games(team)
                    found = True

        # TODO: Add bruteforce part

        place = 1
        for team in self.current_state.simulation_teams:
            if team.get_max_points(self.current_state.schedule) >\
               my_max_points:
                place += 1

        return place

    def win_games(self, team):
        games_with = self.current_state.schedule.get_games_with(team.team_name)

        for game in games_with:
            team.win_game()
            self.current_state.schedule.remove_game(game)
