import re
import argparse
import sys

class Shape:
    def __str__(self):
        raise NotImplementedError

class Point(Shape):
    def __init__(self, x: float, y: float, color: tuple = (0, 0, 0)):
        self.x = x
        self.y = y
        self.color = color
    def __str__(self):
        return f"Point({self.x}, {self.y}, цвет={self.color})"

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
col = r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
point = rf'Point\(\s*({num})\s*,\s*({num})\s*,\s*({col})\s*,\s*({col})\s*,\s*({col})\s*\)'

pattern_point = re.compile(rf'^\s*{point}\s*$')
pattern_line = re.compile(rf'^\s*Line\(\s*{point}\s*,\s*{point}\s*\)\s*$')
pattern_circle = re.compile(rf'^\s*Circle\(\s*{point}\s*,\s*({num})\s*\)\s*$')


def parse_line(line: str):
    match = pattern_point.match(line)
    if match:
        x, y = float(match.group(1)), float(match.group(2))
        color = (int(match.group(3)), int(match.group(4)), int(match.group(5)))
        return Point(x, y, color)

    match = pattern_line.match(line)
    if match:
        color1 = (int(match.group(3)), int(match.group(4)), int(match.group(5)))
        start = Point(float(match.group(1)), float(match.group(2)), color1)

        color2 = (int(match.group(8)), int(match.group(9)), int(match.group(10)))
        end = Point(float(match.group(6)), float(match.group(7)), color2)
        return Line(start, end)

    match = pattern_circle.match(line)
    if match:
        color_center = (
            int(match.group(3)),
            int(match.group(4)),
            int(match.group(5)),
        )
        center = Point(float(match.group(1)), float(match.group(2)), color_center)
        radius = float(match.group(6))
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
        sys.exit(66) # обчный exit - интерактивно в консоль, sys.exit - ошибка в запуске скрипта (как в этой лабе)
                     # - ошибка отсутствующего файла (на будущее)
    return shapes

def operation_print(shapes: list) -> None:
    if not shapes:
        print("Список фигур пуст")
        return

    for shape in shapes:
        print(shape)

def operation_print_count(shapes: list) -> None:
    print(f"Количество фигур: {len(shapes)}")

def operation_remove_from_file(filepath: str, target_color: tuple) -> None:

    def has_color(shape, color):
        if isinstance(shape, Point):
            return shape.color == color
        if isinstance(shape, Line):
            return shape.start.color == color or shape.end.color == color
        if isinstance(shape, Circle):
            return shape.center.color == color
        return False

    lines_to_keep = []
    removed_count = 0

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            cleaned_line = line.strip()

            if not cleaned_line:
                lines_to_keep.append(line)
                continue

            shape = parse_line(cleaned_line)

            if shape and has_color(shape, target_color):
                removed_count += 1
                continue

            lines_to_keep.append(line)

        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(lines_to_keep)

        print(
            f"Операция завершена. Из файла '{filepath}' удалено строк: {removed_count}"
        )

    except FileNotFoundError:
        print(f"Ошибка: файл '{filepath}' не найден", file=sys.stderr)
        sys.exit(66)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Программа для обработки геометрических фигур из файла'
    )

    parser.add_argument(
        '-f', '--file',
        required=True,
        help='Путь к файлу с фигурами'
    )

    parser.add_argument(
        '-o', '--oper',
        required=True,
        choices=['print', 'count', 'remove'],
        help='Операция над списком фигур: print или count или remove'
    )

    parser.add_argument(
        "--color",
        type=int,
        nargs=3,
        metavar=("R", "G", "B"),
        help="Цвет RGB для операции удаления (например: --color 255 255 255)",
    )

    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.oper == "remove" and not args.color:
        print(
            "Ошибка: для операции 'remove' необходимо указать цвет с помощью флага --color R G B",
            file=sys.stderr,
        )
        sys.exit(64) # 64 - ошибка командной строки

    if args.oper == "remove":
        target_color = tuple(args.color)
        operation_remove_from_file(args.file, target_color)
    else:
        shapes = read_shapes(args.file)
        if args.oper == "print":
            operation_print(shapes)
        elif args.oper == "count":
            operation_print_count(shapes)

if __name__ == '__main__':
    main()
