class Constraint:

    def __init__(self, participants, constraint_fn, constraint_str):
        """
        @param should be a tuple with exactly 2 items - the participants involved
        @param `constraint_fn` should be a function that takes a dictionary with the participants as keys
        @param `constraint_str` should be a string representation for the constraint
        """
        if len(participants) != 2:
            raise Exception("Exactly 2 participants must be provided")

        self.participants = participants
        self.fn = constraint_fn
        self.s = constraint_str

    def get_participants(self):
        return self.participants

    def get_other_participant(self, p1):
        return [p for p in self.participants if p != p1][0]

    def satisfy(self, p):
        return self.fn(p)

    def __str__(self):
        return f"{self.s}"

    def __repr__(self):
        return f"{self.s}"

    def __eq__(self, other):
        return self.s == other.s


def ac(X, D, C):
    # **Takes** variables X, domains D, constraints C
    # **Gives** arc consistent domains for variables
    D_new = {}
    todo = []

    for x in X:
        D_new[x] = D[x]
        # add to todo all arcs from x to a constraint involving x
        # get all constraints involving x and add them to  todo
        todo.extend(
            [(x, c) for c in C if x in c.get_participants() and (x, c) not in todo]
        )  # make sure no duplicates are added

    print(f"\nD: {D_new}")
    print(f"Q: {todo}\n\n")

    while len(todo) > 0:
        print("--------------------------")
        (x, c) = todo.pop()

        y = c.get_other_participant(x)
        print(f"x:\t{x}\ny:\t{y}")
        print(f"checking arc: ({x}, '{c}')\n")

        label = f"\n[ where x={x} ]\n"
        domain_changed = False
        for value_x in D_new[x]:

            remove_me = True
            for value_y in D_new[y]:
                cond = c.satisfy({x: value_x, y: value_y})
                print(f"{x}:\t{value_x}\n{y}:\t{value_y}\n{c} = {cond}\n")
                if cond:
                    print(label)
                    print(f"should not remove {value_x} from D(x)={D_new[x]}")
                    remove_me = False
                    break

            if remove_me:
                print(label)
                print(f"should remove {value_x} from D(x)={D_new[x]}")
                D_new[x] = [v for v in D_new[x] if v != value_x]
                print(f"updated domain for x={x} is D(x)={D_new[x]}\n")
                domain_changed = True

        if domain_changed:
            # get all constraints involving x
            # for each constraint get all its participants which are not x
            # for each participant get all its constraints containing x

            # add to todo all arcs from other variables to constraints involving x
            affected_arcs = []
            for ci in C:
                if x in ci.get_participants():
                    y = c.get_other_participant(x)
                    for cj in C:
                        if x in cj.get_participants():
                            affected_arcs.append((x, cj))
            print(f"domain changed\nmust recheck arcs: {affected_arcs}\n")
            todo.extend(
                [arc for arc in affected_arcs if arc not in todo]
            )  # make sure no duplicates are added

        print(f"D': {D_new}\n")


if __name__ == "__main__":

    X = ["a", "b", "c"]

    D = {
        "a": [1, 2, 3],
        "b": [1, 2, 3],
        "c": [1, 2, 3],
    }

    C1 = Constraint(("a", "b"), lambda p: p["a"] < p["b"], "a < b")
    C2 = Constraint(("b", "c"), lambda p: p["b"] < p["c"], "b < c")

    C = [C1, C2]

    ac(X, D, C)
