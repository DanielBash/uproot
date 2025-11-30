"""FILE: Config
 - Global data management"""

import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import arcade
import pyglet

from views import intro, menu
from utils import tilemap


class PathConfig:
    def __init__(self, data_file, asset_folder):
        self.supported_ext = ['.png', '.jpg', '.jpeg', '.ico', '.json', '.mp3', '.wav']

        # roots
        self.data_file = data_file
        self.asset_folder = asset_folder

        # all shortcut endpoints
        self.shortcuts = {
            'icon': self.asset_folder / Path('images/icons'),
            'effect': self.asset_folder / Path('sounds/effects'),
            'music': self.asset_folder / Path('sounds/music'),
            'texture': self.asset_folder / Path('images/textures'),
        }

        self.icon_folder = self.asset_folder / Path('images/icons')

        self.music_folder = self.asset_folder / Path('sounds/music')
        self.sound_effects_folder = self.asset_folder / Path('sounds/effects')

        # build filesystem reconfiguration
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            os.chdir(sys._MEIPASS)

    # -- base method
    def get(self, folder, name):
        path = folder / Path(name)

        if not path.exists():
            for i in self.supported_ext:
                path = folder / Path(name + i)
                if path.exists():
                    return path

        return None

    # -- paths shortcuts
    def short(self, short, name):
        return self.get(self.shortcuts[short], name)


class AssetsConfig:
    def __init__(self, paths):
        self.paths = paths

    def icon(self, name):
        image_path = self.paths.short('icon', name)

        return pyglet.image.load(image_path)

    def music(self, name, streaming=True):
        music_path = self.paths.short('music', name)

        return arcade.load_sound(music_path, streaming=streaming)

    def effect(self, name, streaming=True):
        music_path = self.paths.short('effect', name)

        return arcade.load_sound(music_path, streaming=streaming)

    def texture(self, name):
        return arcade.load_texture(self.paths.short('texture', name))


class DataConfig:
    def __init__(self, paths):
        self.paths = paths

        self.data = {}

        self.load_data()

    def prepare(self):
        if not self.paths.data_file.exists():
            self.paths.data_file.parent.mkdir(parents=True, exist_ok=True)
            self.paths.data_file.write_text('{}')

    def load_data(self):
        self.prepare()
        with self.paths.data_file.open('r', encoding='utf-8') as f:
            self.data = json.load(f)

    def save_data(self):
        self.prepare()
        with self.paths.data_file.open('w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)


@dataclass
class Config:
    # -- constants

    # window params
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 400
    WINDOW_RESIZABLE = True
    WINDOW_NAME = 'Uproot'

    WINDOW_MINIMAL_WIDTH = 200
    WINDOW_MINIMAL_HEIGHT = 200

    WINDOW_ICON = 'window_icon'

    # view management
    LAUNCH_VIEW = intro.Main

    # paths
    DATA_FILE = Path('saves/save.json')
    ASSETS_FOLDER = Path('assets')

    # controls
    KEYS = {'fullscreen': arcade.key.F11,
            'move_up': arcade.key.UP,
            'move_down': arcade.key.DOWN,
            'move_left': arcade.key.LEFT,
            'move_right': arcade.key.RIGHT,
            'zoom_in': arcade.key.W,
            'zoom_out': arcade.key.S}

    # -- dynamic config modules
    paths = PathConfig(DATA_FILE, ASSETS_FOLDER)
    assets = AssetsConfig(paths)
    data = DataConfig(paths)
    tiles = tilemap

    start_time = time.time()
