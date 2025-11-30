"""VIEW: Planet
 - Display current planet"""

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

        # dynamic variables
        self.x = 0
        self.y = 0
        self.camera_speed = 0.1
        self.keys_pressed = []
        self.zoom = 70
        self.zoom_speed = 0.05

    # -- handle drawing
    def on_draw(self):
        self.draw_all()

    def draw_all(self):
        self.clear()
        self.tile_map_drawer.draw(self.x * self.tile_map_drawer.tile_size, self.y * self.tile_map_drawer.tile_size)

    # -- handle updating
    def on_update(self, delta_time: int):
        self.tile_map_drawer.tile_size = int(self.zoom * self.scaling)

        if self.conf.KEYS['move_up'] in self.keys_pressed:
            self.y += self.camera_speed
        if self.conf.KEYS['move_down'] in self.keys_pressed:
            self.y -= self.camera_speed
        if self.conf.KEYS['move_left'] in self.keys_pressed:
            self.x -= self.camera_speed
        if self.conf.KEYS['move_right'] in self.keys_pressed:
            self.x += self.camera_speed

        if self.conf.KEYS['zoom_out'] in self.keys_pressed:
            self.zoom -= self.zoom_speed * self.zoom
            self.zoom = max(self.zoom, 1)

        if self.conf.KEYS['zoom_in'] in self.keys_pressed:
            self.zoom += self.zoom_speed * self.zoom

    # -- handle user input
    def on_key_press(self, key, key_modifiers):
        if key == self.conf.KEYS['fullscreen']:
            self.window.set_fullscreen(not self.window.fullscreen)
        self.keys_pressed.append(key)

    def on_key_release(self, key, key_modifiers):
        if self.keys_pressed.index(key) != -1:
            del self.keys_pressed[self.keys_pressed.index(key)]

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.scaling = min(width / 800, height / 600)
