import pygame
import numpy as np

"""
lane index:
  2
1   3
  0
block index:
1 2
0 3  
"""


class Ground:
    def __init__(self, num_lanes=(2, 2), size_pixel=800) -> None:
        self.size_pixel = size_pixel
        self.num_lanes = num_lanes
        self.lane_width_meter = 3.75
        self.lane_width_pixel = 50

        self.scale = self.lane_width_meter / self.lane_width_pixel

        self.binary_map = self._generate_binary_map()
        self.start_points = self._generate_start_points()

    def _generate_binary_map(self):
        binary = np.zeros((self.size_pixel, self.size_pixel), dtype=np.uint8)
        half_size = int(self.size_pixel / 2)

        self.h0 = half_size - self.num_lanes[0] * self.lane_width_pixel
        self.h1 = half_size + self.num_lanes[0] * self.lane_width_pixel
        self.w0 = half_size - self.num_lanes[1] * self.lane_width_pixel
        self.w1 = half_size + self.num_lanes[1] * self.lane_width_pixel

        binary[0 : self.h0, 0 : self.w0] = 1
        binary[self.h1 : self.size_pixel, 0 : self.w0] = 1
        binary[0 : self.h0, self.w1 : self.size_pixel] = 1
        binary[self.h1 : self.size_pixel, self.w1 : self.size_pixel] = 1
        return binary

    def _generate_start_points(self):
        start_points = []
        # 南北向车道
        for idx in range(self.num_lanes[0]):
            start_points.append((self.size_pixel / 2 - self.lane_width_pixel * (idx + 0.5), 0))
            start_points.append(
                (self.size_pixel / 2 + self.lane_width_pixel * (idx + 0.5), self.size_pixel)
            )
        # 东西向车道
        for idx in range(self.num_lanes[1]):
            start_points.append((0, self.size_pixel / 2 + self.lane_width_pixel * (idx + 0.5)))
            start_points.append(
                (self.size_pixel, self.size_pixel / 2 - self.lane_width_pixel * (idx + 0.5))
            )
        return start_points

    def render(self, canvas):
        # off-road area
        pygame.draw.rect(canvas, (0, 0, 0), pygame.Rect(0, 0, self.w0, self.h0))
        pygame.draw.rect(
            canvas, (0, 0, 0), pygame.Rect(0, self.h1, self.w0, self.size_pixel - self.h1)
        )
        pygame.draw.rect(
            canvas, (0, 0, 0), pygame.Rect(self.w1, 0, self.size_pixel - self.w1, self.h0)
        )
        pygame.draw.rect(
            canvas,
            (0, 0, 0),
            pygame.Rect(self.w1, self.h1, self.size_pixel - self.w1, self.size_pixel - self.h1),
        )
        # lane-line
        half_size = int(self.size_pixel / 2)
        pygame.draw.line(canvas, 0, (half_size, 0), (half_size, self.size_pixel), width=2)
        pygame.draw.line(canvas, 0, (0, half_size), (self.size_pixel, half_size), width=2)
        # start point
        for point in self.start_points:
            pygame.draw.circle(canvas, (0, 255, 255), point, 10)
        return canvas

    def onroad(self, x: int, y: int):
        if self.binary_map[y, x] > 0:
            return False
        else:
            return True

    def random_start_point(self):
        select = np.random.randint(len(self.start_points))
        return self.start_points[select]

    @property
    def size(self):
        return self.size_pixel
