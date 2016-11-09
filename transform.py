import time
import sys
import os
import argparse
import copy

from PIL import Image, ImageDraw
from random import randint as _r


def random_change_in_range(old_value, random_rate, max_value, min_value):
    change_range = int(old_value * random_rate)
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
        self.a = _r(255 // 3, 255 * 2 // 3)

    def as_tuple(self):
        return self.r, self.g, self.b, self.a

    def __str__(self):
        return (" {}" * 4).format(self.r, self.g, self.b, self.a)

    def __repr__(self):
        return self.__str__()


class Circle:
    def __init__(self, image_size, mutate_speed=0.1, mutate_rate=50):
        self.max_range = image_size
        self.centre = (_r(0, image_size[0]), _r(0, image_size[1]))
        self.radius = min(abs(self.max_range[0] - self.centre[0]), abs(self.max_range[1] - self.centre[1]))
        self.mutate_speed = mutate_speed
        self.mutate_rate = mutate_rate

        self.color = Color(self.mutate_speed)

    def _mutate(self):
        self.centre = (
            random_change_in_range(self.centre[0], self.mutate_speed, self.max_range[0], 0),
            random_change_in_range(self.centre[1], self.mutate_speed, self.max_range[1], 0)
        )
        self.radius = random_change_in_range(self.radius, self.mutate_speed, max(self.max_range[0] - self.centre[0],
                                                                                 self.max_range[1] - self.centre[1]), 0)
        self.color.mutate()

    def mutate(self):
        mutated = self.is_mutable()
        if mutated:
            self._mutate()
        return mutated

    def is_mutable(self):
        return _r(0, 100) < self.mutate_rate

    def as_image(self):
        temp_image = Image.new("RGBA", self.max_range)
        draw = ImageDraw.Draw(temp_image)
        draw.ellipse(self.as_tuple(), fill=self.color.as_tuple())
        return temp_image

    def as_tuple(self):
        return self.centre[0], self.centre[1], self.centre[0] + self.radius, self.centre[1] + self.radius

    def __str__(self):
        return "{}   radius:{}".format(self.centre, self.radius)

    def __repr__(self):
        return self.__str__()


# *--------->x
# |
# |
# |
# |
# |
# v
# y


class PixelImage:
    def __init__(self, image_size, circle_nums=100, mutate_speed=0.1, mutate_rate=50):
        self.image_size = image_size
        self.pixels = []
        self.image = None
        self.mutate_speed = mutate_speed
        self.mutate_rate = mutate_rate

        self.circles = [Circle(image_size, mutate_speed, mutate_rate) for _ in range(circle_nums)]

    def born_a_child(self):
        # make a copy
        child = copy.deepcopy(self)
        # if no one mutate
        return child

    def mutate(self):
        counter = 0
        for circle in self.circles:
            counter += 1 if circle.mutate() else 0

        if counter == 0:
            self.circles[0]._mutate()

    def get_pixels(self):
        temp_image = Image.new('RGBA', self.image_size)
        for circle in self.circles:
            temp_image = Image.alpha_composite(temp_image, circle.as_image())

        self.image = temp_image

        pixels = [self.image.getpixel((x, y)) for y in range(self.image.size[1]) for x in range(temp_image.size[0])]
        return pixels

    def save_as_img(self, path, name):
        name += '.png'
        path = os.path.realpath(path)
        self.image.save(os.path.join(path, name))


class Transform:
    def __init__(self, target, output_path, max_loop=10240, save_pre_loop=1000, circle_nums=100, mutate_speed=0.1,
                 mutate_rate=10):
        self.target = Image.open(target).resize((128, 128)).convert('RGBA')
        self.output_path = output_path
        self.max_loop = max_loop
        self.save_pre_loop = save_pre_loop

        self.circle_nums = circle_nums
        self.mutate_speed = mutate_speed
        self.mutate_rate = mutate_rate

        self.target_pixels = [self.target.getpixel((x, y)) for y in range(self.target.size[1]) for x in
                              range(self.target.size[0])]

    def compare_pixel(self, pixels):
        if len(pixels) != len(self.target_pixels):
            raise Exception("Pixels nums not equal")
        ret = 0
        for index in range(len(self.target_pixels)):
            dr = self.target_pixels[index][0] - pixels[index][0]
            dg = self.target_pixels[index][1] - pixels[index][1]
            db = self.target_pixels[index][2] - pixels[index][2]
            ret += dr * dr + dg * dg + db * db
        return ret

    def main(self):
        parent = PixelImage(self.target.size, self.circle_nums, self.mutate_speed, self.mutate_rate)
        counter = 0

        while True:
            if counter > self.max_loop:
                break

            child = parent.born_a_child()

            child.mutate()

            self.parent = parent
            self.child = child

            parent_diff = self.compare_pixel(parent.get_pixels())
            child_diff = self.compare_pixel(child.get_pixels())

            print("Loop:{} \t\t Score Parent:{} \t\t Child: {}".format(counter, parent_diff, child_diff))

            if counter % self.save_pre_loop == 0:
                parent.save_as_img(self.output_path, str(counter))

            if child_diff < parent_diff:
                parent = child

            counter += 1


def main():
    MAX_LOOP = 102400
    SAVE_PRE_LOOP = 1000
    MUTATE_RATE = 10
    MUTATE_SPEED = 0.1
    CIRCLE_NUMS = 100

    parser = argparse.ArgumentParser()
    parser.add_argument('target', help='the image to transform')
    parser.add_argument('output', help='the folder to store result')
    parser.add_argument('--max_loop', help='the max loop nums of transform', type=int)
    parser.add_argument('--save_pre_loop', help='save the temp result pre loop', type=int)
    parser.add_argument('--mutate_rate', help='the rate of mutate MUTATE_RATE, percent', type=int)
    parser.add_argument('--mutate_speed', help='the mutate speed of every mutate', type=float)
    parser.add_argument('--circle_nums', help='numbers of circles to fit the image', type=int)
    args = parser.parse_args()

    TARGET = args.target
    OUTPUT = args.output
    MAX_LOOP = args.max_loop or MAX_LOOP
    SAVE_PRE_LOOP = args.save_pre_loop or SAVE_PRE_LOOP
    MUTATE_RATE = args.mutate_rate or MUTATE_RATE
    MUTATE_SPEED = args.mutate_speed or MUTATE_SPEED
    CIRCLE_NUMS = args.circle_nums or CIRCLE_NUMS

    transformater = Transform(TARGET, OUTPUT, max_loop=MAX_LOOP, save_pre_loop=SAVE_PRE_LOOP, mutate_rate=MUTATE_RATE,
                              circle_nums=CIRCLE_NUMS, mutate_speed=MUTATE_SPEED)
    print("""Max Loop: {} \t Save Pre Loop: {} \t Mutate Rate: {} \t Circle Nums: {} \t Mutate Speed: {}""".format(
        MAX_LOOP, SAVE_PRE_LOOP, MUTATE_RATE, CIRCLE_NUMS, MUTATE_SPEED))
    transformater.main()


if __name__ == '__main__':
    main()
