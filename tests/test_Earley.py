import unittest
from Earley import *

class MyTestCase(unittest.TestCase):

    yes = "The input word can be derived by this context-free grammar!"
    no = "The input word can not be derived by this context-free grammar!"

    def test_cnf_easy(self):
        rules = read_grammar("tests/cnf_grammar_easy.txt")
        self.assertEqual(Earley(rules).check("abb"), self.yes)
        self.assertEqual(Earley(rules).check("abbbbbbbbbbbb"), self.yes)
        self.assertEqual(Earley(rules).check("aabbb"), self.no)


    def test_cnf_normal(self):
        rules = read_grammar("tests/cnf_grammar_normal.txt")
        self.assertEqual(Earley(rules).check("aaabbbcc"), self.yes)
        self.assertEqual(Earley(rules).check("aaabbbcccc"), self.yes)
        self.assertEqual(Earley(rules).check("aaabbb"), self.no)


    def test_cnf_extreme(self):
        rules = read_grammar("tests/cnf_grammar_extreme.txt")
        self.assertEqual(Earley(rules).check("accdb"), self.yes)
        self.assertEqual(Earley(rules).check("cbbcbabcbbb"), self.yes)
        self.assertEqual(Earley(rules).check("aacbabbacbddbcadb"), self.no)


    def test_confree_easy(self):
        rules = read_grammar("tests/confree_grammar_easy.txt")
        self.assertEqual(Earley(rules).check("baa"), self.yes)
        self.assertEqual(Earley(rules).check("ccaabcacaaa"), self.yes)
        self.assertEqual(Earley(rules).check("ccccab"), self.no)

    def test_confree_normal(self):
        rules = read_grammar("tests/confree_grammar_normal.txt")
        self.assertEqual(Earley(rules).check("ddbab"), self.yes)
        self.assertEqual(Earley(rules).check("abadbbcbe"), self.yes)
        self.assertEqual(Earley(rules).check("abdceaedbca"), self.no)


    def test_confree_extreme(self):
        rules = read_grammar("tests/confree_grammar_extreme.txt")
        self.assertEqual(Earley(rules).check("caaafbc"), self.yes)
        self.assertEqual(Earley(rules).check("dcbfedaeaccccccfdfedaeacd"), self.yes)
        self.assertEqual(Earley(rules).check("adcbedfadcfeffadcb"), self.no)

if __name__ == '__main__':
    unittest.main()
