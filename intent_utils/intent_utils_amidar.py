"""Utilities to work with intents in the amidar domain."""

from affordances_option_models.definitions import definitions_amidar
from affordances_option_models.env_utils import env_utils_amidar
from affordances_option_models.option_utils import option_utils_amidar 

Intents = definitions_amidar.Intents
IntentStatus = definitions_amidar.IntentStatus


def is_intent_completed(
    s_i: int,
    option_id: option_utils_amidar.Options,
    s_f: int,
    intent_id: Intents,
    ) -> IntentStatus:
  """Determines if a (state, option, state) transition completes an intent.

  Args:
    s_i: (Unused) The integer representing the taxi state.
    option_id: (Unused) The integer representation of the option.
    s_f: The integer representing the taxi state.
    intent_id: The intent to check the completion for.

  Returns:
    Status of the intent.
  """
  del s_i, option_id  # Unused.

  final_amidar_state = env_utils_amidar.int_to_state_fn(s_f)

  if intent_id not in Intents:
    raise ValueError(
        f'Unknown intent_id={intent_id}. See {Intents} for valid intents.')

  return IntentStatus.incomplete
