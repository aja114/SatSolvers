from copy import deepcopy

clauses = [[1, 2, 0], [-2, -4, 0], [3, 4, 0], [-4, -5, 0], [5, -6, 0], [6, -7, 0], [6, 7, 0], [7, -16, 0],
           [8, -9, 0], [-8, -14, 0], [9, 10, 0], [9, -10, 0], [-10, -11, 0], [10, 12, 0], [11, 12, 0],
           [13, 14, 0], [14, -15, 0], [15, 16, 0]]

# clauses = [[1, 2], [2, 3, -4], [-1, -2], [-1, -3, -4], [1]]
literals = [i for i in range(1, 17)]
interp = {}


def solve(clauses, literals):
    formula = deepcopy(clauses)
    formula_state = [-1 for _ in clauses]
    model = {}

    result, model = dpll(formula, formula_state, model, literals)

    if result:
        result_str = ""
        for l in literals:
            result_str += str(model.get(l, "x"))
        print("The solution is found with: ", result_str)
        return result_str

    print("No solution found")
    return False


def dpll(formula, formula_state, model, literals):
    # print("dpll call:")
    # print("model: ", model)
    # print("formula: ", formula)
    # print("formula_state1: ", formula_state)

    formula, formula_state, model = progagate(formula, formula_state, model)

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
    res, model_tmp = dpll(*update_formula(formula, formula_state, {**model, l: 1, -l: 0}), literals=literals)
    if res:
        return True, model_tmp
    else:
        # print("decide call, with litteral:")
        # print(-l)
        return dpll(*update_formula(formula, formula_state, {**model, l: 0, -l: 1}), literals=literals)


def progagate(formula, formula_state, model):
    # print("propagate call:")
    # print(model)

    if all(len(c) != 1 for c in formula):
        return formula, formula_state, model

    for i in range(len(formula)):
        if len(formula[i]) == 1:
            l = formula[i][0]
            formula, formula_state, model = update_formula(formula, formula_state, {**model, l: 1, -l: 0})
            return progagate(formula, formula_state, model)


def update_formula(formula, formula_state, model):
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


from walksat import WalksatSolver
s = WalksatSolver("simple_v3_c2.cnf")
There are 3 variables
There are 2 clauses
s.satisfiable()