import math

class Line:

    def __init__(self, x1, y1, x2, y2):
        self.__k = (y2 - y1) / (x2 - x1)
        self.__b = (x1*y1-x1*y2+y1*x2-y1*x1)

    def get_crossing(self, line):
        if not isinstance(line, Line):
            raise TypeError('arg isn\'t instance of Line')
        x = (line.__b - self.__b) / (self.__k - line.__k)
        y = self.__k * x + self.__b
        return x, y


def have_intersection(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):

    if abs(ax1 - bx1) + abs(ay1 - by1) > 0.01:
        return False

    v1 = (bx2 - bx1) * (ay1 - by1) - (by2 - by1) * (ax1 - bx1)
    v2 = (bx2 - bx1) * (ay2 - by1) - (by2 - by1) * (ax2 - bx1)
    v3 = (ax2 - ax1) * (by1 - ay1) - (ay2 - ay1) * (bx1 - ax1)
    v4 = (ax2 - ax1) * (by2 - ay1) - (ay2 - ay1) * (bx2 - ax1)
    return (v1 * v2 < 0) and (v3 * v4 < 0)


def evklid(node1, node2):
    return math.sqrt(math.pow(node1.x-node2.x, 2) + math.pow(node1.y-node2.y, 2))
