#Algorithm Earley

''' terminals - a-z
    non-terminals A-Z
    start - non-terminal S
    empty symbol is an empty string'''

class Rule:
    def __init__(self, left_side: str, right_side: str):
        self.left = left_side
        self.right = right_side

class Situation:
    def __init__(self, left_side: str, right_side: str, point_cord: int, offset: int):
        self.left_side = left_side
        self.right_side = right_side
        self.point_cord = point_cord
        self.offset = offset

    def __hash__(self):
        return hash((self.left_side, self.right_side, self.point_cord, self.offset))

    def __eq__(self, other):
        is_eq = self.left_side == other.left_side and self.right_side == other.right_side
        is_eq = is_eq and self.offset == other.offset and self.point_cord == other.point_cord
        return is_eq

def read_grammar(filename):
    """
    reads the rules of a context free grammar
    param filename: name of the text file in current directory
    return: list of Rules
    """
    grammar = open(filename)
    rules = grammar.readlines()
    res_rules = []

    for rule in rules:
        left, right = rule.split(" -> ")
        # for two or more results from a variable
        right = right[:-1].split(" | ")
        for ri in right:
            res_rules.append(Rule(left, ri))
    grammar.close()
    return res_rules

class Earley:

    def __init__(self, rules: list):
        self.rules = []
        self.rules.append(Rule('#', 'S'))  # help rule
        self.rules += rules
        self.word = ""
        self.lists_of_situations = []


    def scan(self, step):
        """
            param step: number of symbol to scan
        """
        for trans in self.lists_of_situations[step - 1]:
            if trans.point_cord < len(trans.right_side) and trans.right_side[trans.point_cord] == self.word[step - 1]:
                new_trans = Situation(trans.left_side, trans.right_side, trans.point_cord + 1, trans.offset)
                self.lists_of_situations[step].add(new_trans)


    def predict(self, step):
        new_set = set()
        for trans in self.lists_of_situations[step]:
            if trans.point_cord == len(trans.right_side):
                continue
            waiting_left = trans.right_side[trans.point_cord]
            for rule in self.rules:
                if rule.left == waiting_left:
                    new_trans = Situation(rule.left, rule.right, 0, step)
                    new_set.add(new_trans)
        self.lists_of_situations[step].update(new_set)


    def complete(self, j):
        new_set = set()
        for trans in self.lists_of_situations[j]:
            if trans.point_cord < len(trans.right_side):
                continue
            for wait_trans in self.lists_of_situations[trans.offset]:
                if wait_trans.point_cord < len(wait_trans.right_side) and \
                        wait_trans.right_side[wait_trans.point_cord] == trans.left_side:
                    new_trans = Situation(wait_trans.left_side, wait_trans.right_side, wait_trans.point_cord + 1,
                                          wait_trans.offset)
                    new_set.add(new_trans)
        self.lists_of_situations[j].update(new_set)


    def check(self, word: str):
        """
            checks if word can be derived by grammar
            param word: word to check
        """
        self.word = word
        self.lists_of_situations = []
        length = len(word) + 1
        # list of situation initialization
        for _ in range(length): self.lists_of_situations.append(set())
        self.lists_of_situations[0].add(Situation('#', 'S', 0, 0))  # first add
        for iter in range(0, length):
            if iter:
                self.scan(iter)
            sz = len(self.lists_of_situations[iter])
            while True:
                self.complete(iter)
                self.predict(iter)
                if sz == len(self.lists_of_situations[iter]):  # check changing
                    break
                else:
                    sz = len(self.lists_of_situations[iter])
        if Situation('#', 'S', 1, 0) in self.lists_of_situations[-1]:  # check result
            return("The input word can be derived by this context-free grammar!")
        else:
            return("The input word can not be derived by this context-free grammar!")
