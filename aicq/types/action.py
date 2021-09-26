from enum import Enum

class Action(Enum):

    LOOKING = "looking"
    TYPING = "typing"

    def __str__(self):
      return self.value