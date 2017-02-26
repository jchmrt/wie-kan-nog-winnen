class HighestPlaceFinder:
    def __init__(self, league_state):
        self.league_state = league_state

    def find_highest_place(self, simulation_team):
        my_team = simulation_team.copy()
        self.current_state = self.league_state.copy()
        self.my_max_points = my_team.get_max_points(self.current_state.schedule)

        self.win_games(my_team)

        # This stores an upper limit of the highest place we can
        # attain, if we attain this place, we can stop the search and
        # return this
        self.highest_place = 1

        # This part lets all the teams that we are sure we can't surpass anymore
        # win everything.
        for team in self.current_state.simulation_teams:
            if team.points > self.my_max_points:
                self.win_games(team)
                # We can't pass this team, so we necessarily end a
                # place lower.
                self.highest_place += 1

        # This part lets all the teams who can't win pass our team in the
        # rankings anymore (when we play perfectly) win from everyone who is
        # left.
        found = True
        while found:
            found = False
            for team in self.current_state.simulation_teams:
                ammount_of_games_with =\
                    len(self.current_state.schedule.
                        get_games_with(team.team_name))
                if (team.get_max_points(self.current_state.schedule) <=
                    self.my_max_points)\
                   and (ammount_of_games_with > 0):
                    self.win_games(team)
                    found = True

        return self.find_best_place_from(self.current_state)

    def win_games(self, team):
        games_with = self.current_state.schedule.get_games_with(team.team_name)

        for game in games_with:
            team.win_game()
            self.current_state.schedule.remove_game(game)

    def find_best_place_from(self, state):
        if not state.schedule.games\
           or self.get_place(state) == self.highest_place:
            return self.get_place(state)

        game = state.schedule.games[0]
        state.schedule.games.remove(game)

        state_win_home = state.copy()
        state_win_home.find_simulation_team(game[0]).win_game()
        best_place_win_home = self.find_best_place_from(state_win_home)

        state_tie = state.copy()
        state_tie.find_simulation_team(game[0]).tie_game()
        state_tie.find_simulation_team(game[1]).tie_game()
        best_place_tie = self.find_best_place_from(state_tie)

        state_win_away = state.copy()
        state_win_away.find_simulation_team(game[1]).win_game()
        best_place_win_away = self.find_best_place_from(state_win_away)

        return min([best_place_win_home,
                    best_place_tie,
                    best_place_win_away])

    def get_place(self, state):
        place = 1
        for team in state.simulation_teams:
            if team.get_max_points(state.schedule) > self.my_max_points:
                place += 1
        return place
