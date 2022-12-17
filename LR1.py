import string

class Rule:
    def __init__(self, id, left, right):
        self.id = id
        self.left = left
        self.right = right


class State:
    def __init__(self, left, right, dot_pos, follow, id):
        self.id = id
        self.left = left
        self.right = right
        self.dot_pos = dot_pos
        self.follow = follow
        self.dot_val = (
            self.right[self.dot_pos] if self.dot_pos < len(self.right) else ""
        )
        self.is_last = 1 if self.dot_pos >= max(len(self.right) - 1, 0) else 0

    def move_dot(self):
        return State(
            self.left,
            self.right,
            min(self.dot_pos + 1, len(self.right)),
            self.follow,
            self.id,
        )

    def next_symbol(self):
        return self.right[self.dot_pos + 1]

    def check_empty(self):
        return self.dot_pos == len(self.right)

    def __hash__(self):
        return hash(
            self.left
            + "->"
            + self.right[: self.dot_pos]
            + "."
            + self.right[self.dot_pos :]
            + ","
            + str(self.follow)
        )

    def __eq__(self, other):
        if (
            self.left == other.left
            and self.right == other.right
            and self.dot_pos == other.dot_pos
            and self.follow == other.follow
            and self.dot_val == other.dot_val
            and self.is_last == other.is_last
        ):
            return True
        else:
            return False


class Vertex:
    def __init__(self, states):
        self.states = states
        self.routines = dict()
        self.empties = set()

    def __hash__(self):
        return hash("(" + str(self.states) + ":" + str(self.routines) + ")")

    def __eq__(self, other):
        if self.states == other.states:
            return True
        else:
            return False


class Cell:
    def __init__(self, typ, value):
        self.type = typ  # 1 for shift and 0 for reduce
        self.value = value

    def __eq__(self, other):
        if self.type == other.type and self.value == other.value:
            return True
        else:
            return False


def get_key(val, my_dict):
    for key, value in my_dict.items():
        if val == value:
            return key


def find_rule(rules, id):
    for rule_list in rules.values():
        for rule in rule_list:
            if rule.id == id:
                return rule


class LR1_Parser:

    def create(self, filename):
        self.table = dict()
        self.terms = list(string.ascii_lowercase)
        self.non_terms = list(string.ascii_uppercase)
        self.non_terms.append("&")
        self.rules = self.read_grammar(filename)
        self.first = dict()
        self.build_first()
        self.vertices = dict()
        self.stack = []
        item = State("&", "S", 0, {"$"}, 0)
        self.vertices[0] = Vertex(self.closure(item))
        self.stack.append([self.vertices[0], 0])
        while self.stack:
            self.act(self.stack[0][0], self.stack[0][1])
            self.stack.pop(0)
        self.build_table()


    def read_grammar(self, filename):
        rules = dict()
        for i in self.non_terms:
            rules[i] = set()
        grammar = open(filename)
        rules_list = grammar.readlines()
        count = 1
        for rule in rules_list:
            left, right = rule.split(" -> ")
            right = right[:-1].split(" | ")
            for ri in right:
                res_rule = Rule(count, left, ri)
                rules[res_rule.left].add(res_rule)
                count += 1
        grammar.close()

        rules["&"].add(Rule(0, "&", "S"))
        return rules


    def build_first(self):
        for sym in self.non_terms:
            self.first[sym] = set()
        for sym in self.non_terms:
            checked = []
            self.set_first(sym, sym, checked)


    def set_first(self, f_sym, cur_sym, checked):
        if cur_sym in self.terms:
            self.first[f_sym].add(cur_sym)
        elif cur_sym in self.non_terms:
            for rule in self.rules[cur_sym]:
                if rule in checked:
                    return
                checked.append(rule)
                self.set_first(f_sym, rule.right[0] if rule.right else "", checked)


    def closure(self, item):
        States = dict()
        States["done"] = set()
        States["todo"] = set()
        States["todo"].add(item)
        while States["todo"]:
            current_state = States["todo"].pop()
            if current_state in States["done"]:
                continue
            if current_state.dot_val in self.terms or current_state.dot_val == "":
                States["done"].add(current_state)
                continue
            for rule in self.rules[current_state.dot_val]:

                if current_state.is_last:
                    States["todo"].add(
                        State(rule.left, rule.right, 0, current_state.follow, rule.id)
                    )
                else:
                    if current_state.next_symbol() in self.non_terms:
                        States["todo"].add(
                            State(
                                left=rule.left,
                                right=rule.right,
                                dot_pos=0,
                                follow=self.first[current_state.next_symbol()],
                                id=rule.id,
                            )
                        )
                    else:
                        States["todo"].add(
                            State(
                                rule.left,
                                rule.right,
                                0,
                                {current_state.next_symbol()},
                                rule.id,
                            )
                        )
            States["done"].add(current_state)
        return States["done"]


    def act(self, vertex, parent_ind):
        for term in self.terms:
            new_states = set()
            for State in vertex.states:
                if State.dot_val == term:
                    new_states.update(self.closure(State.move_dot()))
            if new_states:
                if Vertex(new_states) not in self.vertices.values():
                    self.vertices[parent_ind].routines[term] = len(self.vertices)
                    self.vertices[len(self.vertices)] = Vertex(new_states)
                    self.stack.append(
                        [self.vertices[len(self.vertices) - 1], len(self.vertices) - 1]
                    )
                else:
                    self.vertices[parent_ind].routines[term] = get_key(
                        Vertex(new_states), self.vertices
                    )
        for nterm in self.non_terms:
            new_states = set()
            for State in vertex.states:
                if State.dot_val == nterm:
                    new_states.update(self.closure(State.move_dot()))
            if new_states:
                if Vertex(new_states) not in self.vertices.values():
                    self.vertices[parent_ind].routines[nterm] = len(self.vertices)
                    self.vertices[len(self.vertices)] = Vertex(new_states)
                    self.stack.append(
                        [self.vertices[len(self.vertices) - 1], len(self.vertices) - 1]
                    )
                else:
                    self.vertices[parent_ind].routines[nterm] = get_key(
                        Vertex(new_states), self.vertices
                    )
        for State in vertex.states:
            if State.check_empty():
                self.vertices[parent_ind].empties.add(State)


    def build_table(self):
        for key, value in self.vertices.items():
            self.table[key] = dict()
            for route, dest in value.routines.items():
                self.table[key][route] = Cell(1, dest)
        for key, value in self.vertices.items():
            for empty in value.empties:
                for rule in empty.follow:
                    self.table[key][rule] = Cell(0, empty.id)

    def predict(self, word):
        stack = [0]
        word = word + "$"
        for letter in word:
            while True:
                row = stack[-1]
                row = int(row)
                if not letter in self.table[row].keys():
                    return False
                dest = self.table[row][letter]
                if (dest, letter) == (Cell(0, 0), "$"):
                    return True
                if dest.type:
                    stack.append(letter)
                    stack.append(dest.value)
                    break
                destid = int(dest.value)
                reduce_items = list(find_rule(self.rules, destid).right)
                if reduce_items:
                    if len(stack) <= len(reduce_items) * 2:
                        return False
                    reduce_stack_part = []
                    for i in range(-len(reduce_items) * 2, 0, 2):
                        reduce_stack_part.append(stack[i])
                    if reduce_stack_part != reduce_items:
                        return False
                    stack = stack[: -(len(reduce_items) * 2)]
                rule_left = find_rule(self.rules, destid).left
                current_row = int(stack[-1])
                if not str(self.table[current_row][rule_left]):
                    return False
                stack.append(rule_left)
                stack.append(self.table[current_row][rule_left].value)
        return False