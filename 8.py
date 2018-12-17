class Node:

    def __init__(self):
        self.children = []
        self.metadata = []

    def _as_list(self):
        return [child._as_list() for child in self.children] + self.metadata

    def __repr__(self):
        return repr(self._as_list())

def get_data():
    with open('data/8.txt', 'r') as f:
        return [int(x) for x in f.readline().split()]

def parse_tree(data):
    node_stack, count_stack, metadata_stack, pointer = [], [], [], 0
    while pointer < len(data):

        if count_stack and count_stack[-1] == 0:
            num_metadata = metadata_stack.pop()

            for _ in range(num_metadata):
                node_stack[-1].metadata.append(data[pointer])
                pointer += 1

            if len(node_stack) > 1:
                finished_node = node_stack.pop()
                node_stack[-1].children.append(finished_node)

            count_stack.pop()
            if count_stack:
                count_stack[-1] -= 1

        else:
            node_stack.append(Node())
            count_stack.append(data[pointer])
            metadata_stack.append(data[pointer + 1])
            pointer += 2

    return node_stack[0]

def sum_of_metadata(root):
    return sum(root.metadata) + sum(sum_of_metadata(c) for c in root.children)

def value(node):
    if not node.children:
        return sum(node.metadata)
    else:
        return sum(value(node.children[i - 1]) if i <= len(node.children) else 0 for i in node.metadata)

data = get_data()
root = parse_tree(data)
print(sum_of_metadata(root))
print(value(root))
