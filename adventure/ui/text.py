def run(adventure):
    while True:
        command = input(adventure.user_prompt())
        result = adventure.handle_command("user", command)
        print(result)