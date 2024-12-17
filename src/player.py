class Player:
    def __init__(self):
        self.name = ""
        self.score = 0

    def serialise(self) -> dict:
        return {"name": self.name, "score": self.score}

    def parse(self, data):
        self.name = data["name"]
        self.score = data["score"]
