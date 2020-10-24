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

    def run(self):
        print("Rooms:")
        for name, room in adventure.rooms.items():
            print(name)
            for direction, room in room.exits.items():
                print("  ", direction, "=>", room)
        print("Item:")
        pprint(adventure.inventory)
