import csv
from card import *
import random


class Game:

    def __init__(self):
        self.players = []
        self.deck = Game._init_deck()
        self.discard_pile = []
        self.roles = ["The Crown", "Demon Lord", "Usurper", "Knight", "Cultist"]
        self.logs = []

    def _init_deck():
        deck = []
        for i in range(30): deck.append(Attack("Attack", "", "offensive"))
        for i in range(2): deck.append(Backstab("Backstab", "", "offensive"))
        for i in range(3): deck.append(Capture("Capture", "", "offensive"))
        for i in range(3): deck.append(Destroy("Destroy", "", "offensive"))
        for i in range(1): deck.append(Heist("Heist", "", "offensive"))
        for i in range(1): deck.append(Sabotage("Sabotage", "", "offensive"))
        for i in range(1): deck.append(Spy("Spy", "", "offensive"))
        for i in range(9): deck.append(Defend("Defend", "", "utility"))
        for i in range(2): deck.append(GoodyBag("Goody Bag", "", "utility"))
        for i in range(1): deck.append(GoodyBagPlus("Goody Bag Plus", "", "utility"))
        for i in range(4): deck.append(Building("Barracks", "", "building"))
        for i in range(3): deck.append(Building("Farm", "", "building"))
        for i in range(2): deck.append(Building("Fort", "", "building"))
        for i in range(3): deck.append(Building("Spell Tower", "", "building"))
        deck.append(Barrier("Barrier", "", "spell"))
        deck.append(BlackHole("Black Hole", "", "spell"))
        deck.append(BloodMagic("Blood Magic", "", "spell"))
        deck.append(Nullify("Nullify", "", "spell"))

        return deck

    def print_game_log(self):
        for log in self.logs:
            print(log)

    def add_player(self, player):
        # add player to game
        self.players.append(player)
        player.game = self

        # kick player if no roles available
        if not self.roles:
            self.players.remove(player)
            player.game = None
        
        # assign random role
        player_role = random.choice(self.roles)
        self.roles.remove(player_role)
        player.role = player_role

    def draw_card(self):
        if not len(self.deck):
            self.deck = Game._init_deck()
            
        i = random.randrange(0, len(self.deck))
        return self.deck.pop(i)

    def _player_state(self):
        player_state = ""
        for i in range(len(self.players)): player_state += str(self.players[i]) + "\n"
        player_state += 32*"-" + "\n"

        return player_state

    def _deck_state(self):
        deck_state = f"DECK: {len(self.deck)}\n"
        deck_state += 32*"-" + "\n"

        return deck_state

    def state(self):
        game_state = "\n" + 16*"=" + " GAME STATE " + 16*"=" + "\n"
        game_state += 32*"-" + "\n"
        game_state += self._deck_state()
        game_state += self._player_state()
        game_state += 44*"=" + "\n"

        return game_state

    def play_turn(self, player):
        if player.is_dead(): return
        self.logs.append(f"--- Player {player.name}'s Turn: Role: {player.role}, Cards: {player.hand}, Buildings: {player.buildings} ---")
        player.play_turn()
        player.end_turn()

    def winning_role(self):
        dead_roles = [player.role for player in self.players if player.is_dead()]
        
        if all(role in dead_roles for role in ["The Crown", "Usurper", "Knight", "Cultist"]):
            return "Demon Lord"

        if all(role in dead_roles for role in ["Demon Lord", "Usurper", "Cultist"]):
            return "The Crown"

        if all(role in dead_roles for role in ["The Crown", "Knight"]):
            return "Cultist"

        if all(role in dead_roles for role in ["The Crown"]):
            return "Usurper"

        return None

    def play_round(self):
        for i in range(len(self.players)):
            player = self.players[i]
            self.play_turn(player)

            winning_role = self.winning_role()
            if winning_role:
                return winning_role

        return None
        
    def start(self):
        # all players pick up 5 cards
        for i in range(len(self.players)):
            self.players[i].draw_cards(5)

        # enter game loop
        while True:
            winning_role = self.play_round()

            if winning_role:
                self.logs.append(f"{winning_role} wins!")
                return winning_role
