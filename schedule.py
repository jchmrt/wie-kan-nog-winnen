class Schedule:
    def __init__(self):
        self.games = []

    def add_game(self, team_1, team_2):
        self.games.push((team_1, team_2))

    def find_opponents(self, team):
        opponents = []

        for (team_1, team_2) in self.games:
            if team_1 == team:
                opponents.push(team_2)
            else if team_2 == team:
                opponents.push(team_1)

        return opponents
