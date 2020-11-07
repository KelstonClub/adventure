def run(adventure):
    while True:
        print(adventure.inventory)
        print("You are in %r" % adventure.player.location)
        print("You can go", adventure.player.location.exits)
        print("You can get", adventure.player.location.inventory)
        print("You have", adventure.player.inventory)
        command = input(adventure.user_prompt())
        result = adventure.handle_command("user", command)
        print(result)