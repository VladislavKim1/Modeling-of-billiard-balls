import json

from ball import Ball, root
from hole import Hole
from config import hole_cord
from update import update, last_time


def test_coord():
    global last_time

    holes: list = list()
    for coord in hole_cord:
        holes.append(Hole(coord))

    ########################################
    #   CONST
    ########################################
    dt = 0.001  # (DEFAULT: 0.001) If set to 'none', then the calculation will depend on the processor.
    SPEED_PLAYER: int = 5000
    COORD: list = [
        {'x': 749.1037356209815, 'y': 400.0},
        {'x': 737.4778075654237, 'y': 518.4374639103951},
        {'x': 841.6458133769794, 'y': 296.7989203069272},
        {'x': 834.1708522543635, 'y': 534.2549155340065},
        {'x': 918.795265395989, 'y': 387.5792773227268},
        {'x': 924.1263862601234, 'y': 444.9924739563589},
        {'x': 906.6978983363924, 'y': 263.33987765061704},
        {'x': 886.699359748491, 'y': 522.0441045696581},
        {'x': 980.8492405433761, 'y': 435.93334702264514},
        {'x': 971.2759021415388, 'y': 372.77205010294244},
        {'x': 981.3676568055325, 'y': 313.51423648206907},
        {'x': 742.44247267777, 'y': 241.66676006285635},
        {'x': 1062.1638977248808, 'y': 343.8689652863846},
        {'x': 1087.6745239649977, 'y': 412.3710284138871},
        {'x': 1040.0, 'y': 455.0},
        {'x': 961.9666736738287, 'y': 670.3627325102416}
    ]

    ########################################
    #   Generate balls
    ########################################
    balls: list = list()
    with open('balls.json') as f:
        for ball_name, struct in json.load(f).items():
            balls.append(Ball(struct['position'], struct['color'], struct['radius'], balls))

    ########################################
    #   Move player
    ########################################
    player: Ball = balls[0]
    player.speed_x = SPEED_PLAYER

    ########################################
    #   Check speed
    ########################################
    speed: bool = True
    while speed:
        last_time, balls = update(last_time, balls, dt)

        count_ball: int = 0
        for ball in balls:
            if not(round(ball.speed_x, 3) or round(ball.speed_y, 3)):
                count_ball += 1

        if count_ball == len(balls):
            speed = False

    ########################################
    #   Check location ball
    ########################################
    buf: float = 0.0
    for i, ball in enumerate(balls):
        # relative error
        sigma_x = (abs(COORD[i]['x'] - ball.location['x']) / ball.location['x']) * 100
        sigma_y = (abs(COORD[i]['y'] - ball.location['y']) / ball.location['y']) * 100
        print(f'x: {round(sigma_x, 1)} %, y: {round(sigma_y, 1)} %')
        buf += sigma_x + sigma_y

    # Average
    A = round(buf / (len(balls) * 2), 1)
    print(f'{A} %')
    assert 0.0 == A


if __name__ == '__main__':
    test_coord()
