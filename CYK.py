# Algorithm CYK


def read_grammar(filename):
    """
    reads the rules of a context free grammar
    param filename: name of the text file in current directory
    return: two lists. v_rules lead to variables and t_rules
    lead to terminals.
    """
    grammar = open(filename)
    rules = grammar.readlines()
    v_rules = []
    t_rules = []
    for rule in rules:
        left, right = rule.split(" -> ")

            # for two or more results from a variable
        right = right[:-1].split(" | ")
        for ri in right:

                # it is a terminal
            if str.islower(ri):
                t_rules.append([left, ri])

                # it is a variable
            else:
                v_rules.append([left, ri])
    grammar.close()
    return v_rules, t_rules


def create_cell(first, second):
    """
    creates set of string from concatenation of each character in first
    to each character in second
    param first: first set of characters
    param second: second set of characters
    return: set of desired values
    """
    res = set()
    if first == set() or second == set():
        return set()
    for f in first:
        for s in second:
            res.add(f+s)
    return res


def CYK(varies, terms, inp):
    """
    param varies: rules lead to variables
    param terms: rules lead to terminals
    param inp: input string
    return: resulting table
    """

    length = len(inp)
    var0 = [va[0] for va in varies]
    var1 = [va[1] for va in varies]
    table = [[set() for _ in range(length-i)] for i in range(length)]

    # deal with variables
    for i in range(length):
        for te in terms:
            if inp[i] == te[1]:
                table[0][i].add(te[0])


    # deal with terminals
    for i in range(1, length):
        for j in range(length - i):
            for k in range(i):
                row = create_cell(table[k][j], table[i-k-1][j+k+1])
                for ro in row:
                    for p in range(len(var1)):
                        if ro == var1[p]:
                            table[i][j].add(var0[p])

    # if the last element of table contains "S" the input belongs to the grammar
    return table


def show_result(tab, inp):
    """
    this function prints the procedure of cyk
    param tab: table
    param inp: input
    """
    for c in inp:
        print("\t{}".format(c), end="\t")
    print()
    for i in range(len(inp)):
        print(i+1, end="")
        for c in tab[i]:
            if c == set():
                print("\t{}".format("_"), end="\t")
            else:
                print("\t{}".format(c), end=" ")
        print()

def check(var_rules, term_rules, word):
    table = CYK(var_rules, term_rules, word)
    #show_result(table, word)
    if 'S' in table[len(word) - 1][0]:
        return ("The input word can be derived by this CNF grammar!")
    else:
        return ("The input word can not be derived by this CNF grammar!")
