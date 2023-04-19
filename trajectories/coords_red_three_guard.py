from units.SI import meters, radians
from units.path import coord, waypoints, path, vel_accel

blue_team = False

initial: coord = (1.55, 7.5, 0)

go_get_first_cube: path = (
    initial,
    [],
    (initial[0] + 5.25, initial[1] - 0.43, 0),
    (4.5, 3.3),
    False
)

come_back_with_first_cube: path = (
    go_get_first_cube[2],
    [(initial[0] + 2.42, initial[1] - 0.25)],
    (initial[0] + 0.05, initial[1] - 0.55, 0),
    (3.7, 2.3),
    True
)

go_get_second_cube: path = (
    come_back_with_first_cube[2],
    [
        (initial[0] + 1.85, initial[1] - 0.27),
        (initial[0] + 3.3, initial[1] - 0.24),
        (initial[0] + 4.2, initial[1] - 0.38),
        (initial[0] + 4.6, initial[1] - 1.6),
    ],
    (initial[0] + 5.79, initial[1] - 1.7, 0),
    (4, 2.5),
    False
)

come_back_with_second_cube: path = (
    go_get_second_cube[2],
    [
        (initial[0] + 4.4, initial[1] - 0.38),
        (initial[0] + 3.3, initial[1] - 0.2),
        (initial[0] + 1.85, initial[1] - 0.27),
    ],
    (initial[0] + 0, initial[1] - 0.55, 0),
    (3.6, 2.6),
    True
)


coords_list = ([go_get_first_cube, come_back_with_first_cube, go_get_second_cube, come_back_with_second_cube], "Three Red Guard", blue_team)
