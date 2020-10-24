import os, sys
import collections
import json
import pathlib
from pprint import pprint

import jsonpickle
import openpyxl

from . import base
from . import data
from . import loaders

class Adventure(base.Base):

    def __init__(self, name, player_name):
        """Set up an adventure from details in a spreadsheet
        """
        super().__init__(name)
        self.player = data.Actor(player_name)

    def load_initial_game_from_spreadsheet(self, filepath=None):
        """Load the rooms, layout and items from a spreadsheet
        """
        info = loaders.from_spreadsheet(filepath or "%s.xlsx" % self.name)
        self.rooms = info['rooms']
        self.inventory = info['inventory']
        for room in self.rooms.values():
            if room.is_initial:
                self.player.move_to(room)

    def handle_user_command(self, command):
        raise NotImplementedError

    def handle_system_command(self, command):
        raise NotImplementedError

    def handle_command(self, type, command):
        """Commands come in two types:

        1) a user command which is something the user types in (eg GO NORTH)
        2) a system command which is the ui asking the backend for something
        """
        if type == "user":
            return self.handle_user_command(command)
        elif type == "system":
            return self.handle_system_command(command)
        else:
            raise RuntimeError("Unknown command type %s" % type)

