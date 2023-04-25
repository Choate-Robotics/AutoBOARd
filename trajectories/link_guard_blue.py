from units.SI import meters, radians
from units.path import coord, waypoints, path, vel_accel

blue_team = True

initial: coord = (1.55, 1.63, 0)

go_get_first_cube: path = (
    initial,
    [(initial[0] + .6, initial[1] - .6)],
    (initial[0] + 5.38, initial[1] - .67, 0),
    (4.5, 3.3),
    False
)

come_back_with_first_cube: path = (
    go_get_first_cube[2],
    [(initial[0] + 2.42, initial[1] - .87)],
    (initial[0] + 0.05, initial[1] - 1.12, 0),
    (4.5, 3.3),
    True
)

go_get_second_cube: path = (
    come_back_with_first_cube[2],
    [
        (initial[0] + 1.85, initial[1] - 0.87),
        (initial[0] + 4.8, initial[1] - 0.64),
        (initial[0] + 6.2, initial[1] + .53),
    ],
    (initial[0] + 5, initial[1] + .53, 0),
    (4.5, 3.3),
    False
)

come_back_with_second_cube: path = (
    go_get_second_cube[2],
    [
        (initial[0] + 4.2, initial[1] - 0.64),
        (initial[0] + 1.85, initial[1] - 0.80),
    ],
    (initial[0] + 0, initial[1] - .56, 0),
    (4.5, 3.3),
    True
)

coords_list = ([go_get_first_cube, come_back_with_first_cube, go_get_second_cube, come_back_with_second_cube], "Link Guard Blue", blue_team)
