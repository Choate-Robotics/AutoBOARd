import pygame
import constants

is_blue_alliance = True

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


def scale_to_meters(mouse_pos_pixels):
    if is_blue_alliance:
        scale = WINDOW_HEIGHT / constants.FIELD_HEIGHT_METERS
        x_offset = (WINDOW_WIDTH - scale * constants.FIELD_WIDTH_METERS) / 2
        y_offset = 0
        new_x = (mouse_pos_pixels[0] - x_offset) / scale
        new_y = (WINDOW_HEIGHT - mouse_pos_pixels[1] - y_offset) / scale
        return new_x, new_y


def scale_to_pixels(x, y):
    if is_blue_alliance:
        scale = WINDOW_HEIGHT / constants.FIELD_HEIGHT_METERS
        x_offset = (WINDOW_WIDTH - scale * constants.FIELD_WIDTH_METERS) / 2
        y_offset = 0
        new_x = int(x * scale + x_offset)
        new_y = int(WINDOW_HEIGHT - (y * scale + y_offset))
        return new_x, new_y


def draw_point(x, y):
    pygame.draw.circle(window, (255, 0, 0), (int(x), int(y)), 10)


# BLUE CABLE GUARD 3 PIECE COORDS
initial_x = 1.55
initial_y = 0.51
draw_point(*scale_to_pixels(initial_x, initial_y))
draw_point(*scale_to_pixels(initial_x + 5.25, initial_y + 0.43))

pygame.display.update()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
