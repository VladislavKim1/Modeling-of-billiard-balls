import random
from tkinter import *

from config import *
# from config_test import *
from util import border_value, sigma

root = Tk()
root.title("billiard balls")
canvas = Canvas(root, width=screen_width, height=screen_height)
balls: list = list()


class Ball:
    """
    This class describes the behavior of the ball.
    """
    player: bool = False

    def __init__(self, location: list, color: str = 'black', radius: float = 30.0, balls = balls):
        """
        Ball constructor
        """
        self.color: str = color
        self.radius: float = radius
        self.m = radius * 10  # weight
        self.location: dict = dict()
        self.location['x'] = location[0]
        self.location['y'] = location[1]  # ball_1_centre_x, y
        self.ball = canvas.create_oval(self.location['x'] - self.radius,  # ball_1
                                       self.location['y'] - self.radius,
                                       self.location['x'] + self.radius,
                                       self.location['y'] + self.radius,
                                       fill=self.color, outline="")
        self.speed_x = 0
        self.speed_y = 0
        self.balls = balls

        if not len(self.balls):
            self.player = True

    def render(self):
        canvas.coords(self.ball,
                      self.location['x'] - self.radius,
                      self.location['y'] - self.radius,
                      self.location['x'] + self.radius,
                      self.location['y'] + self.radius)

    def balls_edit(self) -> list:
        tmp: list = self.balls.copy()
        for index, item in enumerate(tmp):
            if self == item:
                del tmp[index]
                return tmp

    def delete(self):
        if self.player:
            while True:
                restart = False
                self.random_location()
                for ball in self.balls_edit():
                    s: float = sigma(0, 0, self, ball)
                    if s <= (self.radius + ball.radius):
                        restart = True
                if not restart:
                    break
            self.speed_x = 0
            self.speed_y = 0
            self.render()
        else:
            canvas.delete(self.ball)
            for index, item in enumerate(self.balls):
                if self == item:
                    del self.balls[index]

    def random_location(self):
        max_x, max_y, min_x, min_y = border_value(self)
        self.location['x']: float = random.choice(range(min_x, int(max_x/2), 1))
        self.location['y']: float = random.choice(range(min_y, max_y, 1))

    def control(self, event):
        if self.player:
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
