import os, sys
import pathlib
from pprint import pprint

from .lib import adventurelib

def main(name):
    initial_filepath = pathlib.Path(f"{name}.xlsx")
    saved_filepath = pathlib.Path(f"{name}.saved")

    if saved_filepath.exists():
        adventure = adventurelib.adventure_from_pickle(saved_filepath)
    elif initial_filepath.exists():
        adventure = adventurelib.Adventure(name)
        adventure.load_initial_game_from_spreadsheet(initial_filepath)
    else:
        raise RuntimeError("Can't find either a saved game or a spreadsheet")

    print("Rooms:")
    for name, room in adventure.rooms.items():
        print(name)
        for direction, room in room.exits.items():
            print("  ", direction, "=>", room)
    print("Item:")
    pprint(adventure.inventory)

    adventure.save_game(saved_filepath)

if __name__ == '__main__':
    main(*sys.argv[1:])
