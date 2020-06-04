from math import sqrt

from config import *
# from config_test import *


def border_value(ball: 'Ball') -> tuple:
    max_x = field_x + field_width - border_width - ball.radius
    max_y = field_y + field_height - border_width - ball.radius
    min_x = field_x + border_width + ball.radius
    min_y = field_y + border_width + ball.radius
    return max_x, max_y, min_x, min_y


def sigma(dx: float, dy: float, obj1: 'Ball', obj2: 'Ball') -> float:
    return sqrt(pow(((obj1.location['x'] + dx) - obj2.location['x']), 2) +
                pow(((obj1.location['y'] + dy) - obj2.location['y']), 2))
