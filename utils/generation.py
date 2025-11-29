"""Universe manager. Goal: better big control over universe settings"""

import random


class Planet:
    def __init__(self, seed='seed',
                 min_planet_size=10 ** 5,
                 max_planet_size=10 ** 6):
        self.seed = seed
        self.min_planet_size = min_planet_size
        self.max_planet_size = max_planet_size

    def get_tile(self, x, y):
        pass

    def get_tile_chunk(self, x, y, width, height):
        pass


class StarSystem:
    def __init__(self, seed='seed',
                 min_planet_size=10 ** 5,
                 max_planet_size=10 ** 6,
                 min_planets_in_star_system=2,
                 max_planets_in_star_system=30):
        self.seed = seed
        self.min_planet_size = min_planet_size
        self.max_planet_size = max_planet_size
        self.min_planets_in_star_system = min_planets_in_star_system
        self.max_planets_in_star_system = max_planets_in_star_system

    def __str__(self):
        return (f'StarSystem'
                f'seed={self.seed}')

    def from_json(self, data, replace_seed=False):
        for i in data.keys():
            if not (not replace_seed and i == 'seed'):
                self.__setattr__(i, data[i])

    def get_planets(self):
        pass

class Universe:
    def __init__(self, seed='seed',
                 star_density=1000,
                 min_planet_size=10 ** 5,
                 max_planet_size=10 ** 6,
                 min_planets_in_star_system=2,
                 max_planets_in_star_system=30,
                 star_system_chunk=10 ** 10):
        self.seed = seed
        self.min_planet_size = min_planet_size
        self.max_planet_size = max_planet_size
        self.star_system_density = star_density
        self.min_planets_in_star_system = min_planets_in_star_system
        self.max_planets_in_star_system = max_planets_in_star_system
        self.star_system_chunk = star_system_chunk

    def get_star_chunk(self, x=0, y=0):
        star_systems = []

        random.seed(f'{self.seed}_{x}_{y}')
        for i in range(self.star_system_density):
            system_x = random.randint(0, self.star_system_chunk)
            system_y = random.randint(0, self.star_system_chunk)
            star_system = StarSystem(f'{self.seed}_{x}_{y}_{system_x}_{system_y}')
            star_system.from_json(self.to_json(), replace_seed=False)
            star_systems.append(star_system)

        return star_systems

    def to_json(self):
        return {'seed': self.seed,
                'min_planet_size': self.min_planet_size,
                'max_planet_size': self.max_planet_size,
                'star_system_density': self.star_system_density,
                'min_planets_in_star_system': self.min_planets_in_star_system,
                'max_planets_in_star_system': self.max_planets_in_star_system,
                'star_system_chunk': self.star_system_chunk}

    def from_json(self, data):
        for i in data.keys():
            self.__setattr__(i, data[i])

    def __str__(self):
        return (f"Universe"
                f"seed={self.seed}"
                f"star_system_density={self.star_system_density}"
                f"min_planet_size={self.min_planet_size}"
                f"max_planet_size={self.max_planet_size}"
                f"min_planets={self.min_planets_in_star_system}"
                f"max_planets={self.max_planets_in_star_system}"
                f"star_chunk={self.star_system_chunk}")
