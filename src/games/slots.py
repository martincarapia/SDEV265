import random


def play_slots(wager):
    emojis = ["🍍", "🍉", "🍒", "🍋", "🍊", "🍇"]
    result = [random.choice(emojis) for _ in range(3)]
    coin_multiplier = random.randint(1, 5)

    if result[0] == result[1] == result[2]:
        earnings = wager * coin_multiplier
        return "You Win!", f"Result: {' '.join(result)}", f"You earned {earnings} coins"
    else:
        return "You Lose!", f"Result: {' '.join(result)}", f"You lost {wager} coins"


wager = int(input("How much ya lookin' to wager?.. "))

results = play_slots(wager)
for line in results:
    print(line)
