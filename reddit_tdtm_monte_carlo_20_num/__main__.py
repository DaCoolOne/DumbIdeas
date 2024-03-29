import random

from strategy import Strategy

def play_game() -> bool:
    s = Strategy()
    for i in range(20):
        if not s.place(random.randint(0, 1000)):
            return False, i
    return True, 20

if __name__ == "__main__":
    total_wins = 0
    total_games = 0
    total_rounds = 0

    try:
        while True:
            result, rounds = play_game()
            total_games += 1
            if result:
                total_wins += 1
            total_rounds += rounds

            if total_games % 10000 == 0:
                print(total_games)
    except KeyboardInterrupt:
        print(f"Played {total_games} games with {total_wins} wins for a {total_wins/total_games*100:0.4f}% win rate averaging {total_rounds/total_games:0.2f} rounds")