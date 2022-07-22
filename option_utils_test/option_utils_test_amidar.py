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
    self.assertLen(option_utils_amidar.Options, 714)
    self.assertLen(option_utils_amidar.OptionsFill, 357)
    self.assertLen(option_utils_amidar.OptionsEscape, 357)

  @parameterized.named_parameters(
      #   GoToXX_Any:
      #     - Grid cell of s_tp1 must match the grid cell XX.
      {
          'testcase_name': 'Fill (6, 5) from (6, 6) + DOWN succeeds.',
          'option': Options.OptionsFill[],
          'row': 6,
          'col': 6,
          'action': ActionMap.DOWN,
          'outcome': True,
      },
      {
          'testcase_name': 'Fill (6, 5) from (6, 6) + RIGHT fails.',
          'option': Options.OptionsFill[],
          'row': 6,
          'col': 6,
          'action': ActionMap.RIGHT,
          'outcome': True,
      },
      {
          'testcase_name': 'Escape to (6, 5) from (6, 6) + DOWN succeeds.',
          'option': Options.OptionsEscape[],
          'row': 6,
          'col': 6,
          'action': ActionMap.DOWN,
          'outcome': True,
      },
      {
          'testcase_name': 'Escape to (6, 5) from (6, 6) + RIGHT fails.',
          'option': Options.OptionsEscape[],
          'row': 6,
          'col': 6,
          'action': ActionMap.RIGHT,
          'outcome': True,
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
