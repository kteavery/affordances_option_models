"""Definitions for constants, options, intents related to the taxienv."""

import enum

JUNCTIONS = list(range(0,56))
INTENT_JUNCTION_FILL = list(range(0,56)) 
INTENT_JUNCTION_ESCAPE = list(range(56,56*2)) 
_NUM_GRID_CELLS = 357

JUNCTION_LOCATIONS = [(6,0), (12,0), (19,0), (25,0),
                    (0,6), (5,6), (6,6), (12,6), (14,6), (17,6), (19,6), (25,6), (26,6), (31,6), 
                    (0,12), (3,12), (5,12), (11,12), (14, 12), (17,12), (20, 12), (26, 12), (28, 12), (31, 12),
                    (0,18), (3,18), (4,18), (9,18), (11,18), (12,18), (19,18), (20,18), (22,18), (27,18), (28,18), (31,18), 
                    (0,24), (4,24), (6,24), (9,24), (10,24), (12,24), (14,24), (17,24), (19,24), (21,24), (22,24), (25,24), (27,24), (31,24), 
                    (6,30), (10,30), (14,30), (17,30), (21,30), (25,30) ]

@enum.unique
class ActionMap(enum.IntEnum):
  """Maps human readable actions to the corresponding env integers."""
  NOOP = 0
  FIRE = 1 # basically noop for all except space invaders
  UP = 2
  RIGHT = 3
  LEFT = 4
  DOWN = 5

JUNCTION_TO_INTENT_MAPPING = { JUNCTIONS[i]: [INTENT_JUNCTION_FILL[i], INTENT_JUNCTION_ESCAPE[i]] 
  for i in range(0,56) }


class IntentStatus(enum.IntEnum):
  """Indicates if intents were completed or not."""
  complete = 1
  incomplete = 0

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
