from typing import Any, NamedTuple, Tuple
import gym
import numpy as np

from affordances_option_models.definitions import definitions_amidar


class AmidarState(NamedTuple):
  """Human readable version of amidar state."""

  def validate(self):
    continue


def make_amidar_environment():
  return gym.make('Amidar').env


_GLOBAL_ENV = make_amidar_environment()
NUM_STATES = _GLOBAL_ENV.nS
NUM_ACTIONS = _GLOBAL_ENV.nA


def state_to_int_fn(amidar_state: AmidarState) -> int:
  """Converts a readable state in the environment to the integer state."""
  amidar_state.validate()
  return _GLOBAL_ENV.encode(*amidar_state)


def int_to_state_fn(x: int) -> AmidarState:
  """Converts an integer representation of state into a human readable one."""
  state = AmidarState(*_GLOBAL_ENV.decode(x))
  state.validate()
  return state
  

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
  num_states = _GLOBAL_ENV.nS
  num_actions = _GLOBAL_ENV.nA
  # pylint: disable=invalid-name
  P = {
      s: {a: [tup[:3] for tup in tups] for (a, tups) in a2d.items()
         } for (s, a2d) in _GLOBAL_ENV.P.items()
  }
  P_matrix = np.zeros((num_states, num_actions, num_states), dtype=np.float32)
  R_matrix = np.zeros((num_states, num_actions))
  # pylint: enable=invalid-name
  for (s, transition) in P.items():
    for a in range(num_actions):
      prob, sprime, reward = transition[a][0]
      P_matrix[s, a, sprime] = prob
      R_matrix[s, a] = reward
  return P, P_matrix, R_matrix
