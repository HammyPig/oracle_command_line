from game import Game
from player import Player
from bot import Bot


def main():
    game = Game()
    Player.game = game

    game.players = [
        Player("1"),
        Bot("2"),
        Bot("3"),
        Bot("4"),
        Bot("5"),
    ]

    # all players pick up 5 cards
    for i in range(len(game.players)): game.players[i].draw_cards(5)

    while True:
        print(game.state())

        game.play_round()

        # check how many players alive
        alive = 0
        for i in range(len(game.players)):
            if not game.players[i].is_dead():
                alive += 1

        if alive < 2:
            break

    print(game.state())

    
if __name__ == "__main__":
    main()
