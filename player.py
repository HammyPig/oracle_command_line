class Player:

    game = None

    def __init__(self, name):
        self.name = name
        self.health = 5
        self.hand = []
        self.buildings = []
        self.attack_count = 0

    def __repr__(self):
        if self.is_dead():
            return f"Player {self.name}: DEAD"

        return f"Player {self.name}, health: {self.health}, buildings: {self.buildings}, attacks: {self.attack_count}/{self._attack_limit()}, cards: {self.hand}"

    def _attack_limit(self):
        attack_limit = 1
        for building in self.buildings:
            if building.name == "Barracks":
                attack_limit += 1

        return attack_limit

    def _hand_limit(self):
        hand_limit = 5
        for building in self.buildings:
            if building.name == "Farm":
                hand_limit += 1

        return hand_limit

    def _attack_damage(self):
        attack_damage = 1
        for building in self.buildings:
            if building.name == "Spell Tower":
                attack_damage += 1

        return attack_damage

    def is_dead(self):
        return self.health <= 0

    def is_targettable(self):
        if self.is_dead():
            return False

        return True

    def can_use_spells(self):
        for player in Player.game.players:
            for building in player.buildings:
                if building.name == "Spell Tower":
                    return True

        return False

    def choose_target(self):
        target = input("Select index of player to target: ")
        target = int(target)
        target = Player.game.players[target]

        return target

    def choose_card_from(self, target):
        target_card = input("Select index of card to target: ")
        target_card = int(target_card)
        target_card = target.hand[target_card]

        return target_card

    def choose_building(self):
        target = self.choose_target()
        
        target_building = input("Select index of building to target: ")
        target_building = int(target_building)
        target_building = target.buildings[target_building]

        return target_building

    def draw_cards(self, n):
        for i in range(n):
            card = Player.game.draw_card()
            self.hand.append(card)

    def play_turn(self):
        while True:
            print(f"HAND: {self.hand}")
            if not len(self.hand): return

            i = input("Select index of card to use, or enter to pass turn: ")
            if i == "": return
            
            i = int(i)
            card = self.hand[i]
            status_code, status_description = card.use(self)
            
            if self.game.log: print(status_description + "\n")

    def end_turn(self):
        self.attack_count = 0

        if len(self.hand) < self._hand_limit():
            amount_to_draw = self._hand_limit() - len(self.hand)
            self.draw_cards(amount_to_draw)
