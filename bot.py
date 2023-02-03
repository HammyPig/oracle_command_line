import random
from player import Player


class Bot(Player):

    def _choose_target(self):
        while True:
            target_i = random.randrange(0, len(Bot.game.players))
            target = Player.game.players[target_i]

            if target.is_targettable():
                return target

    def play_turn(self):
        for i in range(len(self.hand)):
            if random.randint(0, 1):
                self.play_card(i)
