"""UTIL: Tile map manager
 - Easy tile map management
 - Efficient display
 - Procedurally generated tile maps"""

import math
import random

import arcade.examples.perf_test.stress_test_draw_moving_arcade
from arcade import SpriteList, Sprite


# TODO: refactor TileMap class. Add ability to display stars, and add proper planet view
class TileMap:
    def __init__(self, data):
        self.data = data
        self.cache = {}

    def get(self, x, y):
        return

    def get_texture(self, x, y):
        name = self.get_texture_name(x, y)
        if not name in self.cache.keys():
            self.cache[name] = self.data.assets.texture(name)

        return self.cache[name]

    def get_texture_name(self, x, y):
        random.seed(f'{x} {y}')
        return f'grass_tile{random.randint(1, 2)}'


# TODO: optimize tile map drawer
class TileMapDrawer:
    def __init__(self, window, tile_map, tile_size=50):
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

    def draw(self, x, y, pixelated=True):
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
