import math
from random import uniform, random


class Unit:

    def __init__(self, coords: dict, rotation: float, destiny, bases: list, index: int, image, contains: dict,
                 distance, speed: float):
        self.coords = coords
        self.destiny = destiny
        self.rotation = rotation
        self.points = dict({*map(lambda x: (x, distance + 1), bases)})
        self.index = index
        self.image = image
        self.contains = contains
        self.distance = distance
        self.speed = speed

    def listen(self, unit, key):
        if self.points[key] > unit.points[key] + self.distance:
            self.points[key] = unit.points[key] + self.distance

            if key == self.destiny:
                dx = unit.coords['x'] - self.coords['x']
                dy = unit.coords['y'] - self.coords['y']
                self.rotation = math.atan(dy / dx)
                if dx < 0:
                    self.rotation = (self.rotation + math.pi) % (2 * math.pi)
            self.image[2].check_responses(self, key)
            self.image[2].lines.append(
                self.image[0].create_line((unit.coords['x'], unit.coords['y']),
                                          (self.coords['x'], self.coords['y']),
                                          fill='green' if key == 'A' else 'blue'))

    def encounter(self, base):
        self.points[base.kind] = 0
        if base.kind == self.destiny:
            self.destiny = base.next
            self.rotation = (self.rotation + math.pi) % (2 * math.pi)

    def forward(self):
        dx = self.speed * math.cos(self.rotation)
        dy = self.speed * math.sin(self.rotation)
        if self.coords['x'] + dx >= self.contains['x'] or self.coords['y'] + dy >= self.contains['y'] or \
                self.coords['x'] + dx <= 0 or self.coords['y'] + dy <= 0:
            self.rotation = (self.rotation + math.pi) % (2 * math.pi)
            dx = self.speed * math.cos(self.rotation)
            dy = self.speed * math.sin(self.rotation)
        self.coords['x'] += dx
        self.coords['y'] += dy
        self.rotation = (self.rotation + math.pi / 144 * uniform(-1, 1)) % (2 * math.pi)
        self.image[0].move(self.image[1], dx, dy)
        for key in self.points.keys():
            self.points[key] = self.points[key] + 1
