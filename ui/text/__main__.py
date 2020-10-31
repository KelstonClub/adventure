import npyscreen

class App(npyscreen.NPSApp):
    def main(self):
        screen = npyscreen.Form(name = "Welcome to this Adventure game.\n")
        adventure_name = screen.add(npyscreen.TitleText, name="Adventure name:", )
        player_name = screen.add(npyscreen.TitleText, name="Player name:",)
        screen.edit()

        with open("log.txt", "w") as f:
            f.write(f"Adv. name: {adventure_name.value}\nPlyr. name: {player_name.value}\n")
        
        while True:
            screen.display()

if __name__ == "__main__":
    app = App()
    app.run()
