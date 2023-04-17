from units.SI import meters, radians
from units.path import coord, waypoints, path, vel_accel

blue_team = True

initial: coord = (1.55, 0.51, 0)

go_get_first_cube: path = (
    initial,
    [],
    (initial[0] + 5.25, initial[1] + 0.43, 0),
    (4.5, 3.3)
)

come_back_with_first_cube: path = (
    go_get_first_cube[2],
    [(initial[0] + 2.42, initial[1] + 0.25)],
    (initial[0] + 0.05, initial[1] + 0.65, 0),
    (3.7, 2.3)
)

go_get_second_cube: path = (
    come_back_with_first_cube[2],
    [
        (initial[0] + 1.85, initial[1] + 0.28),
        (initial[0] + 3.3, initial[1] + 0.23),
        (initial[0] + 4.1, initial[1] + 0.25),
    ],
    (initial[0] + 5.79, initial[1] + 1.83, 0),
    (4, 2.5)
)

come_back_with_second_cube: path = (
    go_get_second_cube[2],
    [
        (initial[0] + 4.1, initial[1] + 0.25),
        (initial[0] + 3.3, initial[1] + 0.23),
        (initial[0] + 1.85, initial[1] + 0.28),
    ],
    (initial[0] + 0, initial[1] + 0.7, 0),
    (3.6, 2.6)
)

coords_list = [go_get_first_cube, come_back_with_first_cube, go_get_second_cube, come_back_with_second_cube]
