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
    
    def range_search(self, region):
        result = []

        def _search(node, depth):
            if node is None:
                return

            point = node.point
            cd = depth % self.k
            (xmin, ymin), (xmax, ymax) = region

            if xmin <= point[0] <= xmax and ymin <= point[1] <= ymax:
                result.append(point)

            if node.left and point[cd] >= region[0][cd]:
                _search(node.left, depth + 1)
            if node.right and point[cd] <= region[1][cd]:
                _search(node.right, depth + 1)

        _search(self.root, 0)
        return result

def main():
    tree = KDTree()
    tree.insert((3, 6))
    tree.insert((17, 15))
    tree.insert((13, 15))
    tree.insert((6, 12))
    tree.insert((9, 1))
    tree.insert((2, 7))
    tree.insert((10, 19))

    resultado = tree.range_search([(5, 5), (15, 16)])
    print("Pontos dentro da região [(5,5) a (15,16)]:")
    for p in resultado:
        print(p)

if __name__ == "__main__":
    main()