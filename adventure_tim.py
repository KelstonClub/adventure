class State:
    pass
state = State()

class Room:
    def __init__(self, name):
        self.name = self.description = name
        self.exits = {}
        self.items = []

class Item:
    def __init__(self, name):
        self.name = self.description = name

hallway = Room("The hallway")
living_room = Room("The living room")
garden = Room("The garden")
kitchen = Room("The kitchen")

ball = Item("A ball")
sword = Item("A sword")

hallway.exits['E'] = living_room
living_room.exits['W'] = hallway

hallway.exits['W'] = kitchen
kitchen.exits['E'] = hallway

kitchen.exits['N'] = garden
garden.exits['S'] = kitchen

state.location = hallway
state.items = []

while True:
    print("You are in", state.location.name)
    instruction = input("What now? ")
    verb, noun = instruction.upper().split()

    if verb == "GO":
        direction = noun[0]
        if direction in state.location.exits:
            state.location = state.location.exits[direction]
        else:
            print("There is no exit to the", noun)
    else:
        print("I don't know how to", verb)
