from units.SI import meters, inches_to_meters

robot_width: meters = 35 * inches_to_meters
robot_length: meters = 35 * inches_to_meters

# Trajectory visualization settings
continuous = True
speeds = [0.5, 1.0, 2.0, 4.0, 8.0]
current_speed_index = 1
