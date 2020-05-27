balls_filename = 'balls.txt'

screen_width = 1980
screen_height = 1200

border_color = "#A52A2A"
field_color = "#013220"

indent_y = 20
intent_x = 50
border_width = 20

field_x = intent_x
field_y = intent_x + indent_y
field_width = screen_width - 2 * field_x
field_height = screen_height - 2 * field_y

last_time = 0
stop_speed = 0 #ball deceleration coefficient
#stop_speed = 0.0005
max_speed = 5
acceleration = 500


def board(canvas):
    canvas.pack()

    canvas.create_text(screen_width / 2, indent_y,
                       text="Use WASD to accelerate the white ball, to quit use Q")

    canvas.create_rectangle(field_x, field_y, field_x + field_width, field_y + field_height, fill=border_color,
                            outline="")

    canvas.create_rectangle(field_x + border_width, field_y + border_width, field_x + field_width - border_width,
                            field_y + field_height - border_width, fill=field_color, outline="")
