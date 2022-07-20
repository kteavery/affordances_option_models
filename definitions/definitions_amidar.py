# Copyright 2021 DeepMind Technologies Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Definitions for constants, options, intents related to the taxienv."""

import enum


@enum.unique
class ActionMap(enum.IntEnum):
  """Maps human readable actions to the corresponding env integers."""
  continue


# pylint: disable=invalid-name
@enum.unique
class Intents(enum.Enum):
  continue
# pylint: enable=invalid-name


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
  """Options as defined by us in the amidar environment.
  """
  continue
# pylint: enable=invalid-name

# See https://docs.python.org/3/library/enum.html#iteration.
