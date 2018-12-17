from string import ascii_lowercase

class ListNode():

    def __init__(self, data=None, prev_node=None, next_node=None):
        self.data = data
        self.prev_node = prev_node
        self.next_node = next_node

class LList():

    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def __len__(self):
        return self.length

    @classmethod
    def from_iterable(cls, iterable):
        llist = cls()
        for item in iterable:
            llist.append(item)
        return llist

    def append(self, data):
        if not self.head:
            self.head = ListNode(data=data)
            self.tail = self.head
        else:
            node = ListNode(data=data, prev_node=self.tail)
            self.tail.next_node = node
            self.tail = node
        self.length += 1

    def remove(self, node):
        if node.prev_node:
            node.prev_node.next_node = node.next_node
        if node.next_node:
            node.next_node.prev_node = node.prev_node
        if node is self.head:
            self.head = node.next_node
        if node is self.tail:
            self.tail = node.prev_node
        self.length -= 1

    def nodes(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next_node


def get_polymer():
    with open('data/5.txt', 'r') as f:
        return f.readline().strip()

def different_cases(c1, c2):
    return (c1.islower() and c2.isupper()) or (c1.isupper() and c2.islower())

def same_letter(c1, c2):
    return c1.lower() == c2.lower()

def annihilate(c1, c2):
    return different_cases(c1, c2) and same_letter(c1, c2)

def reacted_length(polymer_iterable):
    polymer = LList.from_iterable(polymer_iterable)

    node = polymer.head
    while node is not None:
        next_node = node.next_node
        if next_node and annihilate(node.data, next_node.data):
            polymer.remove(node)
            polymer.remove(next_node)
            node = node.prev_node or next_node.next_node
        else:
            node = next_node

    return len(polymer)

def best_reacted_length(polymer_str):
    def reacted_length_of(letter):
        without_letter = (c for c in polymer_str if c.lower() != letter)
        return reacted_length(without_letter)
    return min(reacted_length_of(c) for c in ascii_lowercase)

polymer_str = get_polymer()
print(reacted_length(polymer_str))
print(best_reacted_length(polymer_str))
