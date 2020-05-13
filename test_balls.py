from tkinter import *

import time

screen_width = 1200
screen_height = 800

indent_y = 20
intent_x = 50
border_width = 20

field_x = intent_x
field_y = intent_x + indent_y
field_width = screen_width - 2 * field_x
field_height = screen_height - 2 * field_y

ball_radius = 30

border_color = "#A52A2A"
field_color = "#013220"
ball_color = "#FFFFF0"

root = Tk()
root.title("billiard balls")

canvas = Canvas(root, width=screen_width, height=screen_height)
canvas.pack()

text = canvas.create_text(screen_width / 2, indent_y,
                          text="Use WASD to accelerate the white ball and arrows to accelerate black ball, to quit "
                               "use Q")

border = canvas.create_rectangle(field_x, field_y, field_x + field_width, field_y + field_height, fill=border_color,
                                 outline="")

field = canvas.create_rectangle(field_x + border_width, field_y + border_width, field_x + field_width - border_width,
                                field_y + field_height - border_width, fill=field_color, outline="")

max_x = field_x + field_width - border_width - ball_radius
max_y = field_y + field_height - border_width - ball_radius
min_x = field_x + border_width + ball_radius
min_y = field_y + border_width + ball_radius

ball_centre_x = field_x + field_width / 5
ball_centre_y = field_y + field_height / 2
ball = canvas.create_oval(ball_centre_x - ball_radius, ball_centre_y - ball_radius, ball_centre_x + ball_radius,
                          ball_centre_y + ball_radius, fill=ball_color, outline="")

ball_1_centre_x = field_x + field_width / 2
ball_1_centre_y = field_y + field_height / 2
ball_1 = canvas.create_oval(ball_1_centre_x - ball_radius, ball_1_centre_y - ball_radius, ball_1_centre_x + ball_radius,
                            ball_1_centre_y + ball_radius, fill='black', outline="")

speed_x = 0
speed_y = 0
speed_1_x = 0
speed_1_y = 0
last_time = 0
acceleration = 100


def key(event):
    dcx, dcy, dc1x, dc1y = 0, 0, 0, 0

    if event.char == "w":
        dcy = -1
    elif event.char == "s":
        dcy = 1
    elif event.char == "a":
        dcx = -1
    elif event.char == "d":
        dcx = 1
    if event.keysym == "Up":
        dc1y = -1
    elif event.keysym == "Down":
        dc1y = 1
    elif event.keysym == "Left":
        dc1x = -1
    elif event.keysym == "Right":
        dc1x = 1
    elif event.char == "q":
        root.quit()

        return

    global speed_x, speed_y, speed_1_x, speed_1_y
    speed_x += acceleration * dcx
    speed_y += acceleration * dcy
    speed_1_x += acceleration * dc1x
    speed_1_y += acceleration * dc1y


def update():
    global last_time, ball_centre_x, ball_centre_y, speed_x, speed_y, ball_1_centre_x, ball_1_centre_y, speed_1_x, speed_1_y
    cur_time = time.time()
    if last_time:
        dt = cur_time - last_time

        dx = speed_x * dt
        dy = speed_y * dt
        ball_centre_x += dx
        ball_centre_y += dy

        dx1 = speed_1_x * dt
        dy1 = speed_1_y * dt
        ball_1_centre_x += dx1
        ball_1_centre_y += dy1

        if not (min_x <= ball_centre_x <= max_x):
            ball_centre_x = max(min_x, min(ball_centre_x, max_x))
            speed_x = -speed_x
        if not (min_y <= ball_centre_y <= max_y):
            ball_centre_y = max(min_y, min(ball_centre_y, max_y))
            speed_y = -speed_y

        if not (min_x <= ball_1_centre_x <= max_x):
            ball_1_centre_x = max(min_x, min(ball_1_centre_x, max_x))
            speed_1_x = -speed_1_x
        if not (min_y <= ball_1_centre_y <= max_y):
            ball_1_centre_y = max(min_y, min(ball_1_centre_y, max_y))
            speed_1_y = -speed_1_y

        canvas.coords(ball, ball_centre_x - ball_radius, ball_centre_y - ball_radius,
                      ball_centre_x + ball_radius, ball_centre_y + ball_radius)
        canvas.coords(ball_1, ball_1_centre_x - ball_radius, ball_1_centre_y - ball_radius,
                      ball_1_centre_x + ball_radius, ball_1_centre_y + ball_radius)

    last_time = cur_time

    root.after(1, update)


root.bind("<Key>", key)

update()
root.mainloop()
