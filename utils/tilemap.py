"""Tile map manager. Goal: better big control over universe settings"""

from arcade import SpriteList, Sprite


class TileMap:
    def __init__(self, data):
        self.data = data

    def get(self, x, y):
        return

    def get_texture(self, x, y):
        return self.data.assets.texture(self.get_texture_name(x, y))

    def get_texture_name(self, x, y):
        return 'grass_tile'


class TileMapDrawer:
    def __init__(self, window, tile_map, tile_size=50):
        self.window = window
        self.tile_size = tile_size
        self.tile_map = tile_map

        self.tiles = SpriteList()
        self.tile_access = {}
        self.sprite_cache = ''
        self.sprites_width = self.window.width // self.tile_size + 3
        self.sprites_height = self.window.height // self.tile_size + 3

        self.prepare()

    def prepare(self):
        self.sprites_width = self.window.width // self.tile_size + 3
        self.sprites_height = self.window.height // self.tile_size + 3

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
                                            'texture': '',}
                self.tiles.append(tile)

    def draw(self, x, y):
        self.prepare()

        tile_start_x = x // self.tile_size
        tile_start_y = y // self.tile_size
        move_x = x % self.tile_size
        move_y = y % self.tile_size
        for w in range(self.sprites_width):
            for h in range(self.sprites_height):
                tile_x = tile_start_x + w
                tile_y = tile_start_y + 1

                if self.tile_map.get_texture_name(tile_x, tile_y) != self.tile_access[(w, h)]['texture']:
                    self.tile_access[(w, h)]['tile'].texture = self.tile_map.get_texture(tile_x, tile_y)
                    self.tile_access[(w, h)]['texture'] = self.tile_map.get_texture_name(tile_x, tile_y)

                self.tile_access[(w, h)]['tile'].center_x = -move_x + self.tile_size // 2 + w * self.tile_size
                self.tile_access[(w, h)]['tile'].center_y = -move_y + self.tile_size // 2 + h * self.tile_size

        self.tiles.draw()