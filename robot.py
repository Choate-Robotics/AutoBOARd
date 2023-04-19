import math

import pygame
from config import robot_length, robot_width
from units.screen import meters_to_pixels, scale_to_pixels


class Robot:
    def __init__(self):
        self.image = pygame.Surface(meters_to_pixels(robot_width, robot_length))

        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)

        self.angle = 0
        self.blue_team = False

    def set_position(self, x, y, angle):
        self.rect.center = scale_to_pixels(x, y)
        self.angle = angle

    def rotate_vertices(self, vertices, angle):
        new_vertices = []
        for vertex in vertices:
            x = vertex[0] - self.rect.center[0]
            y = vertex[1] - self.rect.center[1]

            new_x = x * math.cos(angle) - y * math.sin(angle)
            new_y = x * math.sin(angle) + y * math.cos(angle)

            vertex = (new_x + self.rect.center[0], new_y + self.rect.center[1])
            new_vertices.append(vertex)
        return new_vertices

    def get_vertices(self):
        return [
            (self.rect.center[0] - self.rect.width / 2, self.rect.center[1] - self.rect.height / 2),
            (self.rect.center[0] + self.rect.width / 2, self.rect.center[1] - self.rect.height / 2),
            (self.rect.center[0] + self.rect.width / 2, self.rect.center[1] + self.rect.height / 2),
            (self.rect.center[0] - self.rect.width / 2, self.rect.center[1] + self.rect.height / 2)
        ]

    def draw(self, window, location: tuple[float, float, float]):
        # Draw a border of rectangle
        self.set_position(*location)
        vertices = self.rotate_vertices(self.get_vertices(), self.angle)
        pygame.draw.polygon(window, (0 if self.blue_team else 255, 0, 255 if self.blue_team else 0), vertices, 3)


