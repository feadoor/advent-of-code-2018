PLAYERS = 446
MARBLES = 71522 # 7152200

class Marble():

    def __init__(self, data=None, prev_marble=None, next_marble=None):
        self.data = data
        self.prev_marble = prev_marble
        self.next_marble = next_marble

class MarbleCircle():

    def __init__(self):
        marble = Marble(0)
        marble.prev_marble = marble.next_marble = marble
        self.marbles = [marble]

    def insert_after(self, marble, data):
        new_marble = Marble(data=data, prev_marble=marble, next_marble=marble.next_marble)
        marble.next_marble.prev_marble = new_marble
        marble.next_marble = new_marble
        return new_marble

    def remove(self, marble):
        marble.prev_marble.next_marble = marble.next_marble
        marble.next_marble.prev_marble = marble.prev_marble
        return marble

    def marble_at_offset(self, marble, offset):
        if offset >= 0:
            for _ in range(offset):
                marble = marble.next_marble
        else:
            for _ in range(-offset):
                marble = marble.prev_marble
        return marble


def get_scores():
    scores = [0] * PLAYERS
    marbles = MarbleCircle()
    current_marble = marbles.marbles[0]

    for n in range(1, MARBLES + 1):
        if n % 23:
            insertion_point = current_marble.next_marble
            marble = marbles.insert_after(insertion_point, n)
            current_marble = marble
        else:
            player = ((n - 1) % PLAYERS)
            removed_marble = marbles.remove(marbles.marble_at_offset(current_marble, -7))
            current_marble = removed_marble.next_marble
            scores[player] += n + removed_marble.data

    return scores

print(max(get_scores()))
