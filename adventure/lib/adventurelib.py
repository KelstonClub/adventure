import os, sys
import collections
import json
import pickle
from pprint import pprint

import openpyxl

BORDER_OFFSETS = [
    ("top", (0, -1), "north"),
    ("bottom", (0, +1), "south"),
    ("left", (-1, 0), "west"),
    ("right", (+1, 0), "east")
]

class Base:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.name)

    @classmethod
    def from_namedtuple(cls, info):
        return cls(*info)

class Item(Base):

    def __init__(self, name, weight, description, initial_location, initial_sublocation):
        super().__init__(name)
        self.weight = weight
        self.description = description
        self.initial_location = initial_location
        self.initial_sublocation = initial_sublocation

    def as_dict(self):
        return dict(
            weight=self.weight,
            description=self.description,
            initial_location=self.initial_location,
            initial_sublocation=self.initial_sublocation
        )


class Room(Base):

    def __init__(self, name, description, is_initial):
        super().__init__(name)
        self.description = description
        self.exits = dict()
        self.is_initial = (is_initial == "Yes")

    def as_dict(self):
        return dict(
            description=self.description,
            exits=[(direction, room.name) for (direction, room) in self.exits.items()]
        )

class Actor(Base):

    def __init__(self, name, score=10):
        super().__init__(name)
        self.inventory = set()
        self.score = score
        self.location = None

    def move_to(self, new_location):
        self.location = new_location

def adventure_from_pickle(filepath):
    with open(filepath, "rb") as f:
        return pickle.load(f)

class Adventure(object):

    def __init__(self, name, player_name):
        """Set up an adventure from details in a spreadsheet
        """
        self.name = name
        self.player = Actor(player_name)

    def load_from_saved_game(self, filepath):
        raise NotImplementedError

    def save_game(self, filepath):
        with open(filepath, "wb") as f:
            pickle.dump(self, f)

    def load_initial_game_from_spreadsheet(self, filepath):
        """Load the rooms, layout and items from a spreadsheet
        """
        wb = openpyxl.load_workbook(filepath)
        try:
            self.rooms = self.get_rooms(wb)
            layout = self.get_layout(wb)
            for name, room in self.rooms.items():
                for direction, neighbour in layout[name].items():
                    room.exits[direction] = self.rooms[neighbour]
            self.inventory = self.get_inventory(wb)

            for room in self.rooms.values():
                if room.is_initial:
                    self.actor.move_to(room)
        finally:
            wb.close()

    def sheet_to_namedtuples(self, wb, ws_name, cls):
        """Given an openpyxl workbook yield each row as a class
        based on the worksheet name and header row
        """
        ws = wb[ws_name]
        rows = ws.iter_rows(values_only=True)
        headers = [cell.lower() for cell in next(rows)]
        tuplecls = collections.namedtuple("%sRow" % (ws_name), headers)
        for row in rows:
            yield cls.from_namedtuple(tuplecls(*row))

    def find_neighbours(self, cell):
        neighbours = {}
        ws = cell.parent
        x, y = cell.column, cell.row
        for (edge, (dx, dy), direction) in BORDER_OFFSETS:
            border = getattr(cell.border, edge)
            if border.style is None:
                col, row = x + dx, y + dy
                if (row > 0 and col > 0):
                    neighbour_name = ws.cell(column=col, row=row).value
                    if neighbour_name:
                        neighbours[direction] = neighbour_name

        return neighbours

    def get_layout(self, wb):
        """Return a dictionary mapping each room to its neighbours
        """
        layout = {}
        for row in wb['Layout']:
            for cell in row:
                room_name = cell.value
                if room_name:
                    layout[room_name] = self.find_neighbours(cell)

        return layout

    def get_inventory(self, wb):
        """Return a dictionary mapping inventory names to details"""
        return dict((i.name, i) for i in self.sheet_to_namedtuples(wb, "Items", Item))

    def get_rooms(self, wb):
        """Return a dictionary mapping room names to details"""
        return dict((r.name, r) for r in self.sheet_to_namedtuples(wb, "Rooms", Room))


