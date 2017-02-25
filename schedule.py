class Schedule:
    def __init__(self):
        self.games = []

    def add_game(self, team_1, team_2):
        self.games.append((team_1, team_2))

    def get_games_with(self, team):
        games_with = []

        for game in self.games:
            if team in game:
                games_with.append(game)

        return games_with
