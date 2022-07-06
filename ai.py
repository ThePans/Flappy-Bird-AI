from game import Game

class Agent:
    def __init__(self):
        pass
    def get_state(self, game):
        y, y_change = game.ys()
        pillar = game.close_pillar()
        pillars = pillar.rects()
        ty, by = pillars[3], pillars[4]
        return y, y_change, ty, by
    def action(self, game):
        y, y_change, ty, by = self.get_state(game)
        point = sum([ty, by]) / len([ty, by])
        y = y + 60
        if y >= by + 30:
            return 1
        else:
            return 0

game = Game()

agent = Agent()
while True:
    game.play_frame(agent.action(game))