from wpimath.geometry import Pose2d, Translation2d

from coords import (
    come_back_with_first_cube,
    come_back_with_second_cube,
    go_get_first_cube,
    go_get_second_cube,
)
from util.trajectory_generator import CustomTrajectory
from units.SI import meters_per_second, meters_per_second_squared

max_vel: meters_per_second = 4.5
max_accel: meters_per_second_squared = 3.3


CustomTrajectory(
    start_pose=Pose2d(*go_get_first_cube[0]),
    waypoints=[Translation2d(*x) for x in go_get_first_cube[1]],
    end_pose=Pose2d(*go_get_first_cube[2]),
    max_velocity=max_vel,
    max_accel=max_accel,
    start_velocity=0,
    end_velocity=0,
)
