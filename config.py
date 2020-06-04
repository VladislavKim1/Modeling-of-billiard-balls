balls_filename = 'billiard.json'

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

hole_cord: list = [
    (field_x + border_width + 10, field_y + border_width + 10),
    ((field_x + border_width + field_x + field_width - border_width) / 2, field_y + border_width),
    (field_x + field_width - border_width - 10, field_y + border_width + 10),
    (field_x + border_width + 10, field_y + field_height - border_width - 10),
    ((field_x + border_width + field_x + field_width - border_width) / 2, field_y + field_height - border_width),
    (field_x + field_width - border_width - 10, field_y + field_height - border_width - 10),
]

last_time = 0
stop_speed = 0.0009
max_speed = 5
acceleration = 500
