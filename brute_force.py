from sat_solver import SatSolver


class BruteForceSolver(SatSolver):
    def satisfiable(self):
        print("Checking for satisfiability")
        for s in self.generate_strings():
            if self.solve(self.create_dic(s)):
                print("The formula is solved by the interpretation: ", s)
                return s
        print("The formula is not satisfiable")
        return False
