import constants

WINDOW_WIDTH = int(constants.FIELD_WIDTH_METERS * constants.SCALE_FACTOR)
WINDOW_HEIGHT = int(constants.FIELD_HEIGHT_METERS * constants.SCALE_FACTOR)


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
    new_x = round((x - x_offset) / scale, 3)
    new_y = round((WINDOW_HEIGHT - y - y_offset) / scale, 3)
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


def meters_to_pixels(x: float, y: float):
    """
    Scales the x and y coordinates from meters to pixels
    :param x: x position in meters
    :param y: y position in meters
    :return: x and y position in pixels
    """
    x_scale = WINDOW_HEIGHT / constants.FIELD_HEIGHT_METERS
    y_scale = WINDOW_WIDTH / constants.FIELD_WIDTH_METERS

    new_x = int(x * x_scale)
    new_y = int(y * y_scale)
    return new_x, new_y
