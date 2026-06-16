import unittest
import game.test_suite.utils


class TestUtils(unittest.TestCase):
    """
        `Test Utils Notes:`

        This class tests the functionality of the utils.py file.
    """

    def setUp(self):
        self.utils = game.test_suite.utils
        self.printing: bool = False

    def test_diff_len(self):
        str1, str2 = 'hello', 'worlds!'
        self.assertFalse(self.utils.spell_check(str1, str2, self.printing))

    def test_valid_input(self):
        str1, str2 = 'hello', 'hello'
        self.assertTrue(self.utils.spell_check(str1, str2, self.printing))

    def test_invalid_input(self):
        str1, str2 = 'hello', 'helol'
        self.assertFalse(self.utils.spell_check(str1, str2, self.printing))

    def test_double_space_entry(self):
        str1, str2 = 'hello  me  ', 'hello  me  '
        self.assertTrue(self.utils.spell_check(str1, str2, self.printing))

    def test_long_strings(self):
        str1, str2 = 'hello, how is your day?', 'hello, how is your day?'
        self.assertTrue(self.utils.spell_check(str1, str2, self.printing))

    def test_long_strings_fail(self):
        str1, str2 = 'hello, how is your day?', 'hello. hwo is yruo day!'
        self.assertFalse(self.utils.spell_check(str1, str2, self.printing))
