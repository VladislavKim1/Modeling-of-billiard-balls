import json
import time
from tkinter import Tk, messagebox as mb

from ball import Ball, balls, root
from hole import holes, Hole
from config import *
# from config_test import *
from util import border_value, sigma


def vector_multiplication(a: tuple, b: tuple):
    return (a[0]*b[0]) + (a[1]*b[1])


def delta(ball: 'Ball', dt: float):
    dx = ball.speed_x * dt
    dy = ball.speed_y * dt

    # speed limit
    if abs(dx) > max_speed:
        if dx > 0:
            dx = max_speed
        elif dx < 0:
            dx = -max_speed

    if abs(dy) > max_speed:
        if dy > 0:
            dy = max_speed
        elif dy < 0:
            dy = -max_speed

    return dx, dy


def window_end_game():
    answer = mb.askyesno(title="end game", message="restart?")
    return answer


def start_balls() -> list:
    with open(balls_filename) as f:
        for ball_name, struct in json.load(f).items():
            balls.append(Ball(struct['position'], struct['color'], struct['radius']))
    return balls


def make_holes() -> list:
    for coord in hole_cord:
        holes.append(Hole(coord))
    return holes


def check_game():
    last_time = time.time()
    if len(balls) == 1:
        if window_end_game():
            balls[0].player = False
            balls[0].delete()
            start_balls()
            root.after(1, lambda: update(last_time, balls))
            return last_time, balls
        else:
            root.quit()


def detect_collision(ball_one: Ball, ball_two: Ball):
    s = sigma(0, 0, ball_one, ball_two)
    dr: tuple = (ball_two.location['x'] - ball_one.location['x'], ball_two.location['y'] - ball_one.location['y'])
    du: tuple = (ball_two.speed_x - ball_one.speed_x, ball_two.speed_y - ball_one.speed_y)
    J = (2 * ball_one.m * ball_two.m * vector_multiplication(du, dr)) / (s * (ball_one.m + ball_two.m))

    drx = ball_two.location['x'] - ball_one.location['x']
    dry = ball_two.location['y'] - ball_one.location['y']

    Jx = (J * drx) / s
    Jy = (J * dry) / s

    ball_one.speed_x += Jx / ball_one.m
    ball_one.speed_y += Jy / ball_one.m

    ball_two.speed_x -= Jx / ball_two.m
    ball_two.speed_y -= Jy / ball_two.m


def hole_gravity(ball_one, hole):
    a: int = 5

    x_1: float = abs(ball_one.location['x'] - hole.location['x'])
    y_1: float = abs(ball_one.location['y'] - hole.location['y'])

    if ball_one.location['x'] > hole.location['x']:
        x_1: float = x_1 * (-1)

    if ball_one.location['y'] > hole.location['y']:
        y_1: float = y_1 * (-1)

    k_x: float = abs(x_1 / y_1)
    ball_one.speed_y = y_1 * a
    ball_one.speed_x = x_1 * (k_x * a)


def calculate_border(symbol: str, hole, ball_one, dxy) -> bool:
    min_y_hole: float = hole.location[f"{symbol}"] - hole.radius
    max_y_hole: float = hole.location[f"{symbol}"] + hole.radius
    if min_y_hole <= ball_one.location[f"{symbol}"] + dxy <= max_y_hole:
        return True
    return False


def update(last_time, balls: list, fix_dt=None):
    cur_time = time.time()
    if last_time:
        dt = cur_time - last_time
        if fix_dt:
            dt = fix_dt

        for index, ball_one in enumerate(balls):
            max_x, max_y, min_x, min_y = border_value(ball_one)
            dx, dy = delta(ball_one, dt)

            # attenuation
            ball_one.speed_y /= 1 + stop_speed
            ball_one.speed_x /= 1 + stop_speed

            buf_balls: list = balls.copy()
            del buf_balls[index]

            check_game()

            for ball_two in buf_balls:
                strike: bool = False
                R = ball_one.radius + ball_two.radius

                tmp: bool = True
                # Border
                if not (min_x <= ball_one.location['x'] + dx <= max_x):
                    for hole in holes:
                        if calculate_border('y', hole, ball_one, dy):
                            tmp = False
                            s = sigma(dx, dy, ball_one, hole)
                            if s <= hole.radius * 2:
                                hole_gravity(ball_one, hole)

                            if s <= abs(ball_one.radius - hole.radius):
                                ball_one.delete()
                                last_time = cur_time
                                root.after(1, lambda: update(last_time, balls))
                                return last_time, balls
                    if tmp:
                        ball_one.speed_x = -ball_one.speed_x
                        strike = True

                if not (min_y <= ball_one.location['y'] + dy <= max_y):
                    for hole in holes:
                        if calculate_border('x', hole, ball_one, dx):
                            tmp = False
                            s = sigma(dx, dy, ball_one, hole)
                            if s <= hole.radius * 2:
                                hole_gravity(ball_one, hole)

                            if s <= abs(ball_one.radius - hole.radius):
                                ball_one.delete()
                                last_time = cur_time
                                root.after(1, lambda: update(last_time, balls))
                                return last_time, balls
                    if tmp:
                        ball_one.speed_y = -ball_one.speed_y
                        strike = True

                if sigma(dx, dy, ball_one, ball_two) <= R:
                    strike = True

                    detect_collision(ball_one, ball_two)

                if strike:
                    # Skip to check for collisions in the next iteration
                    dx = 0
                    dy = 0

            ball_one.location['x'] += dx
            ball_one.location['y'] += dy
            ball_one.render()

    last_time = cur_time
    root.after(1, lambda: update(last_time, balls))
    return last_time, balls
