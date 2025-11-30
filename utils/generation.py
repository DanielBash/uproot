"""UTIL: Universe manager
 - Seed generated data
 - Chunk generation"""

import random
from dataclasses import dataclass
from typing import List, Tuple
from strgen import StringGenerator as SG


@dataclass
class BiomSettings:
    tiles: List[str]


@dataclass
class PlanetSettings:
    name: SG = SG('[\l\d]{4:18}&[\d]&[\p]')
    radius: Tuple[int] = (10 ** 10, 10 ** 12),
    bioms: List[BiomSettings] = None


@dataclass
class StarSystemSettings:
    name: SG = SG('[\l\d]{4:18}&[\d]&[\p]')
    planet_amount: Tuple[int, int] = (3, 5),
    planet_types: List[PlanetSettings] = None,
    planet_orbit: Tuple[int, int] = (10 ** 6, 10 ** 8)


@dataclass
class UniverseSettings:
    name: SG = SG('[\l\d]{4:18}&[\d]&[\p]')
    ss_chunk: int = 10 ** 6,
    ss_amount: Tuple[int, int] = (20, 150),
    ss_types: List[Tuple[int, StarSystemSettings]] = None


class Biom:
    def __init__(self, settings: BiomSettings, seed: str = 'seed'):
        self.settings = settings
        self.seed = seed


class Planet:
    def __init__(self, settings: PlanetSettings, seed: str = 'seed', orbit: int = 0):
        # initialization settings
        self.settings = settings
        self.seed = seed
        self.orbit = orbit

        # procedural settings
        self.name = ''

        self.setup()

    def setup(self):
        # name generation
        self.name = self.settings.name.render(seed=hash(self.seed))

    def get_tile(self, x: int, y: int) -> str:
        return 'grass_tile'


class StarSystem:
    def __init__(self, settings: StarSystemSettings, seed: str = 'seed', rel_x: int = 0, rel_y: int = 0):
        # initialization settings
        self.settings = settings
        self.seed = seed
        self.rel_x = rel_x
        self.rel_y = rel_y

        # procedural settings
        self.planets = []
        self.name = []

        self.setup()

    def setup(self):
        # name generation
        self.name = self.settings.name.render(seed=hash(self.seed))

        # planet generation
        random.seed(self.seed)

        planet_amount = random.randint(*self.settings.planet_amount)

        for i in range(planet_amount):
            settings_available = [setting for weight, setting in self.settings.planet_types]
            settings_weights = [weight for weight, ss_setting in self.settings.planet_types]

            planet_setting = random.choices(settings_available, weights=settings_weights)
            orbit = random.randint(*self.settings.planet_orbit)

            self.planets.append(Planet(planet_setting, f'{self.seed}_{orbit}', orbit))


class Universe:
    def __init__(self, settings: UniverseSettings, seed: str = 'seed'):
        # initialization settings
        self.settings = settings
        self.seed = seed

        # procedural settings
        self.name = ''

        self.setup()

    def setup(self):
        # name generation
        self.name = self.settings.name.render(seed=hash(self.seed))

    def get_chunk(self, x: int, y: int) -> List[StarSystem]:
        seed = f'{self.seed}_{x}_{y}'

        random.seed(seed)

        ss_amount = random.randint(*self.settings.ss_amount)

        sss = []

        for i in range(ss_amount):
            settings_available = [setting for weight, setting in self.settings.ss_types]
            settings_weights = [weight for weight, ss_setting in self.settings.ss_types]

            ss_setting = random.choices(settings_available, weights=settings_weights)

            rel_x = random.randint(0, self.settings.ss_chunk)
            rel_y = random.randint(0, self.settings.ss_chunk)

            ss = StarSystem(ss_setting, f'{seed}_{rel_x}_{rel_y}', rel_x=rel_x, rel_y=rel_y)

            sss.append(ss)

        return sss
