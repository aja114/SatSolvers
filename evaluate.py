#!/Users/utilisateur/Library/PythonEnv/ippenv/bin/python

import os
import getopt
import sys

from brute_force import BruteForceSolver
from dpll import DpllSolver
from walksat import WalksatSolver
from baseline import BaselineSolvers

solvers = {
    '0': 'brute force',
    '1': 'dpll',
    '2': 'walksat',
    '3': 'baseline'
}


def solve(solver, file):
    if solver == 'brute force':
        s = BruteForceSolver(file)

    elif solver == 'baseline':
        s = BaselineSolvers(file)

    elif solver == 'dpll':
        s = DpllSolver(file)

    elif solver == 'walksat':
        s = WalksatSolver(file)

    res = s.satisfiable_performance()
    if res:
        s.check_result(res)


def usage():
    signature = f'{os.path.basename(__file__)} -s <solver> -f <file>'
    print('\nThe program needs to be called in this way:')
    print(signature)
    print(f'\t-s or --solver')
    print(f'\t\tFollowing options:\n\t\t' + '\n\t\t'.join(['0: brute force', '1: dpll', '2: walksat', '3: baseline']))
    print(f'\t-f or --file')
    print(f'\t\tThe file has to be in the dimacs format')


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hs:f:", ["help", "solver=", "file="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    flags = [x[0] for x in opts]

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt in ("-s", "--solver"):
            solver = arg
            if solver not in solvers:
                print('Solver not found')
                usage()
                sys.exit(2)
            else:
                print(f'Solver: {solvers[solver]}')
        elif opt in ("-f", "--file"):
            file = arg
            print(f'File: {file}')

    if '-f' not in flags and '--file' not in flags:
        print("Missing file option")
        usage()
        sys.exit(2)
    if '-s' not in flags and '--solver' not in flags:
        print("Missing solver option")
        usage()
        sys.exit(2)

    solve(solvers[solver], file)


if __name__ == "__main__":
    main(sys.argv[1:])
