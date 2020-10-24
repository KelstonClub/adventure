import os, sys
import importlib
import pathlib
from pprint import pprint

import jsonpickle

from .lib import adventurelib, base

class Runner(base.Base):

    def __init__(self, player_name, adventure_name, ui_name):
        super().__init__("runner")
        self.player_name = player_name
        self.adventure_name = adventure_name
        self.ui_name = ui_name

    def restart_game(self):
        xlsx_filepath = pathlib.Path(f"{self.adventure_name}.xlsx")
        adventure = adventurelib.Adventure(self.adventure_name, self.player_name)
        adventure.load_initial_game_from_spreadsheet(xlsx_filepath)
        return adventure

    def load_game(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            return jsonpickle.decode(f.read())

    def save_game(self, adventure, filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(jsonpickle.encode(adventure))

    def run(self):
        saved_filepath = pathlib.Path(f"{self.adventure_name}.saved")
        if saved_filepath.exists():
            adventure = self.load_game(saved_filepath)
        else:
            adventure = self.restart_game()

        ui = importlib.import_module(".ui.%s" % self.ui_name, __package__)

        try:
            ui.run(adventure)
        finally:
            self.save_game(adventure, saved_filepath)

def main(adventure_name=None, player_name=None, ui_name="text"):
    if not adventure_name:
        adventure_name = input("Adventure: ")
    if not player_name:
        player_name = input("Player: ")
    Runner(player_name, adventure_name, ui_name).run()

if __name__ == '__main__':
    main(*sys.argv[1:])
