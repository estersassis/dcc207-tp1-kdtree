class KDNode:
    def __init__(self, point):
        self.point: tuple = point
        self.left = None
        self.right = None

class KDTree:
    def __init__(self):
        self.root: KDNode = None
        self.k = None
    
    def insert(self, point):
        if not self.k:
            self.k = len(point)

        def _insert_rec(node, point, depth):
            if node is None:
                return KDNode(point)

            cd = depth % self.k

            if point[cd] < node.point[cd]:
                node.left = _insert_rec(node.left, point, depth + 1)
            else:
                node.right = _insert_rec(node.right, point, depth + 1)

            return node

        self.root = _insert_rec(self.root, point, depth=0)

def main():
    tree = KDTree()
    tree.insert((3, 6))
    tree.insert((17, 15))
    tree.insert((13, 15))
    tree.insert((6, 12))
    tree.insert((9, 1))
    tree.insert((2, 7))
    tree.insert((10, 19))

if __name__ == "__main__":
    main()