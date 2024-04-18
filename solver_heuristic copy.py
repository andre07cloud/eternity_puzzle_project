from collections import defaultdict
import random
import eternity_puzzle

GRAY = 0 # 0 represent gray color in the border in the board

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

    print("******* Classify pieces: ")
    print("**************************************border_pieces**********************************************************")
    print(border_pieces)
    print("**************************************corner_pieces**********************************************************")
    print(corner_pieces)
    print("**************************************center_pieces**********************************************************")
    print(center_pieces)
    return border_pieces, corner_pieces, center_pieces

    

def place_corner_pieces(corner_pieces, board):
    # Logic to place corner pieces based on constraints.
    board_size = len(board)
    print("**************************************corner_pieces**********************************************************")
    print(corner_pieces)
    #Corner index in the board: top left, top right, bottom right, bottom left
    corners = [(0,0), (0, board_size-1), (board_size-1, 0), (board_size-1, board_size-1)]

    #Expected orientation of board sides for each corner: (top, left), (top, right), (bottom, right), (bottom, left)
    expected_gray_sides = [(0,2), (0,3), (1,2), (1,3)]

    for corner, gray_sides, in zip(corners, expected_gray_sides):
        print("############CORNER SIDE: ",corner)
        print("############GRAY SIDE: ",gray_sides)
        for piece in corner_pieces:
            print("*************PIECE: ",piece)
            for orientation in range(4):     # 0: original, 1: 90°, 2: 180°, 3: 270° rotation
                if check_gray_sides(piece, gray_sides, orientation):
                    # if corresponding piece , place it in the corner with correct orientation
                    board[corner[0]][corner[1]] = (piece, orientation)
                    print("**&&&**** PIECE: ", piece)
                    
                    print("&&&&&&&&&&&& PLACED PIECE &&&&&&&&")
                    corner_pieces.remove(piece) # remove the used piece from piece list
                    print("*****REMOVE :", corner_pieces)
                    break  #go the next corner
            if board[corner[0]][corner[1]] is not None:
                break  #if piece have been placed, go to the next corner
    print("**************************************BOARD for corner**********************************************************")
    print(board)
            
def check_gray_sides(piece, gray_sides, orientation):
    """
    Checks whether a piece matches the gray side expected for
    a specific corner, taking into account the piece orientation
    """
    #Map the piece orientation with side index
    sides = [piece[(i - orientation) % 4] for i in range(4)]

    # verify whether if expected sides as gray are exactly gray
    return all(sides[i] == GRAY for i in gray_sides)


def place_border_pieces(border_pieces, board):
    # Logic to place border pieces respecting adjacent color constraints.
    board_size = len(board)
    print("**************************************border_pieces**********************************************************")
    print(border_pieces)
    #Iterate on border without including corners
    for i in range(board_size):
        for j in [0, board_size-1]:
            if board[i][j] is None:
                place_border_piece_at(border_pieces, board, i, j)
    print("**************************************BOARD**********************************************************")
    print(board)

def place_border_piece_at(border_pieces, board, row, col):
    for piece in border_pieces:
        for orientation in range(4):   #Try all possible orientations
            if is_valid_border_placement(piece, orientation, row, col, board):
                #Place the piece if it corresponds and aligns correctly
                board[row][col] = (piece, orientation)
                border_pieces.remove(piece)  # Remove used piece form list
                return  # Stop after placing a piece
            
def is_valid_border_placement(piece, orientation, row, col, board):
    board_size = len(board)
    # Orientation of piece side : North, South, West, East
    oriented_piece = [piece[(i - orientation) %4] for i in range(4)]

    #verify color border conformity
    if row == 0 and oriented_piece[0] != GRAY:  #Board top
        return False
    if row == board_size-1 and oriented_piece[1] != GRAY:  #Board bottom
        return False
    if col == 0 and oriented_piece[2] != GRAY:  #Board left size
        return False
    if col == board_size-1 and oriented_piece[3] != GRAY:    #Board right size
        return False
    
    #Verify alignment of adjascent pieces
    #Top
    if row > 0 and board[row-1][col] is not None and board[row-1][col][0][1] != oriented_piece[0]:
        return False
    #Bottom
    if row < board_size-1 and board[row+1][col] is not None and board[row+1][col][0][1] != oriented_piece[1]:
        return False
    #Left
    if col > 0 and board[row][col-1] is not None and board[row][col-1][0][2] != oriented_piece[2]:
        return False
    #Right
    if col < board_size-1 and board[row][col+1]is not None and board[row][col+1][0][3] != oriented_piece[3]:
        return False
    
    return True


def fill_center(center_pieces, board):
  """
  Fills the center of the board with pieces, minimizing conflicts.

  Args:
    center_pieces: List of available piece types (e.g., [1, 2, 3, ...]).
    board: The game board (list of lists of tuples).

  Returns:
    The board with the center filled.
  """
  board_size = len(board)
  print("**************************************center_pieces**********************************************************")
  print(center_pieces)
  for row in range(1, board_size - 1):
        for col in range(1, board_size - 1):
            if board[row][col] is None:  # Si l'emplacement est vide
                for piece in center_pieces:
                    for orientation in range(4):  # Tester toutes les orientations
                        if is_valid_center_placement(piece, orientation, row, col, board):
                            board[row][col] = (piece, orientation)  # Placer la pièce
                            center_pieces.remove(piece)  # Enlever la pièce des pièces disponibles
                            break  # Sortir de la boucle d'orientation
                    if board[row][col] is not None:  # Si une pièce a été placée, sortir de la boucle de pièce
                        break
                else:
                    # Si aucune pièce ne peut être placée, cela indique un problème potentiel dans l'approche ou la configuration
                    print(f"Impossible de placer une pièce en {row}, {col}.")
                    return False
  print("**************************************BOARD**********************************************************")
  print(board)
  return True

def is_valid_center_placement(piece, orientation, row, col, board):
    # Appliquer l'orientation à la pièce pour obtenir les couleurs des côtés dans l'ordre correct
    oriented_piece = rotate_piece(piece, orientation)
   
    # Vérifier les côtés Nord et Sud
    if row > 0:  # Vérifier le côté Nord
        north_neighbor = board[row - 1][col]
        if north_neighbor and north_neighbor[1] != oriented_piece[0]:
            return False
    if row < len(board) - 1:  # Vérifier le côté Sud
        south_neighbor = board[row + 1][col]
        if south_neighbor and south_neighbor[0] != oriented_piece[1]:
            return False
   
    # Vérifier les côtés Est et Ouest
    if col > 0:  # Vérifier le côté Ouest
        west_neighbor = board[row][col - 1]
        if west_neighbor and west_neighbor[0][3] != oriented_piece[2]:
            #print("*********************###############****: ",west_neighbor)
            return False
    if col < len(board[0]) - 1:  # Vérifier le côté Est
        east_neighbor = board[row][col + 1]
        if east_neighbor and east_neighbor[0][2] != oriented_piece[3]:
            #print("##########################&&&&&: ",east_neighbor[0])
            return False

    # Si tous les tests sont passés, la pièce peut être placée
    return True

def rotate_piece(piece, orientation):
    """
    Applique une rotation à une pièce en fonction de l'orientation spécifiée.
    L'orientation indique le nombre de rotations de 90 degrés dans le sens des aiguilles d'une montre.
    """
    return piece[orientation:] + piece[:orientation]  


def convert_board_to_solution(board):
    # Convert the board layout into the solution format expected by the puzzle logic.
    solution = []
    for row in board:
        for cell in row:
            if cell is not None:
                piece, orientation = cell
                solution.append((piece, orientation))
            else:
                # Pour les emplacements vides, une convention spécifique peut être appliquée si nécessaire
                solution.append((None, None))
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
    place_corner_pieces(corner_pieces, board)
    #print("***********place_corner_pieces")
    #Place border pieces
    place_border_pieces(border_pieces, board)
    #print("***********place_border_piece")
    #Fill the center of the board
    fill_center(center_pieces, board)
    #print("***********fill_center")

    #Convert board layout to solution format and calculate number of conflicts
    solution = convert_board_to_solution(board)
    #print("******************************************************************")
    #print(solution)
    #print("****************################**********************************")
    #print(len(solution))
    n_conflict = eternity_puzzle.get_total_n_conflict(solution)

    return solution, n_conflict