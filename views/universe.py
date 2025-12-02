"""VIEW: Planet
 - Display current planet"""

import arcade
import arcade.gui
import arcade.gui.widgets.buttons
import arcade.gui.widgets.layout


class Main(arcade.View):
    def __init__(self, config):
        super().__init__()

        # initial configuration
        self.conf = config
        self.scaling = self.width / 800

        # SCENE SETTINGS
        self.background_color = arcade.color.Color(33, 23, 41)
        self.target_fps = 60

        # universe settings
        self.universe = config.generation.Universe(settings=config.DEFAULT_UNIVERSE_SETTINGS)

        # sprites
        self.tile_map = self.conf.tiles.OptimizedTileMap(config)
        self.tile_map_drawer = self.conf.tiles.OptimizedTileMapDrawer(self.window, self.tile_map)

        # cameras
        self.camera = arcade.Camera2D()

        # dynamic variables
        self.x = 0
        self.y = 0
        self.camera_speed = 0.1
        self.keys_pressed = []
        self.zoom = 1
        self.zoom_speed = 0.05
        self.min_zoom = 0.1

    # -- handle drawing
    def on_draw(self):
        self.draw_all()

    def draw_all(self):
        self.clear()
        self.tile_map_drawer.draw(self.x * self.tile_map_drawer.tile_size, self.y * self.tile_map_drawer.tile_size)

        self.camera.use()

        if self.conf.DEBUG:
            arcade.draw_text(f'FPS: {int(arcade.get_fps())}', 0, 0, font_size=30)

    # -- handle updating
    def on_update(self, delta_time: int):
        self.tile_map_drawer.zoom = self.zoom

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
            self.zoom = max(float(self.zoom), self.min_zoom)

        if self.conf.KEYS['zoom_in'] in self.keys_pressed:
            self.zoom += self.zoom_speed * self.zoom

    # -- handle user input
    def on_key_press(self, key, key_modifiers):
        if key == self.conf.KEYS['fullscreen']:
            self.window.set_fullscreen(not self.window.fullscreen)
        if key == self.conf.KEYS['action']:
            print(f'LEN: {len(self.tile_map_drawer.tiles)}\n')
        self.keys_pressed.append(key)

    def on_key_release(self, key, key_modifiers):
        if self.keys_pressed.index(key) != -1:
            del self.keys_pressed[self.keys_pressed.index(key)]

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.camera.match_window()
        self.camera.position = (self.camera.viewport_width * 0.5,
                                self.camera.viewport_height * 0.5)

    # -- handle view show up
    def on_show_view(self):
        self.window.set_update_rate(1 / self.target_fps)