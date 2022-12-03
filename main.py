from Earley import *

if __name__ == '__main__':
    rules = read_grammar("grammar.txt")
    input = open("input.txt")
    word = input.read()
    input.close()
    print(Earley(rules).check(word))
