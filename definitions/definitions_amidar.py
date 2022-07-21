"""Definitions for constants, options, intents related to the taxienv."""

import enum

@enum.unique
class Junctions(enum.Enum):
  junctions = list(range(87))


@enum.unique
class ActionMap(enum.IntEnum):
  """Maps human readable actions to the corresponding env integers."""
  NOOP = 0
  FIRE = 1 # basically noop for all except space invaders
  UP = 2
  RIGHT = 3
  LEFT = 4
  DOWN = 5


# pylint: disable=invalid-name
@enum.unique
class Intents(enum.Enum):
  IntentJunctionFill = [0]*87 # 5+6+9+6+9+6+10+8+13+8+7=87 number of junctions
  for x in IntentJunctionFill:
      x = enum.auto()

  IntentJunctionEscape = [0]*87 
  for y in IntentJunctionEscape:
      y = enum.auto()
# pylint: enable=invalid-name

JUNCTION_TO_INTENT_MAPPING = { Junctions.junctions[i]: [Intents.IntentJunctionFill[i], Intents.IntentJunctionEscape[i]] 
  for i in range(0,357) }


class IntentStatus(enum.IntEnum):
  """Indicates if intents were completed or not."""
  complete = 1
  incomplete = 0

_NUM_GRID_CELLS = 357

# Unfortunately, we have to define each option explicitly to avoid the
# limitations of the functional API given here:
# https://docs.python.org/3.6/library/enum.html#functional-api
# Disable linter since the `_` is important for option completion logic.
# pylint: disable=invalid-name
@enum.unique
class Options(enum.Enum):
  """Options as defined by us in the amidar environment."""
  OptionsFill = [0]*357 # 357 = total number of tracks
  for x in OptionsFill:
      x = enum.auto()

  OptionsEscape = [0]*357 # escape the five enemies
  for y in OptionsEscape:
      y = enum.auto()
# pylint: enable=invalid-name

# See https://docs.python.org/3/library/enum.html#iteration.
