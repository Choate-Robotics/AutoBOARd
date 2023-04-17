import pygame
import constants
from util.trajectory_generator import CustomTrajectory, gen_trajectories
from util.trajectory_estimator import estimate_auto_duration
from trajectories.coords import coords_list

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


def scale_to_meters(x, y):
    """
    Scales the x and y coordinates from pixels to meters
    :param x: x position in pixels
    :param y: y position in pixels
    :return: x and y position in meters
    """
    scale = WINDOW_HEIGHT / constants.FIELD_HEIGHT_METERS

    x_offset = (WINDOW_WIDTH - scale * constants.FIELD_WIDTH_METERS) / 2
    y_offset = 0
    new_x = ((x - x_offset) / scale)
    new_y = ((WINDOW_HEIGHT - y - y_offset) / scale)
    return new_x, new_y


def scale_to_pixels(x: float, y: float):
    """
    Scales the x and y coordinates from meters to pixels
    :param x: x position in meters
    :param y: y position in meters
    :return: x and y position in pixels
    """
    scale = WINDOW_HEIGHT / constants.FIELD_HEIGHT_METERS

    x_offset = (WINDOW_WIDTH - scale * constants.FIELD_WIDTH_METERS) / 2
    y_offset = 0
    new_x = int(x * scale + x_offset)
    new_y = int(WINDOW_HEIGHT - (y * scale + y_offset))
    return new_x, new_y


def draw_point(window, x: float, y: float, color: tuple = (255, 0, 0)):
    """
    Draws a point on the field
    :param window: Pygame window
    :param x: x position in meters
    :param y: y position in meters
    :param color: Color of the point
    """
    pygame.draw.circle(window, color, scale_to_pixels(x, y), 3)


def draw_trajectory(window, trajectory: CustomTrajectory):
    """
    Draws a trajectory on the field
    :param window: Pygame window
    :param trajectory: Trajectory
    """
    global current_color
    color = colors_list[current_color % len(colors_list)]

    for state in trajectory.trajectory.states():
        draw_point(window, state.pose.x, state.pose.y, color)

    current_color += 1


def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    window.blit(scaled_field_image, (0, 0))

    trajectories = gen_trajectories(coords_list)

    print(estimate_auto_duration(trajectories))

    for trajectory in trajectories:
        draw_trajectory(window, trajectory)

    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == "__main__":
    main()
