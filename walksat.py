from sat_solver import SatSolver
import random


class WalksatSolver(SatSolver):
    def satisfiable(self, max_flip=300, p=0.5):
        print("Checking for satisfiability")
        model = {i: round(random.random()) for i in range(1, self.num_el + 1)}

        for i in range(max_flip):
            if self.solve(model):
                result_str = ""
                for l in range(1, self.num_el + 1):
                    result_str += str(model.get(l, "x"))
                print("The formula is solved by the interpretation: ", result_str)
                return result_str

            a = random.randint(0, self.num_clauses - 1)
            while any([model[at] if at > 0 else not model[-at] for at in self.clauses[a][:-1]]):
                a = random.randint(0, self.num_clauses - 1)
            failed_clause = self.clauses[a][:-1]

            if random.random() > p:
                flip_idx = random.randint(0, len(failed_clause) - 1)
            else:
                flip_idx = 0
                max_positive_clauses = 0
                for j in range(len(failed_clause)):
                    model[abs(failed_clause[j])] = 1 * (not model[abs(failed_clause[j])])
                    positive_clauses = sum(
                        [any([model[at] if at > 0 else not model[-at] for at in c[:-1]]) for c in self.clauses]
                    )
                    if positive_clauses > max_positive_clauses:
                        max_positive_clauses = positive_clauses
                        flip_idx = j
                    model[abs(failed_clause[j])] = 1 * (not model[abs(failed_clause[j])])

            model[abs(failed_clause[flip_idx])] = 1 * (not model[abs(failed_clause[flip_idx])])

        print("No solutions found")
        return False