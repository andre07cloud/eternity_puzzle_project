import eternity_puzzle
import random
from solver_heuristic import solve_heuristic
from solver_local_search import solve_local_search
from solver_random import solve_random
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.operators.selection.tournament import TournamentSelection
from pymoo.operators.selection.rnd import RandomSelection
from pymoo.optimize import minimize
from eternity_puzzle import EternityPuzzle

class EternityProblem(EternityPuzzle):
    def __init__(self, instance_file):
        super().__init__(instance_file)

    def _evaluate(self, x, out, *args, **kwargs):
        # Évaluation de la solution ici. x représente une solution potentielle.
        fitness = self.calculate_fitness(x)
        out["F"] = -fitness # PyMOO minimise par défaut, donc nous utilisons -fitness

    def calculate_fitness(self, x):
        # Calcul de la fitness de la solution x
        return self.get_total_n_conflict(x)


def get_single_solution(eternity_puzzle, strategy):
    
    match strategy:
        case "random":
            return solve_random(eternity_puzzle)
        case "heuristic":
            return solve_heuristic(eternity_puzzle)
        case "local_search":
            return solve_local_search(eternity_puzzle)




def initial_solution(eternity_puzzle, num_solution=40):
    #solution_multiple = []
    seen_solutions = []
    solution_unique = []
    for i in range(num_solution):
        solver_choice = ["random", "heuristic", "local_search"]
        solver_selected = random.choice(solver_choice)
        solution, _ = get_single_solution(eternity_puzzle, solver_selected)
        #solution_multiple.append(solution)
        if solution not in seen_solutions:
            seen_solutions.append(solution)
            solution_unique.append(solution)
    
    return solution_unique

    




def solve_advanced(eternity_puzzle):
    """
    Your solver for the problem
    :param eternity_puzzle: object describing the input
    :return: a tuple (solution, cost) where solution is a list of the pieces (rotations applied) and
        cost is the cost of the solution
    """
    
    pop_size = 200
    num_gen = 100
    problem = EternityProblem
    print("********PROBLEM: ", problem)

    # Définir le nombre de tournois et de concurrents par tournoi
    n_tournaments = 2
    n_competitors = 2

    # Créer l'opérateur de sélection par tournoi
    #tournament_selection = TournamentSelection(n_tournaments=n_tournaments, n_competitors=n_competitors, tie_breaker = "best")
    selection = RandomSelection()

    initial = initial_solution(eternity_puzzle)
    method = GA(pop_size=pop_size,
                n_offsprings=int(pop_size/2),
                sampling=initial,
                eliminate_duplicates=True,
                selection = selection
                )
        
    res = minimize(problem,
                method,
                termination=('n_gen', num_gen),
                verbose=True,
                eliminate_duplicates=False,
                save_history=True
                )
        
    print("Best solution found: %s" % res.X)
    print("Function value: %s" % res.F)
    print("Execution data:", res.problem.execution_data)


