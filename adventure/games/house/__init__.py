from ...lib import adventurelib

class Adventure(adventurelib.Adventure):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def user_prompt(self):
        return "House now? "

