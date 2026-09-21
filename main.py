import re
import argparse

class Shape:
    def __str__(self):
        raise NotImplementedError

class Point(Shape):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    def __str__(self):
        return f"Point({self.x}, {self.y})"

class Line(Shape):
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end
    def __str__(self):
        return f"Line({self.start}, {self.end})"

class Circle(Shape):
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

def read_shapes(filepath: str) -> list:
    shapes = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                if not line:
                    continue
                result = parse_line(line)

                if result is not None:
                    shapes.append(result)
                else:
                    print(f"некорректное описание объектов. '{line}'")

    except FileNotFoundError:
        print(f"Ошибка: файл '{filepath}' не найден")
        exit(66) # 66 - ошибка отсутствующего файла (на будущее)

    return shapes



def main():
    shapes = read_shapes("data.txt")
    for s in shapes:
        print(s)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Программа для обработки геометрических фигур из файла"
    )

    parser.add_argument(
        "-f", "--file",
        required=True, help="Путь к файлу с фигурами"
    )

    parser.add_argument(
        "-o",
        "--oper",
        required=True,
        choices=["print", "count"],
        help="Операция над списком фигур: print или count",
    )

    args = parser.parse_args()

    main()
