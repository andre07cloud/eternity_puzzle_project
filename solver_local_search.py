import math
#import eternity_puzzle
from solver_heuristic import solve_heuristic
import random
import numpy as np

def index_center(solution):

    board_size = int(math.sqrt(len(solution)))
    ##print("************* board_size: ",board_size)
    indexes = []
    index = 0
    for i in range(board_size):
        for j in range(board_size):
            
            if i>0 and i<board_size-1 and j>0 and j<board_size-1:
                indexes.append(index)
            index +=1
    ##print("#############*****########## : indexes", indexes)
    return indexes



def find_index(piece, board):
    for i, row in enumerate(board):
        for j , val in enumerate(row):
            if val == piece:
                j = row.index(piece)
            ##print("&&&&&&& ********** ####### j :", j)
            ##print("&&&&&&&&&&&& (i, j)", (i, j))
            return (i, j)

    return None

#perform piece fitness counting matching adjacent sides
def fit_individual(solution, piece):
    board = format_solution_to_board(solution)
    ##print("&&&&&&&&&&&&&& BOARD **********************: ")
    ##print("POSITION **********************: ",board)
    position = find_index(piece, board)
    ##print("POSITION **********************: ",position)
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
    best = 0
    i = 0
    k = 0
    for orientation in orientations:
        fit_piece = fit_individual(solution, orientation)
        if fit_piece > best:
            best = fit_piece
            k = i
        i += 1

    return orientations[k]

def format_solution_to_board(solution):
    
    board_size = int(math.sqrt(len(solution)))
    board = [[None] * board_size for _ in range(board_size)]
    k = 0
    for i in range(board_size):
        for j in range(board_size):
            board[i][j] = solution[k]
            k +=1
    ##print("#################################### format_solution_to_board: ")
    ##print(board)
    return board



def generate_neighbor(eternity_puzzle, solution):
    """Génère une solution voisine par rotation d'une tuile ou échange de deux tuiles."""
    new_solution = solution.copy()
    method = random.choice(["rotate", "swap"])
    indexes = index_center(solution)
    if len(indexes) <=1:
        method = "rotate"
    
    if method == "rotate":
       # #print("********#########$$$$$$$$$ :", method)
        # Sélection aléatoire d'une tuile à tourner
        #piece_index = random.choice(range(len(solution)))
        piece_index = random.choice(indexes)
        piece = new_solution[piece_index]
        # Rotation de la tuile (0: aucune, 1: 90°, 2: 180°, 3: 270°)
        permutation_idx = np.random.choice(np.arange(4))
        piece_permuted = rotation_piece(eternity_puzzle, solution, piece)
        new_solution[piece_index] = piece_permuted
    elif method == "swap":
        ##print("********#########$$$$$$$$$ :", method)
        # Sélection aléatoire de deux tuiles à échanger
        index1, index2 = random.sample(indexes , 2)
        new_solution[index1], new_solution[index2] = new_solution[index2], new_solution[index1]

    return new_solution


def evaluate_solution(eternity_puzzle, solution):
    score = eternity_puzzle.get_total_n_conflict(solution)
   # #print("%%%%%%%%%%%%%%%%%%%%: SCORE: ",score)
    return score


def simulated_annealing(solve_heuristic, eternity_puzzle, initial_temp, cooling_rate, min_temp):
    current_solution, current_score = solve_heuristic(eternity_puzzle)
    #current_score = evaluate_solution(current_solution)
    temperature = initial_temp
    
    while temperature > min_temp:
        new_solution = generate_neighbor(eternity_puzzle, current_solution)
        new_score = evaluate_solution(eternity_puzzle, new_solution)
        delta_score = current_score - new_score
    
        if delta_score > 0 or random.random() < math.exp(delta_score / temperature):
            current_solution, current_score = new_solution, new_score
            
        temperature *= cooling_rate
        
    return current_solution, current_score




def solve_local_search(eternity_puzzle):
    """
    Local search solution of the problem
    :param eternity_puzzle: object describing the input
    :return: a tuple (solution, cost) where solution is a list of the pieces (rotations applied) and
        cost is the cost of the solution
    """
    initial_temp = 10000
    cooling_rate = 0.99
    min_temp = 1

    solution, n_conflict = simulated_annealing(solve_heuristic, eternity_puzzle, initial_temp, cooling_rate, min_temp)

    return solution, n_conflict
