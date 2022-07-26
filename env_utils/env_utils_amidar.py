from typing import Any, NamedTuple, Tuple
import gym
import numpy as np
import toybox
from toybox.envs.atari.amidar import AmidarEnv

from affordances_option_models.definitions import definitions_amidar


junctions = definitions_amidar.JUNCTIONS
junction_locations = definitions_amidar.JUNCTION_LOCATIONS

class AmidarState(NamedTuple):
  """Human readable version of amidar state."""
  row: int
  col: int
  destination: int

  def validate(self):
    if self.destination > 55:
      raise ValueError('Only 56 possible destinations are valid.')
    if not 0 <= self.row <= 31:
      raise ValueError('Row must be between (0, 31)')
    if not 0 <= self.col <= 30: 
      raise ValueError('Column must be between (0, 30)')


def make_amidar_environment():
  print(AmidarEnv)
  return AmidarEnv #gym.make('Amidar').env 

_GLOBAL_ENV = make_amidar_environment()
NUM_STATES = 362
NUM_ACTIONS = 6


def state_to_int_fn(amidar_state: AmidarState) -> int:
  """Converts a readable state in the environment to the integer state."""
  amidar_state.validate()
  return _GLOBAL_ENV.encode(*amidar_state)


def int_to_state_fn(x: int) -> AmidarState:
  """Converts an integer representation of state into a human readable one."""
  state = AmidarState(*_GLOBAL_ENV.decode(x))
  state.validate()
  return state


LOCATION_TO_JUNCTION_MAPPING = {v: k for k, v in zip(junctions, junction_locations)}


def grid_cell_to_xy(pos: int, grid_size: int = 5) -> Tuple[int, int]:
  """Converts an integer from 0-24 into an (x, y) position."""
  num_cells = grid_size * grid_size - 1
  if not 0 <= pos <= num_cells:
    raise ValueError(f'Grid cell does not exist in grid of size {grid_size}')
  x = pos // grid_size
  y = pos % grid_size
  return (x, y)


def get_transition_and_reward_matrices() -> Tuple[Any, np.ndarray, np.ndarray]:
  """Obtains transition and reward matrices for taxi as numpy arrays.

  Use these quantities to do value iteration and obtain the best possible
  flat policy.

  Returns:
    P: The internal dictionary representation of the transition matrix as given
      by Gym.
    P_matrix: A |S| x |A| x |S| probability transition matrix where P[s, a, s']
      represents the probability of transitioning from state s, to s' by taking
      action a.
    R_matrix: A |S| x |A| matrix representing where R[s, a] represents the
      reward obtained by taking action a from state s.
  """
  # pylint: disable=invalid-name
  P = {
      s: {a: [tup[:3] for tup in tups] for (a, tups) in a2d.items()
         } for (s, a2d) in _GLOBAL_ENV.P.items()
  }
  P_matrix = np.zeros((NUM_STATES, NUM_ACTIONS, NUM_STATES), dtype=np.float32)
  R_matrix = np.zeros((NUM_STATES, NUM_ACTIONS))
  # pylint: enable=invalid-name
  for (s, transition) in P.items():
    for a in range(NUM_ACTIONS):
      prob, sprime, reward = transition[a][0]
      P_matrix[s, a, sprime] = prob
      R_matrix[s, a] = reward
  return P, P_matrix, R_matrix
