from ..lib import adventurelib

class Adventure(adventurelib.Adventure):

    name = "House"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

