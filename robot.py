import math

import pygame
from pygame.sprite import Sprite
from trajectories.config import robot_length, robot_width
from units.screen import meters_to_pixels, scale_to_pixels


class Robot:
    def __init__(self):
        self.image = pygame.Surface(meters_to_pixels(robot_width, robot_length))

        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)

        self.vertices = self.get_vertices()

    def set_position(self, x, y, angle):
        self.rect.center = scale_to_pixels(x, y)
        self.vertices = self.get_vertices()
        self.rotate_vertices(angle)

    def rotate_vertices(self, angle):
        new_vertices = []
        for vertex in self.vertices:
            x = vertex[0] - self.rect.center[0]
            y = vertex[1] - self.rect.center[1]

            new_x = x * math.cos(angle) - y * math.sin(angle)
            new_y = x * math.sin(angle) + y * math.cos(angle)

            vertex = (new_x + self.rect.center[0], new_y + self.rect.center[1])
            new_vertices.append(vertex)
        self.vertices = new_vertices

    def get_vertices(self):
        return [
            (self.rect.center[0] - self.rect.width / 2, self.rect.center[1] - self.rect.height / 2),
            (self.rect.center[0] + self.rect.width / 2, self.rect.center[1] - self.rect.height / 2),
            (self.rect.center[0] + self.rect.width / 2, self.rect.center[1] + self.rect.height / 2),
            (self.rect.center[0] - self.rect.width / 2, self.rect.center[1] + self.rect.height / 2)
        ]

    def draw(self, window):
        # Draw a border of rectangle
        vertices = self.vertices
        pygame.draw.polygon(window, (255, 0, 0), vertices, 1)


