import sys
import pygame
from pygame.locals import *

pygame.init()

SIZE = W, H = 800, 600
GUTTER = 10
BG_COLOUR = (0x00, 0x00, 0x00)
FG_COLOUR = (0xff, 0xff, 0xff)

ROOM_X = 0
ROOM_Y = 0
ROOM_W = 3 * W / 4
ROOM_H = 3 * H / 4
ROOM = Rect(ROOM_X, ROOM_Y, ROOM_W, ROOM_H)

INVENTORY_X = ROOM_X + ROOM_W + GUTTER
INVENTORY_Y = ROOM_Y
INVENTORY_W = W - INVENTORY_X
INVENTORY_H = ROOM_H
INVENTORY = Rect(INVENTORY_X, INVENTORY_Y, INVENTORY_W, INVENTORY_H)

INTERACTION_X = ROOM_X
INTERACTION_Y = ROOM_Y + ROOM_H + GUTTER
INTERACTION_W = W
INTERACTION_H = H - INTERACTION_Y
INTERACTION = Rect(INTERACTION_X, INTERACTION_Y, INTERACTION_W, INTERACTION_H)

class Game(object):

    def __init__(self, adventure):
        self.adventure = adventure
        self.screen = pygame.display.set_mode(SIZE)
        self.load_room_images()
        self.load_item_images()

    def load_images(self, folder, names):
        dirpath = os.path.join(adventure.assets_dirpath(), "images", folder)
        for name in names:
            filepath = os.path.join(dirpath, name + ".jpg")
            if os.path.exists(filepath):
                yield name, filepath

    def load_room_images(self):
        self.room_images = self.load_images("rooms", self.adventure.rooms.keys())

    def load_item_images(self):
        self.item_images = self.load_images("items", self.adventure.items.keys())

    def issue_command(self, type, command):
        return self.adventure.handle_command(type, command)

    def reset_screen(self):
        self.screen.fill(BG_COLOUR)

    def draw_rect(self, rect, colour=BG_COLOUR):
        pygame.draw.rect(self.screen, FG_COLOUR, rect)
        pygame.draw.rect(self.screen, colour, rect.inflate(-GUTTER, -GUTTER))

    def draw_room(self):
        self.draw_rect(ROOM, (0xff, 0x00, 0x00))

    def draw_inventory(self):
        self.draw_rect(INVENTORY, (0x00, 0xff, 0x00))

    def draw_interaction(self):
        self.draw_rect(INTERACTION, (0x00, 0x00, 0xff))

    def draw(self):
        self.reset_screen()
        self.draw_room()
        self.draw_inventory()
        self.draw_interaction()
        pygame.display.flip()

    def handle_keydown(self, event):
        if event.key == pygame.K_q and event.mod & pygame.KMOD_CTRL:
            yield "QUIT"

    def check_events(self):
        user_commands = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                user_commands.append("QUIT")
            elif event.type == KEYDOWN:
                print("KEYDOWN found")
                user_commands.extend(self.handle_keydown(event))

        return user_commands

    def run(self):
        player = self.issue_command("system", "status")

        while True:
            self.draw()
            user_commands = self.check_events()
            for command in user_commands:
                print("Command:", command)
                if command.lower() == "quit":
                    return
                player = self.issue_command("user", command)

def run(adventure):
    return Game(adventure).run()
