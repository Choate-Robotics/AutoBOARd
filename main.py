import time

import pygame
import constants
from units.path import path
from util.trajectory_generator import CustomTrajectory, gen_trajectories
from util.trajectory_estimator import estimate_auto_duration
from trajectories.coords import coords_list
from units.screen import scale_to_pixels, scale_to_meters

from robot import Robot

WINDOW_WIDTH = int(constants.FIELD_WIDTH_METERS * constants.SCALE_FACTOR)
WINDOW_HEIGHT = int(constants.FIELD_HEIGHT_METERS * constants.SCALE_FACTOR)

# Charged up field image
field_image = pygame.image.load("./images/field.png")
scaled_field_image = pygame.transform.scale(
    field_image,
    (WINDOW_WIDTH, WINDOW_HEIGHT)
)

colors_list = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
]

global current_color
current_color = 0
global previous_rect
previous_rect = None
global robot
robot = Robot()


def draw_point(window, x: float, y: float, color: tuple = (255, 0, 0), radius: int = 1):
    """
    Draws a point on the field
    :param window: Pygame window
    :param x: x position in meters
    :param y: y position in meters
    :param color: Color of the point
    :param radius: Radius of the point
    """
    pygame.draw.circle(window, color, scale_to_pixels(x, y), radius)


def draw_waypoint(window, x: float, y: float, color: tuple = (255, 0, 0)):
    """
    Draws a waypoint on the field
    :param window: Pygame window
    :param x: x position in meters
    :param y: y position in meters
    :param color: Color of the point
    """
    pygame.draw.rect(window, color, (scale_to_pixels(x, y)[0] - 5, scale_to_pixels(x, y)[1] - 5, 10, 10))


def draw_trajectory(window, trajectory: tuple[CustomTrajectory, path]):
    """
    Draws a trajectory on the field
    :param window: Pygame window
    :param trajectory: Trajectory
    """
    global current_color
    color = colors_list[current_color % len(colors_list)]

    for state in trajectory[0].trajectory.states():
        draw_point(window, state.pose.x, state.pose.y, color)

    draw_waypoint(window, trajectory[1][0][0], trajectory[1][0][1], color)
    for point in trajectory[1][1]:
        draw_waypoint(window, point[0], point[1], color)
    draw_waypoint(window, trajectory[1][2][0], trajectory[1][2][1], color)

    current_color += 1


def animate_trajectory(window, trajectory: tuple[CustomTrajectory, path], speed: float = 1.0, continuous: bool = False):
    """
    Animates a trajectory on the field
    :param window: Pygame window
    :param trajectory: Trajectory
    :param speed: Speed of the animation
    :param continuous: Whether to draw a continuous curve
    """


    global current_color
    color = colors_list[current_color % len(colors_list)]

    draw_waypoint(window, trajectory[1][0][0], trajectory[1][0][1], color)
    for point in trajectory[1][1]:
        draw_waypoint(window, point[0], point[1], color)
    draw_waypoint(window, trajectory[1][2][0], trajectory[1][2][1], color)

    old_window = window.copy()

    start_time = time.time()

    if continuous:
        while time.time() - start_time < trajectory[0].trajectory.totalTime() / speed:
            current_state = trajectory[0].trajectory.sample((time.time() - start_time) * speed)

            window.blit(old_window, (0, 0))
            draw_point(window, current_state.pose.x, current_state.pose.y, color)
            old_window = window.copy()

            robot.set_position(current_state.pose.x, current_state.pose.y, 0)

            robot.draw(window)

            pygame.display.update()
    else:
        for state in trajectory[0].trajectory.states():
            window.blit(old_window, (0, 0))
            draw_point(window, state.pose.x, state.pose.y, color)
            old_window = window.copy()

            robot.set_position(state.pose.x, state.pose.y, 0)
            robot.draw(window)

            pygame.display.update()
            time.sleep(max(0, state.t - ((time.time() - start_time) * speed)))

    window.blit(old_window, (0, 0))

    current_color += 1


def display_data(window, coord, data, previous=False):
    """
    Displays data on the field
    :param window: Pygame window
    :param coord: Coordinate to display the data at
    :param data: Data to display
    :param previous: Whether to clear the previous coords
    """
    font = pygame.font.SysFont("Arial", 20)
    text = font.render(data, True, (255, 0, 0))

    text_rect = text.get_rect()
    # Draw a rectangle to cover the previous text
    global previous_rect

    if previous:
        if previous_rect is not None:
            pygame.draw.rect(
                window,
                (0, 0, 0),
                (
                    scale_to_pixels(coord[0], coord[1])[0],
                    scale_to_pixels(coord[0], coord[1])[1],
                    previous_rect.width,
                    previous_rect.height
                )
            )
        else:
            pygame.draw.rect(
                window,
                (0, 0, 0),
                (
                    scale_to_pixels(coord[0], coord[1])[0],
                    scale_to_pixels(coord[0], coord[1])[1],
                    text_rect.width,
                    text_rect.height
                )
            )
        previous_rect = text_rect
    else:
        pygame.draw.rect(
            window,
            (0, 0, 0),
            (
                scale_to_pixels(coord[0], coord[1])[0],
                scale_to_pixels(coord[0], coord[1])[1],
                text_rect.width,
                text_rect.height
            )
        )

    window.blit(text, scale_to_pixels(coord[0], coord[1]))
    pygame.display.update()


def display_coords(screen, coords):
    global previous_rect
    display_data(screen, (2, 7.5), f"({coords[0]}, {coords[1]})", True)


def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    window.blit(scaled_field_image, (0, 0))

    robot_layer = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    robot_layer.fill((0, 0, 0, 0))
    window.blit(robot_layer, (0, 0))

    trajectories = gen_trajectories(coords_list)

    print(estimate_auto_duration(trajectories))
    display_data(
        window,
        (12.5, 7.5),
        "Estimated Auto Duration: " + str(round(estimate_auto_duration(trajectories), 2)) + "s"
    )

    for trajectory in trajectories:
        animate_trajectory(window, trajectory, speed=1.0, continuous=True)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        user_coords = pygame.mouse.get_pos()
        display_coords(window, scale_to_meters(*user_coords))

        pygame.display.update()

        pygame.time.wait(10)

    pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
