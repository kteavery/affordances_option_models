from typing import Any, NamedTuple, Tuple
import gym
import numpy as np

from affordances_option_models.definitions import definitions_taxi

Colors = definitions.Colors
PASSENGER_INSIDE_CAR_STATUS = 4
# These are the "goal" states in which you cannot enter unless you complete the
# goal of dropping the passenger in the right place. We use these values in
# RL algorithms to mask the transition from here to anywhere.
GOAL_STATES = (0, 85, 410, 475)


class TaxiState(NamedTuple):
  """Human readable version of taxi state."""
  row: int
  col: int
  # Passenger status can be 0, 1, 2, 3, 4 where 0-3 represent where the
  # passenger is in one of the 4 goal locations and 4 represents the passenger
  # inside the car.
  passenger_status: int
  destination: int

  def validate(self):
    if self.passenger_status > PASSENGER_INSIDE_CAR_STATUS:
      raise ValueError('Passenger is in undefined location.')
    if self.destination > 3:
      raise ValueError('Only 4 possible destinations are valid.')
    if not 0 <= self.row <= 4:
      raise ValueError('Row must be between (0, 4)')
    if not 0 <= self.col <= 4:
      raise ValueError('Col must be between (0, 4)')


def make_space_invaders_environment():
  return gym.make('SpaceInvaders').env


_GLOBAL_ENV = make_taxi_environment()
NUM_STATES = _GLOBAL_ENV.nS
NUM_ACTIONS = _GLOBAL_ENV.nA


def state_to_int_fn(taxi_state: TaxiState) -> int:
  """Converts a readable state in the environment to the integer state."""
  taxi_state.validate()
  return _GLOBAL_ENV.encode(*taxi_state)


def int_to_state_fn(x: int) -> TaxiState:
  """Converts an integer representation of state into a human readable one."""
  state = TaxiState(*_GLOBAL_ENV.decode(x))
  state.validate()
  return state

# Maps human readable color from the visualization into one of 4 goal states.
COLOR_TO_LOCATION_MAPPING = {
    Colors.R: _GLOBAL_ENV.locs[0],
    Colors.G: _GLOBAL_ENV.locs[1],
    Colors.Y: _GLOBAL_ENV.locs[2],
    Colors.B: _GLOBAL_ENV.locs[3]
}

# Maps the 4 goal states to a human readable color.
LOCATION_TO_COLOR_MAPPING = {v: k for k, v in COLOR_TO_LOCATION_MAPPING.items()}


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
