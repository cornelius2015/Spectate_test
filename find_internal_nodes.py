import unittest

def find_internal_nodes_num(tree):
    num_of_nodes = len(tree)
    internal_nodes = 0
    # Complexity of O(n)
    for node in range(num_of_nodes):
        if node in tree:
            internal_nodes += 1
    return internal_nodes


my_tree = [4, 4, 1, 5, -1, 4, 5]
print(find_internal_nodes_num(my_tree))


class TestFindInternalNodesNum(unittest.TestCase):

    def test_case1(self):
        # Single internal node
        tree = [4, 4, 4, 4, -1]
        result = find_internal_nodes_num(tree)
        self.assertEqual(result, 1)

    def test_case2(self):
        # Multiple internal nodes
        tree = [4, 4, 1, 5, -1, 4, 5]
        result = find_internal_nodes_num(tree)
        self.assertEqual(result, 3)

    def test_case3(self):
        # No internal nodes
        tree = [-1, -1, -1, -1, -1]
        result = find_internal_nodes_num(tree)
        self.assertEqual(result, 0)

    def test_case4(self):
        # Binary tree
        tree = [-1, 0, 0, 1, 1, 2, 2]
        result = find_internal_nodes_num(tree)
        self.assertEqual(result, 3)


if __name__ == '__main__':
    unittest.main()
