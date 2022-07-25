"""Definitions for constants, options, intents related to the taxienv."""

import enum

JUNCTIONS = list(range(0,87))
INTENT_JUNCTION_FILL = list(range(0,87)) # 5+6+9+6+9+6+10+8+13+8+7=87 number of junctions
INTENT_JUNCTION_ESCAPE = list(range(87,87*2)) 

@enum.unique
class ActionMap(enum.IntEnum):
  """Maps human readable actions to the corresponding env integers."""
  NOOP = 0
  FIRE = 1 # basically noop for all except space invaders
  UP = 2
  RIGHT = 3
  LEFT = 4
  DOWN = 5

JUNCTION_TO_INTENT_MAPPING = { JUNCTIONS[i]: [INTENT_JUNCTION_FILL[i], INTENT_JUNCTION_ESCAPE[87+i]] 
  for i in range(0,87) }


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
  OptionsFill = list(range(0,357)) # 357 = total number of tracks
  OptionsEscape = list(range(357,357*2)) # escape the five enemies

# pylint: enable=invalid-name

# See https://docs.python.org/3/library/enum.html#iteration.
