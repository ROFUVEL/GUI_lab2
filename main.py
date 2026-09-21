import re

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    def __str__(self):
        return f"Point({self.x}, {self.y})"

class Line:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end
    def __str__(self):
        return f"Line({self.start}, {self.end})"

class Circle:
    def __init__(self, center: Point, radius: float):
        self.center = center
        self.radius = radius
    def __str__(self):
        return f"Circle({self.center}, {self.radius})"

num = r'[+-]?\d+(?:\.\d+)?'
point = rf'Point\(\s*({num})\s*,\s*({num})\s*\)'

pattern_point = re.compile(rf'^\s*{point}\s*$')
pattern_line = re.compile(rf'^\s*Line\(\s*{point}\s*,\s*{point}\s*\)\s*$')
pattern_circle = re.compile(rf'^\s*Circle\(\s*{point}\s*,\s*({num})\s*\)\s*$')


def parse_line(line: str):
    match = pattern_point.match(line)
    if match:
        x, y = float(match.group(1)), float(match.group(2))
        return Point(x, y)

    match = pattern_line.match(line)
    if match:
        start = Point(float(match.group(1)), float(match.group(2)))
        end   = Point(float(match.group(3)), float(match.group(4)))
        return Line(start, end)

    match = pattern_circle.match(line)
    if match:
        center = Point(float(match.group(1)), float(match.group(2)))
        radius = float(match.group(3))
        return Circle(center, radius)

    return None

# def main():
#     p = Point(3.4, 5.5)
#     print(p)
#
# if __name__ == '__main__':
#     main()
