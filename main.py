import asyncio
import time

import pygame

import config
import constants
from units.path import path
from util.trajectory_generator import CustomTrajectory, gen_trajectories
from util.trajectory_estimator import estimate_auto_duration
from trajectories.coords import coords_list
from units.screen import scale_to_pixels, scale_to_meters

from robot import Robot
from button import Button, OptionList, Toggle

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

current_color = 0
previous_rect = pygame.rect.Rect(0, 0, 0, 0)
previous_time_rect = pygame.rect.Rect(0, 0, 0, 0)
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


def animate_trajectory(window, trajectory: tuple[CustomTrajectory, path], speed: float = 1.0, continuous: bool = False, display_start_time=0):
    """
    Animates a trajectory on the field
    :param window: Pygame window
    :param trajectory: Trajectory
    :param speed: Speed of the animation
    :param continuous: Whether to draw a continuous curve
    :param display_start_time: Time to display the start time for
    """
    global current_color
    color = colors_list[current_color % len(colors_list)]

    draw_waypoint(window, trajectory[1][0][0], trajectory[1][0][1], color)
    for point in trajectory[1][1]:
        draw_waypoint(window, point[0], point[1], color)
    draw_waypoint(window, trajectory[1][2][0], trajectory[1][2][1], color)

    old_window = window.copy()

    start_time = time.time()
    last_display_time = 0

    if continuous:
        while time.time() - start_time < trajectory[0].trajectory.totalTime() / speed:
            current_state = trajectory[0].trajectory.sample((time.time() - start_time) * speed)
            window.blit(old_window, (0, 0))
            draw_point(window, current_state.pose.x, current_state.pose.y, color)

            display_time = (time.time() - start_time) * speed + display_start_time

            if display_time - last_display_time >= 0.1:
                display_current_time(window, display_time)
                last_display_time = display_time

            old_window = window.copy()

            robot.draw(window, (current_state.pose.x, current_state.pose.y, 0))

            pygame.display.update()
    else:
        for state in trajectory[0].trajectory.states():
            window.blit(old_window, (0, 0))
            draw_point(window, state.pose.x, state.pose.y, color)

            display_time = (time.time() - start_time) * speed + display_start_time

            if display_time - last_display_time >= 0.1:
                display_current_time(window, display_time)
                last_display_time = display_time

            old_window = window.copy()

            robot.draw(window, (state.pose.x, state.pose.y, 0))

            pygame.display.update()
            time.sleep(max(0, state.t - ((time.time() - start_time) * speed)))

    window.blit(old_window, (0, 0))

    current_color += 1


def display_current_time(window, time_to_display):
    """
    Displays the current time on the field
    :param window: Pygame window
    :param time_to_display: Time to display
    """
    display_time(window, str(round(time_to_display, 3)))


def display_data(window, coord, data, previous=None):
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

    window.blit(text, scale_to_pixels(coord[0], coord[1]))
    pygame.display.update()


def display_coords(screen, coords):
    global previous_rect
    display_data(screen, (2, 7.5), f"({coords[0]}, {coords[1]})", previous_rect)


def display_time(screen, data):
    global previous_time_rect
    display_data(screen, (12.5, 7), data, previous_time_rect)


def run_trajectories(window):
    trajectories, buttons = setup(window)

    start_time = time.time()

    for trajectory in trajectories:
        animate_trajectory(window, trajectory, speed=config.speeds[config.current_speed_index], continuous=config.continuous, display_start_time=time.time() - start_time)


def toggle_continuous():
    config.continuous = not config.continuous


def cycle_speed():
    config.current_speed_index = (config.current_speed_index + 1) % len(config.speeds)


def setup(window):
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    window.blit(scaled_field_image, (0, 0))

    trajectories = gen_trajectories(coords_list)

    display_data(
        window,
        (12.5, 7.5),
        "Estimated Auto Duration: " + str(round(estimate_auto_duration(trajectories), 2)) + "s"
    )

    # Add buttons
    buttons = []

    run_button = Button(100, 50, 80, 40, (255, 255, 255), "Run", action=lambda: run_trajectories(window))
    run_button.draw(window)

    buttons.append(run_button)

    continuous_toggle = Toggle(100, 100, 80, 40, (255, 255, 255), text="Continuous", font_size=16, start_state=config.continuous, action=toggle_continuous)
    continuous_toggle.draw(window)

    buttons.append(continuous_toggle)

    speeds_list = OptionList(100, 150, 80, 40, (255, 255, 255), states=["0.5x", "1x", "2x", "4x", "8x"], start_state=config.current_speed_index, font_size=16, action=cycle_speed)
    speeds_list.draw(window)

    buttons.append(speeds_list)

    return trajectories, buttons


def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    trajectories, buttons = setup(window)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.is_clicked(mouse_pos):
                        button.click(surface=window)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    trajectories, buttons = setup(window)

        user_coords = pygame.mouse.get_pos()
        display_coords(window, scale_to_meters(*user_coords))

        pygame.display.update()

        pygame.time.wait(10)

    pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
