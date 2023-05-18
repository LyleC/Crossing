import pygame
import numpy as np


class Vehicle:
    def __init__(self, start_pos, color=(255, 0, 0)) -> None:
        self.pos = np.array(start_pos)
        self.color = color
        self._action_to_direction = {
            0: np.array([1, 0]),
            1: np.array([0, 1]),
            2: np.array([-1, 0]),
            3: np.array([0, -1]),
        }

    def drive(self, action: int):
        move = self._action_to_direction[action]
        self.pos += move

    def _generate_rect(self):
        width = 20
        height = 20
        left = self.pos[0] - width / 2
        top = self.pos[1] - width / 2
        return left, top, width, height

    def render(self, canvas):
        pygame.draw.rect(canvas, self.color, pygame.Rect(*self._generate_rect()))
        return canvas

    @property
    def location(self):
        return self.pos
