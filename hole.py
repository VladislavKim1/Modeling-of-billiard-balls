from ball import canvas
from config import *

holes: list = list()


class Hole:
    def __init__(self, location: list, radius: float = 40.0, color: str = 'black'):
        """
        Hole constructor
        """
        self.color: str = color
        self.radius: float = radius
        self.location: dict = dict()
        self.location['x'] = location[0]
        self.location['y'] = location[1]
        self.hole = canvas.create_oval(self.location['x'] - self.radius,
                                       self.location['y'] - self.radius,
                                       self.location['x'] + self.radius,
                                       self.location['y'] + self.radius,
                                       fill=self.color, outline="")

        self.radius_border = self.radius + border_width
        self.hole_border = canvas.create_oval(self.location['x'] - self.radius_border,
                                              self.location['y'] - self.radius_border,
                                              self.location['x'] + self.radius_border,
                                              self.location['y'] + self.radius_border,
                                              fill=border_color, outline="")
        canvas.tag_lower(self.hole_border)
