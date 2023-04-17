import pygame
import constants

is_blue_alliance = False

WINDOW_WIDTH = int(constants.FIELD_WIDTH_METERS * constants.SCALE_FACTOR)
WINDOW_HEIGHT = int(constants.FIELD_HEIGHT_METERS * constants.SCALE_FACTOR)

# Charged up field image
field_image = pygame.image.load("./images/field.png")
scaled_field_image = pygame.transform.scale(
    field_image,
    (WINDOW_WIDTH, WINDOW_HEIGHT)
)

# Set up Pygame window
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
window.blit(scaled_field_image, (0, 0))


def scale_to_meters(x, y):
    """
    Scales the x and y coordinates from pixels to meters
    :param x: x position in pixels
    :param y: y position in pixels
    :return: x and y position in meters
    """
    scale = WINDOW_HEIGHT / constants.FIELD_HEIGHT_METERS

    # WORKING FOR BLUE
    if is_blue_alliance:
        x_offset = (WINDOW_WIDTH - scale * constants.FIELD_WIDTH_METERS) / 2
        y_offset = 0
        new_x = ((x - x_offset) / scale)
        new_y = ((WINDOW_HEIGHT - y - y_offset) / scale)
        return new_x, new_y
    else:  # lol idk
        x_offset = (WINDOW_WIDTH - scale * constants.FIELD_WIDTH_METERS) / 2 + WINDOW_WIDTH
        y_offset = WINDOW_HEIGHT
        new_x = ((x - x_offset) / scale)
        new_y = ((WINDOW_HEIGHT - y - y_offset) / scale)
        return -new_x, -new_y


def scale_to_pixels(x: float, y: float):
    """
    Scales the x and y coordinates from meters to pixels
    :param x: x position in meters
    :param y: y position in meters
    :return: x and y position in pixels
    """
    scale = WINDOW_HEIGHT / constants.FIELD_HEIGHT_METERS

    #  WORKING FOR BLUE
    if is_blue_alliance:
        x_offset = (WINDOW_WIDTH - scale * constants.FIELD_WIDTH_METERS) / 2
        y_offset = 0
        new_x = int(x * scale + x_offset)
        new_y = int(WINDOW_HEIGHT - (y * scale + y_offset))
        return new_x, new_y
    else:  # je ne sais pas
        x_offset = (WINDOW_WIDTH - scale * constants.FIELD_WIDTH_METERS) / 2 + WINDOW_WIDTH
        y_offset = WINDOW_HEIGHT
        new_x = int(x * scale - x_offset)
        new_y = int(WINDOW_HEIGHT - y + y_offset) * scale
        return -new_x, new_y


def draw_point(x: float, y: float):
    """
    Draws a point on the field
    :param x: x position in meters
    :param y: y position in meters
    """
    pygame.draw.circle(window, (255, 0, 0), scale_to_pixels(x, y), 10)


if is_blue_alliance:
    initial_x = 1.55
    initial_y = 0.51
    draw_point(initial_x, initial_y)
    draw_point(initial_x + 5.25, initial_y + 0.43)
else:
    initial_x = 1.55
    initial_y = 7.495
    draw_point(initial_x, initial_y)
    draw_point(initial_x + 5.25, initial_y - 0.43)

pygame.display.update()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        print((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))

pygame.quit()
