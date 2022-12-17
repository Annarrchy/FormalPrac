from LR1 import *

if __name__ == "__main__":
    LR = LR1_Parser()
    LR.create("grammar.txt")
    word_amount = int(input())
    for i in range(word_amount):
        word = input()
        if LR.predict(word):
            print("The input word can be derived by this grammar!")
        else:
            print("The input word can not be derived by this grammar!")
