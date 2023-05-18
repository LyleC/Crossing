from gymnasium.spaces import Sequence, Box

observation_space = Sequence(Box(0, 1))
print(observation_space)
print(observation_space.sample())
