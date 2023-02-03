import csv
from card import *
import random


class Game:

    def __init__(self):
        self.players = []
        self.deck = Game._init_deck()
        self.discard_pile = []

    def _init_deck():
        deck = []
        for i in range(30): deck.append(Attack("Attack", "", "offensive"))
        for i in range(2): deck.append(Backstab("Backstab", "", "offensive"))
        for i in range(3): deck.append(Capture("Capture", "", "offensive"))
        for i in range(3): deck.append(Destroy("Destroy", "", "offensive"))
        for i in range(1): deck.append(Heist("Heist", "", "offensive"))
        for i in range(1): deck.append(Sabotage("Sabotage", "", "offensive"))
        for i in range(1): deck.append(Spy("Spy", "", "offensive"))
        for i in range(2): deck.append(GoodyBag("Goody Bag", "", "utility"))
        for i in range(1): deck.append(GoodyBagPlus("Goody Bag Plus", "", "utility"))
        for i in range(4): deck.append(Building("Barracks", "", "building"))
        for i in range(3): deck.append(Building("Farm", "", "building"))
        #for i in range(2): deck.append(Building("Fort", "", "building"))
        for i in range(3): deck.append(Building("Spell Tower", "", "building"))

        return deck

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
        print(16*"=" + f" Player {player.name}'s Turn " + 16*"=" + "\n")
        player.play_turn()
        player.end_turn()

    def play_round(self):
        for i in range(len(self.players)):
            player = self.players[i]
            self.play_turn(player)
