from sat_solver import SatSolver

# from sympy.logic.boolalg import And, Or, Implies, Equivalent, Not, to_cnf
# from sympy.abc import p, q, r
from sympy.logic.inference import satisfiable
from sympy.logic.utilities.dimacs import load_file


class BaselineSolvers(SatSolver):
    def __init__(self, file):
        self.form = load_file(file)
        self.num_el = len(self.form.atoms())
        self.num_clauses = len(self.form.args)
        print("There are {} variables".format(self.num_el))
        print("There are {} clauses".format(self.num_clauses))

    def satisfiable(self, solver='dpll'):
        if solver == 'dpll':
            sat = satisfiable(self.form, algorithm='dpll')
        elif solver == 'cdcl':
            sat = satisfiable(self.form, algorithm='dpll2')

        res = ''
        for i in sorted(list(sat.items()), key=lambda x: int(str(x[0])[4:])):
            res += str(1 * i[1])
        print("The formula is solved by the interpretation: ", res)

        return res

    def solve(self, interp):
        return True

