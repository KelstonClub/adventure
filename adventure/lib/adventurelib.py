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

class UnknownVerbError(Exception):
    pass

class UnknownExitError(Exception):
    pass
    
class UnknownObjectError(Exception):
    pass

class Adventure(base.Base):
    
    verbs = {"go", "get", "drop"}
    syns = {"run" : "go", "move" : "go", "grab" : "get"}
    
    def __init__(self, name, player_name):
        """Set up an adventure from details in a spreadsheet
        """
        super().__init__(name)
        self.player = data.Actor(player_name)
        self.rooms = {}
        self.inventory = {}

    def get_verb(self, word):
        found_word = self.syns.get(word, word)
        if found_word in self.verbs:
            return found_word
        else:
            raise RuntimeError("No hablo espanol")
        
    def load_initial_game_from_spreadsheet(self, filepath=None):
        """Load the rooms, layout and items from a spreadsheet
        """
        info = loaders.from_spreadsheet(filepath or "%s.xlsx" % self.name)
        self.rooms = info['rooms']
        self.inventory = info['inventory']
        for room in self.rooms.values():
            if room.is_initial:
                self.player.move_to(room)
    
    def user_prompt(self):
        return "What now? "

    def get_anlayse_command(self, command):
        verb, noun = command.lower().strip().split()
        return verb, noun
    
    def handle_go(self, noun):
        print("handle go", noun)
        current_location = self.player.location
        print(current_location.exits)
        if noun in current_location.exits:
            new_location = current_location.exits[noun]
            self.player.location = new_location
        else:
            raise UnknownExitError
    
    def handle_get(self, noun):
        print("handle get", noun)
        print(self.inventory)
        object = self.inventory[noun]
        if object in self.player.location.inventory:
            self.player.inventory.add(object)
            # The line of code above adds the object to the players inventory
            self.player.location.inventory.remove(object)
            # The line of code above removes the object from the current rooms inventory
        else:
            raise UnknownObjectError
            
    def handle_drop(self):
        print("Handle drop, noun")
        print(self.inventory)
        object = self.inventory[noun]
        if object in self.player.location.inventory:
            self.player.inventory.remove(object)
            # The line of code above removes the object from the players inventory
            self.player.location.inventory.add(object)
            # The line of code above adds the objects to the current rooms inventory
        else:
            raise UnknownObjectError

    def handle_user_command(self, command):
        verb, noun = self.get_anlayse_command(command)
        print(verb, noun)
        if verb == "go":
            self.handle_go(noun)
        elif verb == "get":
            self.handle_get(noun)
        elif verb == "drop":
            self.handle_drop(noun)
        else:
            raise UnknownVerbError
        return self.player

    def handle_system_command(self, command):
        return self.player

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

if __name__ == "__main__":
    a = Adventure("Peter", "house")
    print(a.get_verb("go"))
    print(a.get_verb("move"))