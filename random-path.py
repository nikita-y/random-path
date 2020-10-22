import math
import random
import sys
import turtle

help_string = """
Simple random path generator.

This script draws a randomly generate path with no intersections.
Every segement of the path is a line with random length.
The max length of a line can be specified with first agrument.
If max length of a line is set to 0 or is't supplied
the line length will not be limited
"""


class Point:

    """Struct for 2D points"""

    __slots__ = ['_x', '_y']

    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    def __eq__(self, other):
        if self._x == other._x and self._y == other._y:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self == other

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, val):
        self._x = val

    @y.setter
    def y(self, val):
        self._y = val

    @staticmethod
    def random_point():
        return Point(random.randint(-200, 200),
                     random.randint(-200, 200))


class Line:

    """Class for base operations with 2D lines"""

    __slots__ = ['begin', 'end']

    def __init__(self, begin=Point(), end=Point()):
        self.begin = begin
        self.end = end

    def __distance(self, a, b):
        """returns distance between two points

        :type a: Point
        :type b: Point
        :rtype: float
        """
        return math.sqrt((b.x - a.x)**2 + (b.y - a.y)**2)

    def __area(self, a, b, c):
        """returns area of triangle, using its vertex coordinates x, y and c

        :type a: Point
        :type b: Point
        :type c: Point
        :rtype: float
        """
        return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

    def __point_belongs_the_line(self, line, point):
        return line.length() > 0 and \
            (point.x - line.begin.x) * (line.end.y - line.begin.y) - \
            (point.y - line.begin.y) * (line.end.x - line.begin.x) == 0

    def __intersect_points(self, a, b, c, d):
        """returns True if there is an intersection between lines a-b and c-d,
         otherwise returns False

        Determines if there is an intersection between lines a-b and c-d
        using oriented triangle area algorithm

        :param a: begin of the 1st line
        :type a: Point
        :param b: end of the 1st line
        :type b: Point
        :param c: begin of the 2nd line
        :type c: Point
        :param d: end of the 2nd line
        :type d: Point
        :rtype: bool
        """

        abc_abd = self.__area(a, b, c) * self.__area(a, b, d)
        cda_cdb = self.__area(c, d, a) * self.__area(c, d, b)
        return abc_abd < 0 and cda_cdb < 0

    def __intersect_lines(self, a, b):
        """returns True if there is an intersection between lines a and b,
         otherwise returns False

        :type a: Line
        :type b: Line
        :rtype: bool
        """

        return self.__point_belongs_the_line(a, b.end) or \
            self.__intersect_points(a.begin, a.end, b.begin, b.end)

    def is_intersected(self, line):
        """returns True if the line intersects the given line, otherwise
        returns False

        :type line: Line
        :rtype: bool
        """
        return self.__intersect_lines(self, line)

    def length(self):
        """returns distance between begin and end points

        :rtype: float
        """
        return abs(self.__distance(self.begin, self.end))


def generate_path(line_lengh_max):
    """ The generator yeilds random, not intersecting itself 2D polygonal path

        :param line_lengh_max: max length of each node
        :type line_lengh_max: int
        :rtype Line()
    """
    lines = [Line()]
    while True:
        new_point = Point.random_point()
        end_of_last_line = lines[-1].end
        new_line = Line(end_of_last_line, new_point)

        if new_line.length() > line_lengh_max > 0:
            continue

        intersection = any(l.is_intersected(new_line) for l in lines)

        if not intersection:
            lines.append(new_line)
            yield new_line


def draw_path(line_lengh_max):
    """
        The function draws random, not intersecting itself 2D polygonal path

        :param line_lengh_max: max length of each node
    """
    turtle.bgcolor("black")
    turtle.color("white")
    turtle.shape('circle')
    turtle.shapesize(0.1, 0.1)
    turtle.speed(0)
    turtle.pendown()

    try:
        for line in generate_path(line_lengh_max):
            turtle.goto(line.end.x, line.end.y)
    except:
        exit()


def main(args):
    try:
        line_lengh = int(args[0])
    except ValueError:
        print(help_string)
    except IndexError:
        draw_path(0)
    else:
        draw_path(line_lengh)


if __name__ == '__main__':
    main(sys.argv[1:])
