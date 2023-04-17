from units.SI import meters, radians, meters_per_second, meters_per_second_squared

coord = (meters, meters, radians)
waypoints = [(meters, meters)]
vel_accel = (meters_per_second, meters_per_second_squared)
path = (coord, waypoints, coord, vel_accel)
