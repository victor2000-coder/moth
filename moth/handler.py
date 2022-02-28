import math
from random import random
from random import choice
from window_handler import WindowHandler
from unit import Unit
from base import Base


class Handler:
    units = list()
    bases = list()
    lines = list()

    def __init__(self, width: int, height: int, count_of_units: int, count_of_bases: int, kinds_of_bases: list,
                 radius_of_base: float, units_size: float, units_speed: float, sim_speed: int, distance: float):
        self.units_speed = units_speed
        self.width = width
        self.height = height
        self.distance = distance
        self.graphics = WindowHandler(width, height)
        self.kinds_of_bases = kinds_of_bases
        self.point_radius = radius_of_base
        self.generate(width, height, count_of_units, count_of_bases, kinds_of_bases, radius_of_base, units_size)
        self.graphics.add_on_timer_tick(self.timer_tick, sim_speed)
        self.graphics.start()

    def generate(self, width: int, height: int, count_of_units: int, count_of_bases: int, kinds_of_bases: list,
                 radius_of_base: float, size_of_unit: float):
        self.units = list()
        self.bases = list()
        for i in range(count_of_units):
            coords = {'x': random() * width / 7 * 1.5 + width / 7 * 2.75, 'y': random() * height / 5 * 1.5 + height / 5 * 1.75}
            self.units.append(Unit(coords, random() * 2 * math.pi, "A",
                                   kinds_of_bases, i, (*self.graphics.new_image(coords, size_of_unit, 'red'), self),
                                   {'x': width, 'y': height}, self.distance, random() * self.units_speed / 5 * 4 + self.units_speed / 5))

        coords = {'x': width / 7 * 2, 'y': height / 3 * 1}
        self.bases.append(Base(coords, 'A', 'B', 1, radius_of_base,
                               self.graphics.new_image(coords, radius_of_base * 2, 'yellow')))
        coords = {'x': width / 7 * 2, 'y': height / 3 * 2}
        self.bases.append(Base(coords, 'A', 'B', 1, radius_of_base,
                               self.graphics.new_image(coords, radius_of_base * 2, 'yellow')))

        coords = {'x': width / 7 * 5, 'y': height / 10 * 5}
        self.bases.append(Base(coords, 'B', 'A', 1, radius_of_base,
                               self.graphics.new_image(coords, radius_of_base * 2, 'yellow')))

        # for i in range(count_of_bases):
        #    coords = {'x': random() * width, 'y': random() * height}
        #    kind = choice(kinds_of_bases)
        #    self.bases.append(Base(coords, kind, choice(list({*kinds_of_bases} - {kind})), i, radius_of_base,
        #                           self.graphics.new_image(coords, radius_of_base * 2, 'yellow')))

    def check_encounter(self, unit: Unit):
        for base in self.bases:
            if math.sqrt((unit.coords['x'] - base.coords['x']) ** 2 +
                         (unit.coords['y'] - base.coords['y']) ** 2) <= base.radius:
                unit.encounter(base)
                self.check_responses(unit, base.kind)
                self.check_requests(unit)

    def check_responses(self, unit, key):
        for another_unit in set(self.units) - {unit}:
            if math.sqrt((another_unit.coords['x'] - unit.coords['x']) ** 2 + (
                    another_unit.coords['y'] - unit.coords['y']) ** 2) < self.distance:
                another_unit.listen(unit, key)

    def check_requests(self, unit):
        for another_unit in set(self.units) - {unit}:
            if math.sqrt((another_unit.coords['x'] - unit.coords['x']) ** 2 + (
                    another_unit.coords['y'] - unit.coords['y']) ** 2) < self.distance:
                for key in self.kinds_of_bases:
                    unit.listen(another_unit, key)

    def unit_forward(self, unit: Unit):
        unit.forward()

    def timer_tick(self, simulation_speed: int):
        for line in self.lines:
            self.graphics.canvas.delete(line)
        del self.lines[:]
        for unit in self.units:
            self.unit_forward(unit)
            self.check_encounter(unit)

        # for unit in self.units:
        #     self.check_distances(unit, choice(self.kinds_of_bases))
        self.graphics.add_on_timer_tick(self.timer_tick, simulation_speed)
