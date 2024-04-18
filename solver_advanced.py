
import random
import math
from solver_heuristic import solve_heuristic
from solver_local_search import solve_local_search
from solver_heuristic import *
from solver_local_search import *
import solver_random
#import eternity_puzzle
#from eternity_puzzle import EternityPuzzle

def get_single_solution(eternity_puzzle, strategy):
    
    match strategy:
        case "heuristic":
            return solve_heuristic(eternity_puzzle)
        case "local_search":
            return solve_local_search(eternity_puzzle)
        case "random":
            return solver_random.solve_best_random(eternity_puzzle, 200)



def initial_solution(eternity_puzzle, num_solution=200):
    #solution_multiple = []
    seen_solutions = []
    solution_unique = []
    solution_multiple = []
    for i in range(num_solution):
        solver_choice = ["heuristic", "local_search", "random"]
        solver_selected = random.choice(solver_choice)
        solution, _ = get_single_solution(eternity_puzzle, solver_selected)
        solution_multiple.append(solution)
        if solution not in seen_solutions:
            seen_solutions.append(solution)
            ###print("*********** SOLVER *******************")
            ###print(solver_selected)
            solution_unique.append(solution)
    ##print("############## SOLUTION UNIQUE ********************")
    ##print(solution_unique)
    ###print("############## SOLUTION UNIQUE LENGHT ********************")
    ###print(len(solution_unique))
    return solution_multiple

#perform a fitness of an individual in a population. We put minus(-) to minimize number of conflicts
def fitness_function(eternity_puzzle, solution):
    

    fitness = eternity_puzzle.get_total_n_conflict(solution)
    #####print("*********** fitness_function(x) *************: ",-fitness)
    return -fitness
    

def tournament_selection(eternity_puzzle, population, parent_selected, parent_participated):
    
    preselected = random.sample(population, parent_participated)
    #print("######## preselected ################################################################# :")
    #print(preselected)
    pop = tri_fusion(eternity_puzzle, preselected)
    #selected = [preselected.sort(key=lambda x: fitness_function(eternity_puzzle, x), reverse=True)]
    selected = pop[:parent_selected]
    #print("******** selected ********** :", selected)
    #print(selected)
    return selected [:parent_selected]


def crossover(parent1, parent2): # Perform Exchange Region crossover  
	
    	
    board1 = format_solution_to_board(parent1)
    board2 = format_solution_to_board(parent2)
    print("********* BOARD 1 ******* ",board1)
    board_size = len(board1)
    print("********* BOARD SIZE ******* ",board_size)
    # Sélection aléatoire d'une région
    region_start = random.randint(0, board_size - 2)
    region_end = random.randint(region_start + 2, board_size)

    #print("region strat",region_start)
    #print("region end",region_end)
    
    # Clonage de board1 pour former offspring
    offspring = board1[:]

    # Suppression des tuiles de offspring qui sont à l'intérieur de la région de board2
    for i in range(region_start, region_end):
        for j in range(len(board2[i])):
            if board2[i][j] in offspring[i]:
                offspring[i].remove(board2[i][j])
    
    # Ajout des tuiles restantes de board2 à une liste
    remaining_tiles = []
    for i in range(region_start, region_end):
        for tile in board2[i]:
            if tile not in offspring[i]:
                remaining_tiles.append(tile)
    
    # Copie des cellules à l'intérieur de la région de board2 à offspring
    for i in range(region_start, region_end):
        offspring[i] = board2[i][:]

    # Remplissage aléatoire des cellules vides de offspring avec les tuiles restantes
    for i in range(region_start, region_end):
        empty_cells = [j for j in range(len(board1[i])) if board1[i][j] is None]
        random.shuffle(empty_cells)
        for j, tile in zip(empty_cells, remaining_tiles):
            offspring[i][j] = tile
    
    offspring1 = convert_board_to_solution(offspring)

    return offspring1

    
def format_solution_to_board(solution):
    
    board_size = int(math.sqrt(len(solution)))
    board = [[None] * board_size for _ in range(board_size)]
    k = 0
    for i in range(board_size):
        for j in range(board_size):
            board[i][j] = solution[k]
            k +=1
    ####print("#################################### format_solution_to_board: ")
    ####print(board)
    return board

def find_index(piece, board):
    for i, row in enumerate(board):
        for j , val in enumerate(row):
            if val == piece:
                j = row.index(piece)
            ####print("&&&&&&& ********** ####### j :", j)
            ####print("&&&&&&&&&&&& (i, j)", (i, j))
            return (i, j)

    return None
            

#perform piece fitness counting matching adjacent sides
def fit_individual(solution, piece):
    board = format_solution_to_board(solution)
    ####print("&&&&&&&&&&&&&& BOARD **********************: ")
    ####print("POSITION **********************: ",board)
    position = find_index(piece, board)
    ####print("POSITION **********************: ",position)
    count = 0
    i , j = position[0], position[1]
    if piece[0] == board[i-1][j][1]:
        count +=1
    if piece[3] == board[i][j+1][2]:
        count +=1
    if piece[1] == board[i+1][j][0]:
        count +=1
    if piece[2] == board[i][j-1][3]:
        count +=1

    return count
#perform a rotation of a piece according to orientation fitness of a piece
def rotation_piece(eternity_puzzle, solution, piece):
    orientations = eternity_puzzle.generate_rotation(piece)
    #best = 0
    #i = 0
    #k = 0
    #for orientation in orientations:
        #fit_piece = fit_individual(solution, orientation)
        #if fit_piece > best:
            #best = fit_piece
            #k = i
        #i += 1

    return orientations[1]

def rotate_matrix(matrix):
    n = len(matrix)
    rotated_matrix = [[0]*n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            new_i = j
            new_j = n - 1 - i
            rotated_matrix[new_i][new_j] = matrix[i][j]

    return rotated_matrix

def convert_board_to_solution(board):
    board_size = len(board)
    solution = []
    for i in range(board_size):
        for j in range(board_size):
            solution.append(board[i][j])
    
    return solution

def select_random_submatrix(matrix, submatrix_size):
    """
    Sélectionne aléatoirement une sous-matrice carrée dans une matrice carrée.

    Args:
    - matrix : La matrice carrée à partir de laquelle sélectionner la sous-matrice.
    - submatrix_size : La taille de la sous-matrice carrée à sélectionner.

    Returns:
    - submatrix : La sous-matrice carrée sélectionnée.
    """
    matrix_size = len(matrix)
    if matrix_size < submatrix_size:
        raise ValueError("La taille de la matrice est inférieure à la taille de la sous-matrice.")

    # Choisir aléatoirement les coordonnées du coin supérieur gauche de la sous-matrice
    start_row = random.randint(0, matrix_size - submatrix_size)
    start_col = random.randint(0, matrix_size - submatrix_size)

    # Extraire la sous-matrice
    submatrix = [row[start_col:start_col+submatrix_size] for row in matrix[start_row:start_row+submatrix_size]]

    return submatrix, start_row, start_col, submatrix_size

#perform region rotation of a region randomly selected from individual 
def rotation_region(eternity_puzzle, solution, mutation_rate):

    #if random.random() < mutation_rate:
        #return solution
    #print(solution)

    board = format_solution_to_board(solution)
    print("********* BOARD: ************************************************************************")
    
    print(board)
    print("********* BOARD: *************************************************************************", len(board))
    board_size = len(board)
    #index = random.randint(0, board_size-2)
    #index = 1
    #region_start = random.randint(0, board_size - 2)
    region_size = random.randint(2, board_size-1)
    # Sélection aléatoire des coordonnées de la première région
    region_start = (random.randint(0, board_size - 2), random.randint(0, board_size - 2))
    region_start = (0, region_size)
    region_end = (region_start[0] + region_size, region_start[1] + region_size)
    #region_end = random.randint(region_start + 2, board_size)
    #region_start = 1
    #region_end = 2
    #####print("board_size #########", board_size )
    #width_region = random.randint(1,board_size-1)
    #####print("######## width_region:  ", width_region)
    #test = False
    #while index+width_region > board_size-1:
        
        #if index+width_region <= board_size-1:
            #####print("random ******************************************************88", index+width_region)
            #test = True
        #else:
            
        #width_region = random.randint(1,board_size-1)
        #####print("random+++++....", width_region)
        #####print("random+++++.... index", index+width_region, board_size-1)

    #m = index+width_region
    print("REGION SIZE: ", region_size)
    row = 0
    matrix, start_row, start_col, submatrix_size = select_random_submatrix(board, region_size)
    print("********* board[k][index : m] MATRIX **************************************************: ", start_row, start_col, submatrix_size)
    print("********* MATRIX BEFORE **************************************************: ")
    print(matrix)
    rotated_matrix = rotate_matrix(matrix)
    print("********* MATRIX ROTATED **************************************************: ")
    print(rotated_matrix)
    row = 0
    n = m = submatrix_size
    if start_row != 0:
        n = submatrix_size+1
    if start_col != 0:
        m = submatrix_size+1
    for i in range(start_row, n):
        col = 0
        for j in range(start_col, m):
            print("&&&&& j: ", j)
            board[i][j] = rotation_piece(eternity_puzzle, solution, rotated_matrix[row][col])
            col +=1
        row +=1

    

    print("********* BOARD AFTER ROTATION **************************************************: ")
    print(board)

    solution = convert_board_to_solution(board)
    return solution

#get intern index from a solution
def indexes_intern(solution):
    board_size = int(math.sqrt(len(solution)))
    board = format_solution_to_board(solution)
    indexes = []
    for i in range(board_size):
        for j in range(board_size):
            if i>0 and i<board_size-1 and j>0 and j<board_size-1:
                indexes.append((i,j))
    
    return indexes


def swap_intern(solution):
    #_, _, intern_pieces = classify_pieces()
    index_intern = index_center(solution)
    solution_copy = solution.copy()
    if len(index_intern) >=2:
        index1, index2  = random.sample(index_intern, 2)
        solution_copy[index1], solution_copy[index2] = solution_copy[index2], solution_copy[index1]


def swap_pieces(population):

    swap_side = ["corner", "border", "intern"]
    swap_stategy = random.choice(swap_side)
    if swap_stategy == "corner":
        return swap_corner(population)
    if swap_stategy == "border":
        return swap_border(population)
    if swap_stategy == "intern":
        return swap_intern(population)
    selected_piece = random.sample(population, 2)
    copy_poluation = population.copy()
    fit1_before = fit_individual(selected_piece[0])
    fit2_before = fit_individual(selected_piece[1])

    return


def swap_region(individual):
    board = format_solution_to_board(individual)
    board_size = len(board)
    region_size = random.randint(1, board_size-1)
    # Sélection aléatoire des coordonnées de la première région
    region1_start = (random.randint(0, board_size - region_size), random.randint(0, board_size - region_size))
    region1_end = (region1_start[0] + region_size, region1_start[1] + region_size)
    
    # Sélection aléatoire des coordonnées de la deuxième région qui ne se superpose pas avec la première
    region2_start = (random.randint(0, board_size - region_size), random.randint(0, board_size - region_size))
    while overlaps(region1_start, region1_end, region2_start, region2_start[0] + region_size, region2_start[1] + region_size):
        region2_start = (random.randint(0, board_size - region_size), random.randint(0, board_size - region_size))
    region2_end = (region2_start[0] + region_size, region2_start[1] + region_size)
    
    # Échange des régions dans la solution
    for i in range(region_size):
        for j in range(region_size):
            board[region1_start[0] + i][region1_start[1] + j], board[region2_start[0] + i][region2_start[1] + j] = board[region2_start[0] + i][region2_start[1] + j], board[region1_start[0] + i][region1_start[1] + j]
    solution = convert_board_to_solution(board)
    return solution

def overlaps(start1, end1, start2, end2_x, end2_y):
    # Vérifie si les deux régions se chevauchent
    return not (end1[0] <= start2[0] or start1[0] >= end2_x or end1[1] <= start2[1] or start1[1] >= end2_y)


#mutation type randomly chosen from "rotation region" or "swap region"
def mutation(eternity_puzzle, individual, mutation_rate):
    def custom_mutation(eternity_puzzle):
        strategy = ["rotation", "swap"]
        strategy_selected = random.choice(strategy)
        strategy_selected = "swap"
        if strategy_selected == "rotation":
            return rotation_region(eternity_puzzle, individual, mutation_rate)
        if strategy_selected == "swap":
            return swap_region(individual)
    return custom_mutation(eternity_puzzle)

def tri_fusion(eternity_puzzle, tableau):
  """
  Trie un tableau en utilisant le tri fusion.

  Args:
    tableau: Le tableau à trier.

  Returns:
    Le tableau trié.
  """

  if len(tableau) <= 1:
    return tableau

  milieu = len(tableau) // 2
  gauche = tri_fusion(eternity_puzzle, tableau[:milieu])
  droite = tri_fusion(eternity_puzzle, tableau[milieu:])

  return fusionner(eternity_puzzle, gauche, droite)

def fusionner(eternity_puzzle, gauche, droite):
  """
  Fusionne deux tableaux triés en un seul tableau trié.

  Args:
    gauche: Le premier tableau trié.
    droite: Le deuxième tableau trié.

  Returns:
    Le tableau fusionné trié.
  """

  tableau_fusionne = []
  i = 0
  j = 0

  while i < len(gauche) and j < len(droite):
    fitness1 = fitness_function(eternity_puzzle, gauche[i])
    fitness2 = fitness_function(eternity_puzzle, droite[j])
    if fitness1  >= fitness2:
      tableau_fusionne.append(gauche[i])
      i += 1
    else:
      tableau_fusionne.append(droite[j])
      j += 1

  tableau_fusionne.extend(gauche[i:])
  tableau_fusionne.extend(droite[j:])

  return tableau_fusionne


#off-spring generation
def create_new_generation(eternity_puzzle, population, elite_size, mutation_rate, crossover_rate):
    new_generation = []
    population = tri_fusion(eternity_puzzle, population)
    #####print("***** POPULATION *******************:")
    #####print(population)
    #population.sort(key=compare_fitness, reverse=True)
    #population.sort(key=lambda x: fitness_function(eternity_puzzle, x), reverse =True)
    population = tri_fusion(eternity_puzzle, population)
    #####print("***** POPULATION SORTED *******************: ")
    #####print("***** POPULATION SORTED *******************: ", population)
    elites = population[:elite_size]
    new_generation.extend(elites)
    parent_selected = 2 
    #parent_participated = random.randint(int(len(population)/2), len(population))
    parent_participated = 5
    while len(new_generation) < len(population):
        parent1 = tournament_selection(eternity_puzzle, population, parent_selected, parent_participated)[0]
        parent2 = tournament_selection(eternity_puzzle, population, parent_selected, parent_participated)[1]
        #if random.random() < crossover_rate:
        child = crossover(parent1, parent2)
        ##print("****************************************** PARENT 1: ********************************")
        ##print(parent1)
        #print("*********** Child *************************************************", )
        #print("***** CHILD : ", child)
        ##print("****************************************** PARENT 2: ********************************")
        ##print(parent2)
        #####print("*********** Child2 *************************************************", )
        #####print("***** CHILD 2: ", child2)
        mutation_prob = random.random()
        if mutation_prob < mutation_rate:
            #print("********************************************** MUTATION RATE ********************************************************************************")
            #print(mutation_prob)
            #print("********************************************** MUTATION RATE ********************************************************************************")
            child = mutation(eternity_puzzle, child, mutation_rate)
        
        new_generation.extend([child])
    
    return new_generation



#Genetic Algorithm definition
def genetic_algorithm(eternity_puzzle, pop_size, elite_size, mutation_rate, num_gen, crossover_rate):
    current_generation = initial_solution(eternity_puzzle, pop_size)
    #####print("############# current genetion ###############################################################################:")
    #####print(current_generation)
    for gen in range(num_gen):
        current_generation = create_new_generation(eternity_puzzle, current_generation, elite_size, mutation_rate, crossover_rate)
        best_individual = max(current_generation, key=lambda x: fitness_function(eternity_puzzle, x))
        print(f"Generation {gen+1}: Best Fitness = {fitness_function(eternity_puzzle, best_individual)} Best Individual = {best_individual}")

    return best_individual, fitness_function(eternity_puzzle, best_individual)

def solve_advanced(eternity_puzzle):
    """
    Your solver for the problem
    :param eternity_puzzle: object describing the input
    :return: a tuple (solution, cost) where solution is a list of the pieces (rotations applied) and
        cost is the cost of the solution
    """
    
    pop_size = 200
    elite_size=0
    mutation_rate=0.1
    crossover_rate = 0.99
    num_gen=100

    best_solution, n_conflict = genetic_algorithm(eternity_puzzle, pop_size, elite_size, mutation_rate, num_gen, crossover_rate)

    return best_solution, -n_conflict
