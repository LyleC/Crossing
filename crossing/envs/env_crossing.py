import gymnasium as gym
import numpy as np
import pygame
from gymnasium import spaces

from .ground import Ground
from .vehicle import Vehicle


class CrossingEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 10}

    def __init__(self, render_mode=None):
        # TODO: 目前都用的默认值去初始化Ground
        self.ground = Ground()
        self.window_size = self.ground.size
        # TODO: 便于调试指定了自车的初始位置
        self.ego_veh = Vehicle(self.ground.start_points[0])
        # self.ego_veh = Vehicle(self.ground.random_start_point())

        # TODO: 观测空间目前只定义了自车
        self.observation_space = spaces.Dict(
            {
                "ego": spaces.Box(0, self.window_size, shape=(2,), dtype=int),
            }
        )
        # TODO: 动作空间目前是直接控制位置，更合理是控制加速度
        self.action_space = spaces.Discrete(4)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.window = None
        self.clock = None

    def _get_obs(self):
        return {"ego": self._agent_location}

    def _get_info(self):
        return {}

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)
        self._agent_location = self.ego_veh.location

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def step(self, action):
        self.ego_veh.drive(action)

        # TODO: 终止条件（1）车辆碰撞（2）车辆到达目的地
        terminated = None
        reward = 1 if terminated else 0  # Binary sparse rewards
        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((self.window_size, self.window_size))
        canvas.fill((255, 255, 255))

        canvas = self.ground.render(canvas)
        canvas = self.ego_veh.render(canvas)

        if self.render_mode == "human":
            # The following line copies our drawings from `canvas` to the visible window
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.transpose(np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2))

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
