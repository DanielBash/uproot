"""Universe view. Goal: select star system"""

import math
import time
from math import sin
import arcade
import arcade.gui
import arcade.gui.widgets.buttons
import arcade.gui.widgets.layout
from pyglet.math import Vec2


class Main(arcade.View):
    def __init__(self, config):
        super().__init__()

        # initial configuration
        self.conf = config
        self.scaling = self.width / 800

        # SCENE SETTINGS
        self.background_color = arcade.color.Color(33, 23, 41)

        # sprites
        self.tile_map = self.conf.tiles.TileMap(self.conf)
        self.tile_map_drawer = self.conf.tiles.TileMapDrawer(self.window, self.tile_map)

    # -- handle drawing
    def on_draw(self):
        self.draw_all()

    def draw_all(self):
        self.clear()
        self.tile_map_drawer.draw(self.window.time * 100, self.window.time * 100)

    # -- handle updating
    def on_update(self, delta_time):
        pass

    # -- handle user input
    def on_key_press(self, key, key_modifiers):
        if key == self.conf.WINDOW_FULLSCREEN_KEY:
            self.window.set_fullscreen(not self.window.fullscreen)

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.scaling = min(width / 800, height / 600)
