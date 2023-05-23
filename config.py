from units.SI import meters, inches_to_meters
from trajectories import *

robot_width: meters = 35 * inches_to_meters
robot_length: meters = 35 * inches_to_meters

# Trajectory visualization settings
continuous = True
speeds = [0.5, 1.0, 2.0, 4.0, 8.0, "instant"]
current_speed_index = 1

coords_list = [three_blue_no_guard, three_blue_guard, three_red_guard, link_guard_blue, red_three_balance, blue_three_balance]
coords_index = 0
