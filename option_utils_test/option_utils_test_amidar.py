"""Tests for option_utils."""

from absl.testing import absltest
from absl.testing import parameterized
from affordances_option_models.definitions import definitions_amidar
from affordances_option_models.env_utils import env_utils_amidar
from affordances_option_models.option_utils import option_utils_amidar

Options = option_utils_amidar.Options
OptionsAny = option_utils_amidar.OptionsAny
OptionsDropping = option_utils_amidar.OptionsDropping
OptionsPicking = option_utils_amidar.OptionsPicking
ActionMap = definitions_amidar.ActionMap


class OptionUtilsTest(parameterized.TestCase):

  def test_number_of_options(self):
    continue

  @parameterized.named_parameters(
      #   GoToXX_Any:
      #     - Grid cell of s_tp1 must match the grid cell XX.
      {
          'testcase_name': 'GoTo 0 passenger inside. Dropping',
          'option': ,
      },
      {
          'testcase_name': 'GoTo 0 passenger inside. Picking',
          'option': ,
      },
      {
          'testcase_name': 'GoTo 0 passenger outside. Picking',
          'option': ,
      },
      {
          'testcase_name': 'GoTo 3 from 2 + East succeeds.',
          'option': ,
      },
      {
          'testcase_name': 'GoTo (1, 3) from (0, 3) + South succeeds.',
          'option': ,
      },
      {
          'testcase_name': 'GoTo (1, 3) from (0, 3) + EAST Fails.',
          'option': ,
      },
      {
          'testcase_name': 'GoTo 2 from 2 + East fails.',
          'option': ,
      },
      {
          'testcase_name': 'Drop passenger in taxi at 0',
          'option': ,
      },
      {
          'testcase_name': 'Fail to drop passenger @ 0 (not in vehicle) at 0',
          'option': ,
      },
      {
          'testcase_name': 'Fail to drop passenger @ 2 (not in vehicle) at 0',
          'option': ,
      },
      {
          'testcase_name': 'Drop passenger in vehicle at (0, 2)',
          'option': ,
      },
      {
          'testcase_name':
              'Fail Drop passenger in vehicle at (0, 1) when at (0, 2)',
          'option': ,
      },
      {
          'testcase_name': 'Cannot pickup when action is move.',
          'option': ,
      },
      {
          'testcase_name': 'Fail to pickup passenger already inside.',
          'option': ,
      },
      {
          'testcase_name': 'Try to pickup passenger @ 2 at 0',
          'option': ,
      },
      {
          'testcase_name': 'Try to pickup passenger @ 0 at 0',
          'option': ,
      },
      )
  def test_check_option_termination(
      self, action, option, outcome):

    amidar_state = env_utils_amidar.state_to_int_fn(
        env_utils_amidar.AmidarState(row, col, 0))

    self.assertEqual(
        option_utils_amidar.check_option_termination(amidar_state, action, option),
        outcome)


if __name__ == '__main__':
  absltest.main()
