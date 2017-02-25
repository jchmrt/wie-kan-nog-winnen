import copy


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

    def remove_game(self, game):
        self.games.remove(game)

    def to_string(self):
        s = ''
        for game in self.games:
            s += game[0] + ' - ' + game[1] + '\n'
        return s

    def copy(self):
        s = Schedule()
        for game in self.games:
            s.games.append((copy.copy(game[0]), copy.copy(game[1])))
        return s
