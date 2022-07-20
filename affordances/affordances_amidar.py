"""Heuristic affordances to aid learning a policy over options."""
from typing import Callable, List, Tuple
from absl import logging
import numpy as np

from affordances_option_models.definitions import definitions_amidar
from affordances_option_models.env_utils import env_utils_amidar


State = int
Option = int
AffordancesList = List[Tuple[State, Option]]
AffordancesFn = Callable[[], np.ndarray]


def _compute_affordance_mask(affordances: AffordancesList) -> np.ndarray:
  """Computes the affordances mask and does some error checking."""
  if not affordances:
    raise ValueError('List of affordances cannot be empty.')
  logging.log_every_n(
      logging.INFO, 'Number of affordances: %s', 10, len(affordances))

  affs = np.zeros(
      (env_utils_amidar.NUM_STATES, len(definitions_amidar.Options))).astype(np.float)
  affs[tuple(zip(*affordances))] = 1.0

  if not np.all(affs.sum(1) >= 1):
    raise ValueError('All states must have at least one option affordable.')
  return affs


def _all_affs() -> AffordancesList:
  """Returns all states + options."""
  affordances = []
  for state in range(env_utils_amidar.NUM_STATES):
    for option in definitions_amidar.Options:
      affordances.append((state, option.value-1))
  return affordances


ALL_AFFORDANCES = {

}


def get_heuristic_affordances_by_name(affordances_name: str) -> AffordancesFn:
  affordances = ALL_AFFORDANCES[affordances_name]()
  mask = _compute_affordance_mask(affordances)
  def _affordance_function():
    return mask
  return _affordance_function
