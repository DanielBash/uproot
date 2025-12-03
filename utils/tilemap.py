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
        return f'grass_tile{random.randint(1, 10)}'


class TileMapDrawer:
    def __init__(self, window: arcade.Window, tile_map: TileMap, tile_size: int = 50):
        self.window = window
        self.tile_size = tile_size
        self.tile_map = tile_map

        self.tiles = SpriteList(use_spatial_hash=False)
        self.tile_access = {}
        self.sprite_cache = ''
        self.column_amount = self.window.width // self.tile_size + 2
        self.row_amount = self.window.height // self.tile_size + 2

        self.prepare()

    def prepare(self):
        self.column_amount = math.ceil(self.window.width // self.tile_size + 2)
        self.row_amount = math.ceil(self.window.height // self.tile_size + 2)

        sprite_state = f'{self.row_amount}_{self.column_amount}_{self.tile_size}'
        if sprite_state == self.sprite_cache:
            return
        else:
            self.sprite_cache = sprite_state

        self.tiles.clear()
        self.tile_access.clear()

        for w in range(self.column_amount):
            for h in range(self.row_amount):
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

        for w in range(self.column_amount):
            for h in range(self.row_amount):
                tile_x = tile_start_x + w
                tile_y = tile_start_y + h

                if self.tile_map.get_texture_name(tile_x, tile_y) != self.tile_access[(w, h)]['texture']:
                    self.tile_access[(w, h)]['tile'].texture = self.tile_map.get_texture(tile_x, tile_y)
                    self.tile_access[(w, h)]['texture'] = self.tile_map.get_texture_name(tile_x, tile_y)

                # calculate changes
                calc_scale = self.tile_size / (
                        self.tile_access[(w, h)]['tile'].width / self.tile_access[(w, h)]['scale'])
                calc_center_x = -move_x + self.tile_size // 2 + w * self.tile_size
                calc_center_y = -move_y + self.tile_size // 2 + h * self.tile_size

                # apply changes if actually needed
                if self.tile_access[(w, h)]['tile'].scale != calc_scale:
                    self.tile_access[(w, h)]['tile'].scale = calc_scale
                    self.tile_access[(w, h)]['scale'] = calc_scale

                if (self.tile_access[(w, h)]['tile'].center_x, self.tile_access[(w, h)]['tile'].center_y) != (
                calc_center_x, calc_center_y):
                    self.tile_access[(w, h)]['tile'].center_x = calc_center_x
                    self.tile_access[(w, h)]['tile'].center_y = calc_center_y

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


# PROCEED WITH CATION: HIGHLY OPTIMIZED CLASSES(!)
class OptimizedTileMap:
    def __init__(self, conf):
        self.conf = conf

        self.textures = []
        self.tex_size = 0

        self.setup()

    def setup(self):
        self.textures = [self.conf.assets.texture(f'grass_tile{i + 1}') for i in range(10)]
        self.tex_size = self.textures[0].width

    def tex_all(self):
        return self.textures

    def tex_hash(self, x: int, y: int):
        ind = abs(int(x * 92821) ^ int(y * 68937)) % 10
        return ind

    def tex(self, x: int = 0, y: int = 0):
        return self.textures[self.tex_hash(x, y)]


class OptimizedTileMapDrawer:
    def __init__(self, window: arcade.Window, tile_map: OptimizedTileMap, zoom: int = 1):
        self.window = window
        self.zoom = zoom
        self.tile_map = tile_map

        self.tiles = SpriteList(use_spatial_hash=False)
        self.tiles.preload_textures(self.tile_map.tex_all())
        self.tile_access = {}

        self.tile_size = self.tile_map.tex_size

        self.column_amount = self.window.width // self.tile_size + 2
        self.row_amount = self.window.height // self.tile_size + 2

        self.camera = arcade.Camera2D()

        # caching
        self._prev_column_amount = 0
        self._prev_row_amount = 0
        self._prev_window_size = self.window.size
        self._prev_tile_start = (1, 1)

        self.prepare()

    def prepare(self):
        self.column_amount = math.ceil(self.window.width // (self.tile_size * self.camera.zoom) + 2)
        self.row_amount = math.ceil(self.window.height // (self.tile_size * self.camera.zoom) + 2)

        if self.column_amount == self._prev_column_amount and self.row_amount == self._prev_row_amount:
            return

        self._prev_column_amount, self._prev_row_amount = self.column_amount, self.row_amount

        for w in range(self.column_amount):
            for h in range(self.row_amount):
                if (w, h) not in self.tile_access:
                    tile = Sprite()
                    tile.texture = self.tile_map.tex(w, h)
                    tile.th = self.tile_map.tex_hash(w, h)

                    tile.center_x = tile.texture.width // 2 + w * tile.texture.width
                    tile.center_y = tile.texture.height // 2 + h * tile.texture.height

                    self.tile_access[(w, h)] = tile

                    self.tiles.append(tile)

    def draw(self, x: int, y: int, pixelated: bool = True):
        self.prepare()

        self.camera.zoom = self.zoom

        x -= self.camera.viewport_width / (2 * self.camera.zoom)
        y -= self.camera.viewport_height / (2 * self.camera.zoom)

        # update camera
        move_x = x % self.tile_size
        move_y = y % self.tile_size

        self.camera.position = (move_x + self.camera.viewport_width / (2 * self.camera.zoom),
                                move_y + self.camera.viewport_height / (2 * self.camera.zoom))
        if self.window.size != self._prev_window_size:
            self.camera.match_window()

        self.camera.use()

        # update tile textures if necessary

        tile_start_x = x // self.tile_size
        tile_start_y = y // self.tile_size

        if (tile_start_x, tile_start_y) != self._prev_tile_start:
            for w in range(self.column_amount):
                for h in range(self.row_amount):
                    tile_x = tile_start_x + w
                    tile_y = tile_start_y + h

                    if self.tile_access[(w, h)].th != self.tile_map.tex_hash(tile_x, tile_y):
                        self.tile_access[(w, h)].texture = self.tile_map.tex(tile_x, tile_y)
                        self.tile_access[(w, h)].th = self.tile_map.tex_hash(tile_x, tile_y)
            self._prev_tile_start = (tile_start_x, tile_start_y)
        self.tiles.draw(pixelated=pixelated)
