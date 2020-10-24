class Base:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.name)

class DataBase(Base):

    @classmethod
    def from_namedtuple(cls, info):
        return cls(*info)
