from collections import defaultdict
import random
import eternity_puzzle
import math

GRAY = 0 # 0 represent gray color in the border in the board

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


def classify_pieces(piece_list):
    # This function should classify pieces into border, corner, and center pieces
    # based on their colors and constraints. This is a placeholder for the logic.

    corner_pieces = []
    border_pieces = []
    center_pieces = []

    for piece in piece_list:
        #Count color gray of border
        gray_sides = piece.count(GRAY)

        if gray_sides == 2:
            #if there exactly 2 gray sides, it's a corner piece
            corner_pieces.append(piece)
        elif gray_sides == 1:
            #if there exactly 1 gray sides, it's a border piece
            border_pieces.append(piece)
        else:
            #else there is not gray side it's a center piece
            center_pieces.append(piece)

    ##print("******* Classify pieces: ")
    ##print("**************************************border_pieces**********************************************************")
    ##print(border_pieces)
    ##print("**************************************corner_pieces**********************************************************")
    ##print(corner_pieces)
    ##print("**************************************center_pieces**********************************************************")
    ##print(center_pieces)
    return border_pieces, corner_pieces, center_pieces


def place_corner_pieces(eternity_puzzle, corner_pieces, board):
    # Logic to place corner pieces based on constraints.
    board_size = len(board)
    ##print("**************************************corner_pieces**********************************************************")
    ##print(corner_pieces)
    #Corner index in the board: top left, top right, bottom right, bottom left
    corners = [(0,0), (0, board_size-1), (board_size-1, board_size-1), (board_size-1, 0)]

    #Expected orientation of board sides for each corner: (top, left), (top, right), (bottom, right), (bottom, left)
    expected_gray_sides = [(0,2), (0,3), (1,3), (1,2)]
    
    for corner, gray_sides, in zip(corners, expected_gray_sides):
        ##print("############CORNER SIDE: ",corner)
        ##print("############GRAY SIDE: ",gray_sides)
        for piece in corner_pieces:
            rotation = eternity_puzzle.generate_rotation(piece)
            ##print("**********ROTATIONS***************")
            ##print(rotation)
            ##print("*************PIECE: ",piece)
            for orientation in rotation:     # 0: original, 1: 90°, 2: 180°, 3: 270° rotation
                if all(orientation[i] == GRAY for i in gray_sides):
                    # if corresponding piece , place it in the corner with correct orientation
                    board[corner[0]][corner[1]] = orientation
                    ##print("**&&&**** PIECE: ", orientation)
                    
                    ##print("&&&&&&&&&&&& PLACED PIECE &&&&&&&&")
                    corner_pieces.remove(piece) # remove the used piece from piece list
                    ##print("*****REMOVE :", corner_pieces)
                    break  #go the next corner
            if board[corner[0]][corner[1]] is not None:
                break  #if piece have been placed, go to the next corner
    ##print("**************************************BOARD for corner**********************************************************")
    ##print(board)
            
def check_gray_sides(piece, gray_sides, orientation):
    """
    Checks whether a piece matches the gray side expected for
    a specific corner, taking into account the piece orientation
    """
    #Map the piece orientation with side index
    sides = [piece[(i - orientation) % 4] for i in range(4)]

    # verify whether if expected sides as gray are exactly gray
    return all(sides[i] == GRAY for i in gray_sides)


def place_border_pieces(eternity_puzzle, border_pieces, board):
    # Logic to place border pieces respecting adjacent color constraints.
    board_size = len(board)
    ##print("**************************************border_pieces**********************************************************")
    ##print(border_pieces)
    #Iterate on border without including corners
    for i in range(board_size):
        for j in [0, board_size-1]:
            if board[i][j] is None:
                ##print("&&&&&&&&&&&&&&&& NONE NONE: ",board, i, j)
                place_border_piece_at(eternity_puzzle, border_pieces, board, i, j)
    ##print("**************************************BOARD for border**********************************************************")
    ##print(board)
    for i in [0, board_size-1]:
        for j in range(board_size):
            if board[i][j] is None:
                ##print("&&&&&&&&&&&&&&&& NONE NONE: ",board, i, j)
                place_border_piece_at(eternity_puzzle, border_pieces, board, i, j)
def place_border_piece_at(eternity_puzzle, border_pieces, board, row, col):

    for piece in border_pieces:
        rotation = eternity_puzzle.generate_rotation(piece)
        ##print("ROTATION********: ",rotation)
        for orientation in rotation:   #Try all possible orientations
            if is_valid_border_placement(piece, orientation, row, col, board):
                #Place the piece if it corresponds and aligns correctly
                ##print("ORIENTATION BORDER********: ",orientation)
                board[row][col] = orientation
                border_pieces.remove(piece)  # Remove used piece form list
                return  # Stop after placing a piece
            
def is_valid_border_placement(piece, orientation, row, col, board):
    board_size = len(board)
    # Orientation of piece side : North, South, West, East
    #oriented_piece = [piece[(i - orientation) %4] for i in range(4)]

    #verify color border conformity
    if row == 0 and orientation[0] != GRAY:  #Board top
        return False
    if row == board_size-1 and orientation[1] != GRAY:  #Board bottom
        return False
    if col == 0 and orientation[2] != GRAY:  #Board left size
        return False
    if col == board_size-1 and orientation[3] != GRAY:    #Board right size
        return False
    
    #Verify alignment of adjascent pieces
    #Left side
    ##print("board[row-1][col][0][1]********************: ", board[row-1][col])
    if col == 0 and orientation[2] == GRAY:
        return True
    #Right side
    if col == board_size-1 and orientation[3] == GRAY:
        return True
    #Top side
    if row == 0 and orientation[0] == GRAY:
        return True
    #Bottom side
    if row == board_size-1 and orientation[1] == GRAY:
        return True


def fill_center(eternity_puzzle, center_pieces, board):
  """
  Fills the center of the board with pieces, minimizing conflicts.

  Args:
    center_pieces: List of available piece types (e.g., [1, 2, 3, ...]).
    board: The game board (list of lists of tuples).

  Returns:
    The board with the center filled.
  """
  board_size = len(board)
  solution1 = convert_board_to_solution(board)
  solution =solution1[::-1]
  #print("**************************************center_pieces**********************************************************")
  #print(solution)
  for row in range(1, board_size - 1):
        for col in range(1, board_size - 1):
            if board[row][col] is None:  # Si l'emplacement est vide
                for piece in center_pieces:
                    rotation = eternity_puzzle.generate_rotation(piece)
                    for orientation in rotation:  # Tester toutes les orientations
                        if is_valid_center_placement(piece, orientation, row, col, board):
                            orientation = rotation_piece(eternity_puzzle, solution, piece)
                            board[row][col] = orientation  # Placer la pièce
                            center_pieces.remove(piece)  # Enlever la pièce des pièces disponibles
                            break  # Sortir de la boucle d'orientation
                    if board[row][col] is not None:  # Si une pièce a été placée, sortir de la boucle de pièce
                        break
            else:
                # Si aucune pièce ne peut être placée, cela indique un problème potentiel dans l'approche ou la configuration
                #print(f"Impossible de placer une pièce en {row}, {col}.")
                return False
  ##print("**************************************BOARD**********************************************************")
  ##print(board)
  return True

def is_valid_center_placement(piece, orientation, row, col, board):
    # Appliquer l'orientation à la pièce pour obtenir les couleurs des côtés dans l'ordre correct
    #oriented_piece = rotate_piece(piece, orientation)
   
    # Vérifier les côtés Nord et Sud
    if row > 0:  # Vérifier le côté Nord
        north_neighbor = board[row - 1][col]
        if north_neighbor and north_neighbor[1] == orientation[0]:
            return True
    if row < len(board) - 1:  # Vérifier le côté Sud
        south_neighbor = board[row + 1][col]
        if south_neighbor and south_neighbor[0] == orientation[1]:
            return False
   
    # Vérifier les côtés Est et Ouest
    if col > 0:  # Vérifier le côté Ouest
        west_neighbor = board[row][col - 1]
        if west_neighbor and west_neighbor[3] != orientation[2]:
            ##print("*********************###############****: ",west_neighbor)
            return True
    if col < len(board[0]) - 1:  # Vérifier le côté Est
        east_neighbor = board[row][col + 1]
        if east_neighbor and east_neighbor[2] == orientation[3]:
            ##print("##########################&&&&&: ",east_neighbor[0])
            return False

    # Si tous les tests sont passés, la pièce peut être placée
    return True


def convert_board_to_solution(board):
    # Convert the board layout into the solution format expected by the puzzle logic.
    solution = []
    board_size = len(board)
    board_reverse = board[::-1]
    ##print("REVERSE *************** : ",board_reverse)
    for row in board_reverse:
        for piece in row:
            if piece is not None:
                solution.append(piece)
            else:
                # Pour les emplacements vides, une convention spécifique peut être appliquée si nécessaire
                solution.append(None)
    return solution




def solve_heuristic(eternity_puzzle):
    """
    Heuristic solution of the problem
    :param eternity_puzzle: object describing the input
    :return: a tuple (solution, cost) where solution is a list of the pieces (rotations applied) and
        cost is the cost of the solution
    """


    board = [[None for _ in range(eternity_puzzle.board_size)] for _ in range(eternity_puzzle.board_size)]
    piece_list = eternity_puzzle.piece_list
    border_pieces, corner_pieces, center_pieces = classify_pieces(piece_list)

    #Place corner pieces
    place_corner_pieces(eternity_puzzle, corner_pieces, board)
    ##print("***********place_corner_pieces")
    #Place border pieces
    place_border_pieces(eternity_puzzle, border_pieces, board)
    ##print("***********place_border_piece")
    #Fill the center of the board
    fill_center(eternity_puzzle, center_pieces, board)
    ##print("***********fill_center")

    #Convert board layout to solution format and calculate number of conflicts
    solution = convert_board_to_solution(board)
    #solution = board
    ##print("*****************************SOLUTIONNNNNNNNNNNNNNNNNNNNNNN*************************************")
    ##print(solution)
    ##print("****************################**********************************")
    ##print(len(solution))
    n_conflict = eternity_puzzle.get_total_n_conflict(solution)

    return solution, n_conflict