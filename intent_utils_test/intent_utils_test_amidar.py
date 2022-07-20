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

"""Tests intent_utils."""

from absl.testing import absltest
from absl.testing import parameterized
from affordances_option_models.env_utils import env_utils_amidar
from affordances_option_models.intent_utils import intent_utils_amidar

Intents = intent_utils_amidar.Intents
IntentStatus = intent_utils_amidar.IntentStatus


class IntentUtilsTest(parameterized.TestCase):

  @parameterized.named_parameters(
      {
          'testcase_name': 'Matches passenger state and amidar location',
          'intent_id': ,
      },
      {
          'testcase_name': 'Does not matches passenger state and taxi location',
          'intent_id': ,
      },
      {
          'testcase_name': 'Matches taxi location but not pass state',
          'intent_id': ,
      },
      {
          'testcase_name': 'Matches pass state but not location',
          'intent_id': ,
      },
      {
          'testcase_name': 'Matches pass state outside @ location 1.',
          'intent_id': ,
      },
      {
          'testcase_name': 'Matches pass state outside @ location 2.',
          'intent_id': ,
      },
      {
          'testcase_name': 'Matches pass state outside but wrong location.',
          'intent_id': ,
      },
      {
          'testcase_name': 'Does not match pass state outside @ location.',
          'intent_id': ,
      },
      {
          'testcase_name': 'Random location + passenger inside, incomplete 1.',
          'intent_id': ,
      },
      {
          'testcase_name': 'Random location + passenger inside, incomplete 2.',
          'intent_id': ,
      },
      )
  def test_is_intent_completed(
      self, intent_id, status):

    amidar_state = env_utils_amidar.state_to_int_fn(
        env_utils_amidar.AmidarState(row, col, passenger_status, 0))

    self.assertEqual(
        intent_utils_amidar.is_intent_completed(None, None, amidar_state, intent_id),
        status)


if __name__ == '__main__':
  absltest.main()
