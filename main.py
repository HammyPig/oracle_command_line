from game import Game
from player import Player
from bot import Bot


def main():
    game = Game()
    
    players = [
        Player("1"),
        Bot("2"),
        Bot("3"),
        Bot("4"),
        Bot("5"),
    ]

    for player in players:
        game.add_player(player)

    game.start()
    game.print_game_log()
    
if __name__ == "__main__":
    main()
