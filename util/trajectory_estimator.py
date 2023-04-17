from util.trajectory_generator import CustomTrajectory
from wpimath.trajectory import Trajectory


def estimate_duration(trajectory: Trajectory):
    """
    Estimates the duration of a trajectory
    :param trajectory: Trajectory
    :return: Duration of the trajectory
    """
    return trajectory.totalTime()


def estimate_auto_duration(trajectories: list[CustomTrajectory]):
    """
    Estimates the duration of a list of trajectories
    :param trajectories: List of trajectories
    :return: Duration of the trajectories
    """
    duration = 0
    for trajectory in trajectories:
        duration += estimate_duration(trajectory.trajectory)
    return duration
