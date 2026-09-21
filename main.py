class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Line:
    def __init__(self, x: Point, y: Point):
        self.x = x
        self.y = y


class Circle:
    def __init__(self, center: Point, radius: float):
        self.center = center
        self.radius = radius

# if __name__ == '__main__':
#     print_hi('PyCharm')
