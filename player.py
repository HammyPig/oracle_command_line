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

        return f"Player {self.name}, health: {self.health}, buildings: {self.buildings}, attacks: {self.attack_count}/{self._attack_limit()}"

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

    def is_dead(self):
        return self.health <= 0

    def is_targettable(self):
        if self.is_dead():
            return False

        return True

    def _choose_target(self):
        while True:
            target = input("Select index of player to target: ")
            target = int(target)
            target = Player.game.players[target]

            if target.is_targettable():
                return target
            else:
                print(f"Player {target.name} is not targettable! Please choose another player.")

    def play_card(self, card_i):
        if card_i >= len(self.hand):
            return

        card = self.hand[card_i]

        if card.type == "offensive":
            if card.name == "Attack" and self.attack_count >= self._attack_limit():
                print("Already used maximum amount of attacks!")
                return
            else:
                self.attack_count += 1

            target = self._choose_target()
            card.use(self, target)
        elif card.type == "building":
            self.buildings.append(card)
            print(f"Player {self.name} used {card.name}")

        self.hand.pop(card_i)

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
            self.play_card(i)

    def end_turn(self):
        self.attack_count = 0

        if len(self.hand) < self._hand_limit():
            amount_to_draw = self._hand_limit() - len(self.hand)
            self.draw_cards(amount_to_draw)
