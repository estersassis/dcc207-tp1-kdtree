class Point:
    def __init__(self, point: tuple, name: str, alvara: str, date: str, address: str):
        self.point = point
        self.name = name
        self.alvara = alvara
        self.date = date
        self.address = address

class KDNode:
    def __init__(self, point: Point):
        self.point = point

        self.left = None
        self.right = None

class KDTree:
    def __init__(self, points: list[Point]):
        self.k = len(points[0].point) 
        self.root: KDNode = self.build(points)

    def build(self, points: list[Point], depth=0):
        if not points:
            return None

        axis = depth % self.k
        sorted_points = sorted(points, key=lambda p: p.point[axis])
        median_idx = len(sorted_points) // 2
        median_point = sorted_points[median_idx]

        node = KDNode(median_point)
        node.left = self.build(sorted_points[:median_idx], depth + 1)
        node.right = self.build(sorted_points[median_idx + 1:], depth + 1)

        return node
    
    def search(self, region):
        result = []

        def _search(node, depth):
            if node is None:
                return

            p = node.point
            cd = depth % self.k
            (xmin, ymin), (xmax, ymax) = region

            if xmin <= p.point[0] <= xmax and ymin <= p.point[1] <= ymax:
                result.append(node.point)

            if node.left and p.point[cd] >= region[0][cd]:
                _search(node.left, depth + 1)
            if node.right and p.point[cd] <= region[1][cd]:
                _search(node.right, depth + 1)

        _search(self.root, 0)
        return result