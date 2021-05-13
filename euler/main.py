from ortools.sat.python import cp_model


def SimpleSatProgram():
    """Minimal CP-SAT example to showcase calling the solver."""
    # Creates the model.
    model = cp_model.CpModel()

    # Creates the variables.
    num_vals = 3
    grid = []
    for i in range(16):
        grid.append(model.NewIntVar(0, 9, f'grid[{i}]'))

    # Creates the constraints.
    for i in range(0, 16, 4):
        model.Add(grid[i] + grid[i+1] + grid[i+2] + grid[i+3] == 12)

    for i in range(4):
        model.Add(grid[i] + grid[i+4] + grid[i+8] + grid[i+12] == 12)

    model.Add(grid[0] + grid[5] + grid[10] + grid[15] == 12)
    model.Add(grid[3] + grid[6] + grid[9] + grid[12] == 12)

    # Creates a solver and solves the model.
    solver = cp_model.CpSolver()
    solution_printer = VarArraySolutionPrinter(grid)
    status = solver.SearchForAllSolutions(model, solution_printer)

    # if status == cp_model.OPTIMAL:
    #     for i in range(16):
    #         print(f'g[{i}] = {solver.Value(grid[i])}')
    print(solution_printer.solution_count())


class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        #for v in self.__variables:
         #   print('%s=%i' % (v, self.Value(v)), end=' ')
        # print()

    def solution_count(self):
        return self.__solution_count


if __name__ == '__main__':
    all_p = []
    for a in range(10):
        for b in range(10):
            for c in range(10):
                for d in range(10):
                    if a + b + c + d == 12:

