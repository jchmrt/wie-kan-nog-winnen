class MaxPoints:
    def __init__(self):
        self.team_points = []

    def calculate_max_points(self, team_info_list):
        for team_info in team_info_list:
            max_points = team_info.points + 3 * team_info.games_left
            self.team_points.append(team_info.team_name, max_points)

    def get_team_max_points(self, team_name):
        for (list_team_name, max_points) in self.team_points:
            if list_team_name = team_name:
                return max_points

    def deduct_points_from_team(self, team_name, points_to_deduct):
        for i in range(0, len(self.team_points)):
            if self.team_points[i][0] == team_name:
                self.team_points[i][1] -= points_to_deduct
                return


class TeamInfo:
    def __init__(self, team_name, points, games_left):
        self.team_name = team_name
        self.points = points
        self.games_left = games_left
