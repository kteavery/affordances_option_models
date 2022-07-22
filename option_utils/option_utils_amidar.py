"""Utilities related to options and learning option policies in Amidar."""
from typing import Optional, Tuple
from absl import logging
import numpy as np

from affordances_option_models.affordance import affordances_amidar
from affordances_option_models.definitions import definitions_amidar
from affordances_option_models.env_utils import env_utils_amidar
from affordances_option_models import rl

Options = definitions_amidar.Options
OptionsFill = definitions_amidar.Options.OptionsFill
OptionsEscape = definitions_amidar.Options.OptionsEscape

_TRANSITION_DICT, _TRANSITION_MATRIX = (
    env_utils_amidar.get_transition_and_reward_matrices()[:-1])


def check_option_termination(
    s_t: int,
    a_t: int,
    option: Options) -> bool:
  """Given an (s, a) transition, determines if an option_id terminates in P.
  """
  if option not in Options:
    raise ValueError(
        f'Unknown Option {option}. Valid: {Options.__members__.values()}')
  
  _, s_tp1, _ = _TRANSITION_DICT[s_t][a_t][0]
  amidar_row, amidar_col, _ = env_utils_amidar.int_to_state_fn(s_tp1)

  print("option.name: ")
  print(option.name)
  grid_idx = option.name
  grid_row, grid_col = env_utils_amidar.grid_cell_to_xy(grid_idx)
  if (amidar_row, amidar_col) == (grid_row, grid_col):
    return True
  else:
    return False


def compute_per_step_matrices_for_option_learning(
    option: Options,
    r_option_completion: float = 1.0,
    r_other: float = 0.0,
    ) -> Tuple[np.ndarray, np.ndarray]:
  """Computes per-step matrices needed to learn option polices.

  Args:
    option: The option for which you want to compute the matrices for.
    r_option_completion: The reward for successful completion of the option.
    r_other: The reward for all other steps of the option.

  Returns:
    1. A matrix containing the per-step rewards for the requested option.
    2. A matrix containing the termination mask for the transition matrix. e.g.
       if the entry (s, a) has a 1, transitions can take place. If it has a zero
       it terminates.
  """
  amidarenv = env_utils_amidar.make_amidar_environment()
  num_states, num_actions = amidarenv.nS, amidarenv.nA
  option_step_reward = np.full((num_states, num_actions), r_other)
  option_transition_mask = np.ones((num_states, num_actions), dtype=np.float)
  for s in range(num_states):
    for a in range(num_actions):
      if check_option_termination(s, a, option):
        option_step_reward[s, a] = r_option_completion
        option_transition_mask[s, a] = 0.0  # No possible transitions from here.

  return option_step_reward, option_transition_mask


def learn_option_policy(
    env: str,
    option: Options,
    gamma: float = rl.DEFAULT_GAMMA,
    stopping_threshold: float = 0.0001,
    max_iterations: int = 10000,
    seed: Optional[int] = None,
    ) -> Tuple[np.ndarray, int]:
  """Learns the low level policy for an option.

  Args:
    option: The option for which to learn the policy.
    gamma: Discount factor in VI.
    stopping_threshold: Stop if the change in value is less than this value.
    max_iterations: Maximum number of iterations to run VI.
    seed: For tie-breaking.

  Returns:
    pi_star: Low level policy, |S| x |A| that achieves the desired option.
  """
  r_option, b_option = compute_per_step_matrices_for_option_learning(option)
  # The transition matrix must be masked to take into account when an option
  # will terminate. For example, if the option termination condition is to go to
  # state X, then it must not be able to go to any other state after. The
  # b_option matrix contains this information and we expand dimensions to
  # automatically broadcast and mask the usual transition matrix.
  b_option = np.expand_dims(b_option, -1)
  masked_transition_matrix = b_option * _TRANSITION_MATRIX
  V_star, _, num_iters = rl.value_iteration(  # pylint: disable=invalid-name
      env=env,
      reward_matrix=r_option,
      transition_matrix=masked_transition_matrix,
      max_iterations=max_iterations,
      stopping_threshold=stopping_threshold,
      gamma=gamma)
  pi_star = rl.extract_greedy_policy(
      env, r_option, masked_transition_matrix, V_star, gamma=gamma, seed=seed)

  return pi_star, num_iters


def learn_policy_over_options(
    env: str, 
    option_reward: np.ndarray,
    option_transition: np.ndarray,
    option_length: np.ndarray,
    gamma: float = rl.DEFAULT_GAMMA,
    stopping_threshold: float = 0.0001,
    max_iterations: int = 10000,
    seed: Optional[int] = None,
    affordances_fn: Optional[affordances_taxi.AffordancesFn] = None,
    writer=None,
    ) -> Tuple[np.ndarray, int]:
  """Learns the policy over option policies.

  Args:
    option_reward: Reward matrix of shape |S| x |O| that determines the
      environment reward for every state option pair.
    option_transition: Transition matrix of shape |S| x |O| x |S| that
      determines the transition state after executing an option in a state.
    option_length: Length matrix of shape |S| x |O| that determines the
      Length of execution for every state option pair.
    gamma: Discount factor in VI.
    stopping_threshold: Stop if the change in value is less than this value.
    max_iterations: Maximum number of iterations to run VI.
    seed: For tie-breaking.
    affordances_fn: Affordances and relevant masking for the bellman update.
    writer: An optional writer to save data.

  Returns:
    pi_star: Policy over options, |S| x |O|.
  """
  if option_length.min() < 1:
    logging.error(
        ('At least one option has a length < 1 at %s (values=%s). Clipping has '
         'occurred.'),
        np.where(option_length < 1)[0],
        option_length[option_length < 1])
    option_length = np.clip(option_length, 1, 100)
  if np.any(option_transition.sum(-1).round(2) > 1):
    raise ValueError(
        'At least one probability distribution from a (state, option) pair '
        'had a sum > 1.')
  if not (np.all(option_transition <= 1) and np.all(option_transition >= 0)):
    raise ValueError(
        'At least one transitition probability is not between (0, 1).')

  gamma = gamma ** option_length
  num_states, num_options = option_reward.shape
  if option_transition.shape != (num_states, num_options, num_states):
    raise ValueError(
        f'Option transition matrix has shape {option_transition.shape}. '
        f'Expected {(num_states, num_options, num_states)}')
  if gamma.shape != (num_states, num_options):
    raise ValueError(
        f'gamma matrix has shape {gamma.shape}. '
        f'Expected {(num_states, num_options)}')

  V_star, _, num_iters = rl.value_iteration(  # pylint: disable=invalid-name
      env=env,
      reward_matrix=option_reward,
      transition_matrix=option_transition,
      max_iterations=max_iterations,
      stopping_threshold=stopping_threshold,
      affordances_fn=affordances_fn,
      gamma=gamma,
      writer=writer)
  pi_star = rl.extract_greedy_policy(
      env, option_reward, option_transition, V_star, gamma=gamma, seed=seed,
      affordances_fn=affordances_fn)

  return pi_star, num_iters
