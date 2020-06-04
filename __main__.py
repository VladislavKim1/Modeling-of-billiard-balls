from ball import balls, canvas, root
from config import *
# from config_test import *
from update import update, start_balls, make_holes


def key(event):
    for ball in balls:
        ball.control(event)


def main():
    canvas.pack()

    text = canvas.create_text(screen_width / 2, indent_y - 10,
                              text="Use WASD to accelerate the white ball, to quit use Q")

    border = canvas.create_rectangle(field_x, field_y, field_x + field_width, field_y + field_height, fill=border_color,
                                     outline="")

    field = canvas.create_rectangle(field_x + border_width, field_y + border_width, field_x + field_width - border_width,
                                    field_y + field_height - border_width, fill=field_color, outline="")

    root.bind("<Key>", key)

    make_holes()
    update(last_time, start_balls(), root)
    root.mainloop()


if __name__ == '__main__':
    main()


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

