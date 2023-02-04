import random
from player import Player


class Bot(Player):

    def choose_target(self):
        targettable_players = [player for player in self.game.players if player.is_targettable()]
        if not targettable_players: return None

        target = random.choice(targettable_players)

        return target

    def choose_card_from(self, target):
        if not target.hand: return None

        target_card = random.choice(target.hand)

        return target_card

    def choose_building(self):
        players_with_buildings = [player for player in self.game.players if player.buildings]
        if not players_with_buildings: return None, None
        
        target = random.choice(players_with_buildings)
        target_building = random.choice(target.buildings)

        return target, target_building

    def choose_defend(self):
        return random.randint(0, 1)

    def block_with_fort(self):
        fort = self._fort()
        if not fort: return None

        use_fort = random.randint(0, 1)
        if use_fort:
            return fort
        else:
            return None

    def play_turn(self):
        i = 0
        while True:
            if self.is_dead(): return
            if not len(self.hand): return

            card = self.hand[i]
            if random.randint(0, 1):
                status_code, status_description = card.use(self)
                if self.game.log: print(status_description)

                if card.name == "Heist" and status_code == 0:
                    i = 0
                    continue

                if status_code == 1:
                    i += 1

            if i >= len(self.hand):
                return
