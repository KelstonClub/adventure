def run(adventure):
    while True:
        print("You are in the", adventure.player.location)
        print("You can see", adventure.player.location.inventory)
        print("You have", adventure.player.inventory)
        print("You can go", adventure.player.location.exits.keys())
        command = input("What now? ")
        result = adventure.handle_command("user", command)
        print(result)
