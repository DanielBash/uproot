"""UTIL: Tile map manager
 - Easy tile map management
 - Efficient display
 - Procedurally generated tile maps"""

import math
import random
from typing import Tuple

import arcade.examples.perf_test.stress_test_draw_moving_arcade
from arcade import SpriteList, Sprite
from typing import Tuple

from PIL import Image, ImageDraw
import random
import arcade


class TileMap:
    def __init__(self, conf):
        self.cache = {}
        self.conf = conf

    def get(self, x: int, y: int):
        return

    def get_texture(self, x: int, y: int) -> arcade.Texture:
        name = self.get_texture_name(x, y)
        if name not in self.cache.keys():
            self.cache[name] = self.conf.assets.texture(name)

        return self.cache[name]

    def get_texture_name(self, x: int, y: int) -> str:
        random.seed(f'{x} {y}')
        return f'grass_tile{random.randint(1, 2)}'


class TileMapDrawer:
    def __init__(self, window: arcade.Window, tile_map: TileMap, tile_size: int = 50):
        self.window = window
        self.tile_size = tile_size
        self.tile_map = tile_map

        self.tiles = SpriteList(use_spatial_hash=True)
        self.tile_access = {}
        self.sprite_cache = ''
        self.sprites_width = self.window.width // self.tile_size + 3
        self.sprites_height = self.window.height // self.tile_size + 3

        self.prepare()

    def prepare(self):
        self.sprites_width = math.ceil(self.window.width // self.tile_size + 3)
        self.sprites_height = math.ceil(self.window.height // self.tile_size + 3)

        sprite_state = f'{self.sprites_height}_{self.sprites_width}_{self.tile_size}'
        if sprite_state == self.sprite_cache:
            return
        else:
            self.sprite_cache = sprite_state

        self.tiles.clear()
        self.tile_access.clear()

        for w in range(self.sprites_width):
            for h in range(self.sprites_height):
                tile = Sprite()
                self.tile_access[(w, h)] = {'tile': tile,
                                            'texture': '',
                                            'scale': 1}
                self.tiles.append(tile)

    def draw(self, x: int, y: int, pixelated: bool = True):
        self.prepare()
        x -= self.window.width // 2
        y -= self.window.height // 2

        tile_start_x = x // self.tile_size
        tile_start_y = y // self.tile_size
        move_x = x % self.tile_size
        move_y = y % self.tile_size

        for w in range(self.sprites_width):
            for h in range(self.sprites_height):
                tile_x = tile_start_x + w
                tile_y = tile_start_y + h

                if self.tile_map.get_texture_name(tile_x, tile_y) != self.tile_access[(w, h)]['texture']:
                    self.tile_access[(w, h)]['tile'].texture = self.tile_map.get_texture(tile_x, tile_y)
                    self.tile_access[(w, h)]['texture'] = self.tile_map.get_texture_name(tile_x, tile_y)

                calc_scale = self.tile_size / (
                        self.tile_access[(w, h)]['tile'].width / self.tile_access[(w, h)]['scale'])
                if self.tile_access[(w, h)]['tile'].scale != calc_scale:
                    self.tile_access[(w, h)]['tile'].scale = calc_scale
                    self.tile_access[(w, h)]['scale'] = calc_scale
                self.tile_access[(w, h)]['tile'].center_x = -move_x + self.tile_size // 2 + w * self.tile_size
                self.tile_access[(w, h)]['tile'].center_y = -move_y + self.tile_size // 2 + h * self.tile_size

        self.tiles.draw(pixelated=pixelated)


class StarTileMap:
    def __init__(self, universe, conf):
        self.cache = {}
        self.universe = universe
        self.conf = conf

    def generate_texture(self, x: int, y: int, size: Tuple[int, int]) -> arcade.Texture:
        width, height = size

        image = Image.new("RGBA", (width, height), (0, 0, 0, 255))
        draw = ImageDraw.Draw(image)

        for _ in self.universe.get_chunk(x, y):
            star_x = _.rel_x / self.universe.settings.ss_chunk * width
            star_y = _.rel_y / self.universe.settings.ss_chunk * height

            star_size = random.choice([1, 1, 1, 2, 2, 3])

            left = star_x - star_size
            top = star_y - star_size
            right = star_x + star_size
            bottom = star_y + star_size

            draw.ellipse([left, top, right, bottom],
                         fill=(255, 255, 255, 255))

        texture = arcade.Texture(image)

        if len(self.cache) > 1000:
            self.cache.clear()

        return texture

    def get_texture(self, x: int, y: int) -> arcade.Texture:
        name = self.get_texture_name(x, y)

        if name not in self.cache.keys():
            self.cache[name] = self.generate_texture(x, y, size=(512, 512))

        return self.cache[name]

    def get_texture_name(self, x: int, y: int) -> str:
        return f'{x} {y}'