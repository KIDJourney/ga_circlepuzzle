import getopt
import time
import sys
import os

from PIL import Image, ImageDraw
from random import randint as _r


def random_change_in_range(old_value, random_rate, max_value, min_value):
    change_range = old_value * random_rate
    new_value = old_value + _r(-change_range, change_range)
    new_value = max(min_value, min(max_value, new_value))
    return new_value


class Color:
    def __init__(self, mutate_speed=0.1):
        self.r = _r(0, 255)
        self.g = _r(0, 255)
        self.b = _r(0, 255)
        self.a = _r(0, 255)
        self.mutate_speed = mutate_speed

    def mutate(self):
        for attr in ['r', 'g', 'b', 'a']:
            new_value = random_change_in_range(getattr(self, attr), self.mutate_speed, 255, 0)
            setattr(self, attr, new_value)


class Circel:
    def __init__(self, max_range, mutate_speed=0.1, mutate_rate=50):
        self.max_range = max_range
        self.centre = (_r(0, max_range[0]), _r(0, max_range[1]))
        self.radius = min(abs(self.max_range[0] - self.centre[0]), abs(self.max_range[1] - self.centre[1]))
        self.mutate_speed = mutate_speed
        self.mutate_rate = mutate_rate

        self.color = Color(self.mutate_speed)

    def _mutate(self):
        self.centre = (
            random_change_in_range(self.centre[0], self.mutate_speed, self.max_range[0], 0),
            random_change_in_range(self.centre[1], self.mutate_speed, self.max_range[1], 0)
        )
        self.color.mutate()

    def mutate(self):
        pass

    def is_mutable(self):
        return _r(0, 100) < self.mutate_rate


class Transform:
    def __init__(self, target, output_path, circel_nums=100, max_loop=10240):
        self.target = Image.open(target)
        self.output_path = output_path
        self.circel_nums = circel_nums
        self.max_loop = 10240
