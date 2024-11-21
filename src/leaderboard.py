import json
from src.player import Player


class Leaderboard:

    def __init__(self):
        self.num_scores = 0
        self.scores = []  # scores are formatted as [["name", score]]
        self.readScores()

    def readScores(self):
        with open("src/leaderboard.json", "r") as leaderboard_file:
            self.scores = json.load(leaderboard_file)
            self.num_scores = len(self.scores)

    def writeScores(self):

        self.sortScores()  # sort them

        with open("src/leaderboard.json", "w") as leaderboard_file:
            json.dump(self.scores, leaderboard_file)

    def sortScores(self):
        self.scores = sorted(self.scores, key=lambda x: x[1], reverse=True)

    def get_high_score(self):
        return self.scores[0][1]

    def add_new_score(self, player: Player):
        name = player.name
        score = player.score
        self.scores.append([name, score])
        self.sortScores()
        self.writeScores()
