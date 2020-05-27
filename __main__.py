import time
import json
from math import sqrt
from tkinter import *

from config import *

root = Tk()
root.title("billiard balls")
balls: list = list()

canvas = Canvas(root, width=screen_width, height=screen_height)


def vector_multiplication(a: tuple, b: tuple):
    return (a[0]*b[0]) + (a[1]*b[1])


class Ball:
    """
    This class describes the behavior of the ball.
    """
    _player: bool = False

    def __init__(self, location: list, color: str = 'black', radius: float = 30.0, balls = balls):
        """
        Ball constructor
        """
        self.color = color
        self.radius = radius
        self.m = radius * 10  # weight
        self.location = dict()
        self.location['x'] = location[0]
        self.location['y'] = location[1]  # ball_1_centre_x, y
        self.ball = canvas.create_oval(self.location['x'] - self.radius,  # ball_1
                                       self.location['y'] - self.radius,
                                       self.location['x'] + self.radius,
                                       self.location['y'] + self.radius,
                                       fill=self.color, outline="")
        self.speed_x = 0
        self.speed_y = 0

        if not len(balls):
            self._player = True

    def render(self):
        canvas.coords(self.ball,
                      self.location['x'] - self.radius,
                      self.location['y'] - self.radius,
                      self.location['x'] + self.radius,
                      self.location['y'] + self.radius)

    def control(self, event):
        if self._player:
            dcx, dcy = 0, 0
            if event.char == "w":
                dcy = -1
            elif event.char == "s":
                dcy = 1
            elif event.char == "a":
                dcx = -1
            elif event.char == "d":
                dcx = 1
            elif event.char == "q":
                root.quit()

            self.speed_x += acceleration * dcx
            self.speed_y += acceleration * dcy


def key(event):
    for ball in balls:
        ball.control(event)


def update():
    global last_time
    cur_time = time.time()
    if last_time:
        dt = cur_time - last_time

        for index, ball_one in enumerate(balls):

            dx = ball_one.speed_x * dt
            dy = ball_one.speed_y * dt

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

            # attenuation
            ball_one.speed_y /= 1 + stop_speed
            ball_one.speed_x /= 1 + stop_speed

            buf_balls = balls.copy()
            del buf_balls[index]

            for ball_two in buf_balls:
                strike = False
                R = ball_one.radius + ball_two.radius

                max_x = field_x + field_width - border_width - ball_one.radius
                max_y = field_y + field_height - border_width - ball_one.radius
                min_x = field_x + border_width + ball_one.radius
                min_y = field_y + border_width + ball_one.radius

                if not (min_x <= ball_one.location['x'] + dx <= max_x):
                    ball_one.speed_x = -ball_one.speed_x
                    strike = True
                if not (min_y <= ball_one.location['y'] + dy <= max_y):
                    ball_one.speed_y = -ball_one.speed_y
                    strike = True

                sigma_next = sqrt(pow(((ball_one.location['x'] + dx) - ball_two.location['x']), 2) + pow(((ball_one.location['y'] + dy) - ball_two.location['y']), 2))
                if sigma_next <= R:
                    strike = True
                    sigma = sqrt(pow((ball_one.location['x'] - ball_two.location['x']), 2) + pow((ball_one.location['y'] - ball_two.location['y']), 2))
                    dr = (ball_two.location['x'] - ball_one.location['x'], ball_two.location['y'] - ball_one.location['y'])
                    du = (ball_two.speed_x - ball_one.speed_x, ball_two.speed_y - ball_one.speed_y)
                    J = (2 * ball_one.m * ball_two.m * vector_multiplication(du, dr)) / (sigma * (ball_one.m + ball_two.m))

                    drx = ball_two.location['x'] - ball_one.location['x']
                    dry = ball_two.location['y'] - ball_one.location['y']

                    Jx = (J * drx) / sigma
                    Jy = (J * dry) / sigma

                    ball_one.speed_x += Jx / ball_one.m
                    ball_one.speed_y += Jy / ball_one.m

                    ball_two.speed_x -= Jx / ball_two.m
                    ball_two.speed_y -= Jy / ball_two.m

                if strike:
                    # Skip to check for collisions in the next iteration
                    dx = 0
                    dy = 0

            ball_one.location['x'] += dx
            ball_one.location['y'] += dy
            ball_one.render()

    last_time = cur_time
    root.after(1, update)


if __name__ == '__main__':
    board(canvas)
    with open(balls_filename) as f:
        for ball_name, struct in json.load(f).items():
            balls.append(Ball(struct['position'], struct['color'], struct['radius']))

    root.bind("<Key>", key)

    update()
    root.mainloop()

