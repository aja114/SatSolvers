from sat_solver import SatSolver
from copy import deepcopy


class DpllSolver(SatSolver):
    def satisfiable(self):
        print("Checking for satisfiability")
        formula = deepcopy(self.clauses)
        formula_state = [-1] * self.num_clauses
        literals = [i for i in range(1, self.num_el+1)]
        model = {}

        result, model = self.dpll(formula, formula_state, model, literals)

        if result:
            result_str = ""
            for l in literals:
                result_str += str(model.get(l, "x"))
            print("The formula is solved by the interpretation: ", result_str)
            return result_str

        print("The formula is not satisfiable")
        return False

    def dpll(self, formula, formula_state, model, literals):
        # print("dpll call:")
        # print("model: ", model)
        # print("formula: ", formula)
        # print("formula_state1: ", formula_state)

        formula, formula_state, model = self.propagate(formula, formula_state, model)

        # print("formula_state2: ", formula_state)

        if 0 in formula_state:
            # print("backtracking")
            return False, model

        if all(c == 1 for c in formula_state):
            return True, model

        for l in literals:
            if l not in model:
                break

        # print("decide call, with litteral:")
        # print(l)
        res, model_tmp = self.dpll(*self.update_formula(formula, formula_state, {**model, l: 1, -l: 0}),
                                   literals=literals)
        if res:
            return True, model_tmp
        else:
            # print("decide call, with litteral:")
            # print(-l)
            return self.dpll(*self.update_formula(formula, formula_state, {**model, l: 0, -l: 1}), literals=literals)

    def propagate(self, formula, formula_state, model):
        # print("propagate call:")
        # print(model)
        if all(len(c) != 1 for c in formula):
            return formula, formula_state, model

        for i in range(len(formula)):
            if len(formula[i]) == 1:
                l = formula[i][0]
                formula, formula_state, model = self.update_formula(formula, formula_state, {**model, l: 1, -l: 0})
                return self.propagate(formula, formula_state, model)

    def update_formula(self, formula, formula_state, model):
        new_formula = [[] for _ in range(len(formula))]
        new_formula_state = [i for i in formula_state]
        for i in range(len(formula)):
            if formula_state[i] == -1:
                if len(formula[i]) == 1 and model.get(formula[i][0], 1) == 0:
                    new_formula[i] = []
                    new_formula_state[i] = 0
                else:
                    for l in formula[i]:
                        if l in model.keys():
                            if model[l]:
                                new_formula[i] = []
                                new_formula_state[i] = 1
                                break
                        else:
                            new_formula[i].append(l)

        return new_formula, new_formula_state, model
