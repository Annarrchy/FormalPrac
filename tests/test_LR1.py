import unittest
from LR1 import *

class MyTestCase(unittest.TestCase):
    LR = LR1_Parser()
    def test_cnf_easy(self):
        self.LR.create("tests/cnf_grammar_easy.txt")
        self.assertEqual(self.LR.predict("abb"), True)
        self.assertEqual(self.LR.predict("abbbbbbbbbbbb"), True)
        self.assertEqual(self.LR.predict("aabbb"), False)


    def test_cnf_normal(self):
        self.LR.create("tests/cnf_grammar_normal.txt")
        self.assertEqual(self.LR.predict("aaabbbcc"), True)
        self.assertEqual(self.LR.predict("aaabbbcccc"), True)
        self.assertEqual(self.LR.predict("aaabbb"), False)


    def test_cnf_extreme(self):
        self.LR.create("tests/cnf_grammar_extreme.txt")
        self.assertEqual(self.LR.predict("aac"), True)
        self.assertEqual(self.LR.predict("bbabacb"), True)
        self.assertEqual(self.LR.predict("aacbabbacbddbcadb"), False)


    def test_confree_easy(self):
        self.LR.create("tests/confree_grammar_easy.txt")
        self.assertEqual(self.LR.predict("baa"), True)
        self.assertEqual(self.LR.predict("ccaabcacaaa"), True)
        self.assertEqual(self.LR.predict("ccccab"), False)

    def test_confree_normal(self):
        self.LR.create("tests/confree_grammar_normal.txt")
        self.assertEqual(self.LR.predict("ddbab"), True)
        self.assertEqual(self.LR.predict("abbbdbe"), True)
        self.assertEqual(self.LR.predict("abdceaedbca"), False)


    def test_confree_extreme(self):
        self.LR.create("tests/confree_grammar_extreme.txt")
        self.assertEqual(self.LR.predict("caacfdd"), True)
        self.assertEqual(self.LR.predict("faccccccfedaeacaeaccfbc"), True)
        self.assertEqual(self.LR.predict("adcbedfadcfeffadcb"), False)



if __name__ == '__main__':
    unittest.main()
