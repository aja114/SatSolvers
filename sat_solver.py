import time as time


class SatSolver:
    def __init__(self, file):
        with open(file, 'r') as f:
            lines = f.readlines()

        self.form = [l.strip() for l in lines if l.strip()[0] != 'c']
        if self.form[0][:5] == 'p cnf':
            self.num_el = int(self.form[0].split()[2])
            self.num_clauses = int(self.form[0].split()[3])
            self.form.pop(0)
        else:
            raise Exception('Expressions description is missing')

        print("There are {} variables".format(self.num_el))
        print("There are {} clauses".format(self.num_clauses))
        self.create_clauses()

    def assert_formula(self):
        assert len(self.form) == self.num_clauses, "Formula is not conformed"
        for j in self.clauses:
            assert j[-1] == 0, "EOL missing"

    def create_clauses(self):
        self.clauses = [[int(y) for y in x.split(' ')] for x in self.form]

    def create_dic(self, string):
        input_dic = {}
        assert len(string) == self.num_el, "wrong input length"
        for i in range(1, self.num_el + 1):
            if string[i - 1] == 'x':
                input_dic[i] = 1
            else:
                input_dic[i] = int(string[i - 1])
        return input_dic

    def generate_strings(self):
        strings = []
        for i in range(2 ** self.num_el):
            strings.append(bin(i)[2:].zfill(self.num_el))
        return strings

    def satisfiable(self):
        pass

    def satisfiable_performance(self, **kwargs):
        start = time.time()
        res = self.satisfiable(**kwargs)
        end = time.time()
        print("The evaluation took {:.2f} ms".format(1000 * (end - start)))
        return res

    def solve(self, interp):
        res = all([any([interp[at] if at > 0 else not interp[-at] for at in c[:-1]]) for c in self.clauses])
        return res

    def check_result(self, interp):
        interp = self.create_dic(interp)
        print("\nResult check:")
        if self.solve(interp):
            print("Passed")
        else:
            print("Failed")
