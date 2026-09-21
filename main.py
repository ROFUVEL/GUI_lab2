import re

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


num = r'[+-]?\d+(?:\.\d+)?'
point = rf'Point\(\s*({num})\s*,\s*({num})\s*\)'

pattern_point = re.compile(rf'^\s*{point}\s*$')
pattern_line = re.compile(rf'^\s*Line\(\s*{point}\s*,\s*{point}\s*\)\s*$')
pattern_circle = re.compile(rf'^\s*Circle\(\s*{point}\s*,\s*({num})\s*\)\s*$')

# def main():
#     p = Point(3.4, 5.5)
#     print(p)
#
# if __name__ == '__main__':
#     main()
