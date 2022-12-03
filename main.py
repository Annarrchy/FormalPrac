from CYK import *


if __name__ == '__main__':
    var_rules, term_rules = read_grammar("grammar.txt")
    input = open("input.txt")
    word = input.read()
    print(check(var_rules, term_rules, word))
    input.close()
