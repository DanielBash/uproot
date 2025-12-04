"""UTIL: Tile map manager
 - Easy tile map management
 - Efficient display
 - Procedurally generated tile maps"""

import math
import random
from typing import Tuple

import arcade.examples.perf_test.stress_test_draw_moving_arcade
from typing import Tuple
from arcade import DefaultTextureAtlas as TextureAtlas, SpriteList, Sprite
from PIL import Image, ImageDraw
import random
import arcade


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

        textures = self.tile_map.tex_all()
        self.tiles = SpriteList(use_spatial_hash=False)
        self.tiles.preload_textures(textures)
        self.tile_access = [[]]

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

    def _reposition(self):
        for w in range(self.column_amount):
            for h in range(self.row_amount):
                tile = self.tile_access[h][w]
                tile.center_x = tile.texture.width // 2 + w * tile.texture.width
                tile.center_y = tile.texture.height // 2 + h * tile.texture.height

    def prepare(self):
        self.column_amount = math.ceil(self.window.width // (self.tile_size * self.camera.zoom) + 2)
        self.row_amount = math.ceil(self.window.height // (self.tile_size * self.camera.zoom) + 2)

        if self.column_amount == self._prev_column_amount and self.row_amount == self._prev_row_amount:
            return

        self._prev_column_amount, self._prev_row_amount = self.column_amount, self.row_amount

        if len(self.tile_access) < self.row_amount:
            for i in range(self.row_amount - len(self.tile_access)):
                self.tile_access.append([None] * self.column_amount)

        for i in range(len(self.tile_access)):
            if len(self.tile_access[i]) < self.column_amount:
                self.tile_access[i] += [None] * (self.column_amount - len(self.tile_access[i]))


        for w in range(self.column_amount):
            for h in range(self.row_amount):
                if self.tile_access[h][w] is None:
                    tile = Sprite()
                    tile.texture = self.tile_map.tex(w, h)
                    tile.th = self.tile_map.tex_hash(w, h)

                    tile.center_x = tile.texture.width // 2 + w * tile.texture.width
                    tile.center_y = tile.texture.height // 2 + h * tile.texture.height

                    self.tile_access[h][w] = tile

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

        if (tile_start_x, tile_start_y, self.row_amount, self.column_amount) != self._prev_tile_start:
            for w in range(self.column_amount):
                for h in range(self.row_amount):
                    tile_x = tile_start_x + w
                    tile_y = tile_start_y + h

                    if self.tile_access[h][w].th != self.tile_map.tex_hash(tile_x, tile_y):
                        self.tile_access[h][w].texture = self.tile_map.tex(tile_x, tile_y)
                        self.tile_access[h][w].th = self.tile_map.tex_hash(tile_x, tile_y)

        self._prev_tile_start = (tile_start_x, tile_start_y, self.row_amount, self.column_amount)

        self.tiles.draw(pixelated=pixelated)
