# Write your code here :-)
from pprint import pprint
rooms = {
    (0, 0): "The hallway",
    (1, 1): "The Living Room",
    (0, 1): "The Kitchen",
    (0, -1) : "The garden"
}
pprint(rooms)

directions = {
    "north": (0, +1),
    "south": (0, -1),
    "east": (+1,0),
    "west": (-1,0)
}

current_coord = (0, 0)

allowed_verbs = ["go"]
allowed_nouns = ["north", "south", "east" "west"]

def check_exits(current_coord):
    x,y = current_coord
    possible_direction = directions[direction]
    if possible_direction in rooms:
        print("You can go to :", possible_direction)

while True:
    room_name = rooms[current_coord]
    print("You are in", room_name)
    print("Type 'Go' followed a direction")

    command = input("What next? ").lower()
    command1=command.split()
    if len(command1) not in (1, 2):
        print("I can't handle this; my brain hurts")
        continue

    verb = command1[0]
    print(verb)
    if len(command1) == 2:
        noun = command1[1]
    else:
        noun = None
    print(noun)

    if verb not in allowed_verbs:
        print("I don't know what", verb ,"is")

    if noun not in allowed_nouns:
        print("I don't know what", noun ,"is")

    if verb == 'go':
        noun_coordinates=directions[noun]
        x,y = current_coord
        dx, dy = noun_coordinates

        new_coord= ((x+dx),(y+dy))
        print(new_coord)
        if new_coord not in rooms:
            print("You can't go this way")
        else:
            current_coord=new_coord

