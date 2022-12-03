import unittest
from CYK import *

class MyTestCase(unittest.TestCase):

    yes = "The input word can be derived by this CNF grammar!"
    no = "The input word can not be derived by this CNF grammar!"

    def test_easy(self):
        var_rules, term_rules = read_grammar("tests/grammar_easy.txt")
        self.assertEqual(check(var_rules, term_rules, "abb"), self.yes)
        self.assertEqual(check(var_rules, term_rules, "abbbbbbbbbbbb"), self.yes)
        self.assertEqual(check(var_rules, term_rules, "aabbb"), self.no)


    def test_normal(self):
        var_rules, term_rules = read_grammar("tests/grammar_normal.txt")
        self.assertEqual(check(var_rules, term_rules, "aaabbbcc"), self.yes)
        self.assertEqual(check(var_rules, term_rules, "aaabbbcccc"), self.yes)
        self.assertEqual(check(var_rules, term_rules, "aaabbb"), self.no)


    def test_extreme(self):
        var_rules, term_rules = read_grammar("tests/grammar_extreme.txt")
        self.assertEqual(check(var_rules, term_rules, "accdb"), self.yes)
        self.assertEqual(check(var_rules, term_rules, "cbbcbabcbbb"), self.yes)
        self.assertEqual(check(var_rules, term_rules, "aacbabbacbddbcadb"), self.no)


if __name__ == '__main__':
    unittest.main()
