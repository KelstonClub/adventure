from . import base

class Item(base.DataBase):

    def __init__(self, name, weight, description, initial_location, initial_sublocation):
        super().__init__(name)
        self.weight = weight
        self.description = description
        self.initial_location = initial_location
        self.initial_sublocation = initial_sublocation
    
    def __repr__(self):
        return "%s, %s" %(self.name, self.initial_location)
    
    def __eq__(self, other):
        return self.name == other.name
        
    def __hash__(self):
        return hash(self.name)
    
class Room(base.DataBase):

    def __init__(self, name, description, is_initial):
        super().__init__(name)
        self.description = description
        self.exits = dict()
        self.is_initial = (is_initial == "Yes")
        self.inventory = set()
    
    def __repr__(self):
        return "%s, %s" %(self.name, self.inventory)

class Actor(base.DataBase):

    def __init__(self, name, score=10):
        super().__init__(name)
        self.inventory = set()
        self.score = score
        self.location = None

    def move_to(self, new_location):
        self.location = new_location

