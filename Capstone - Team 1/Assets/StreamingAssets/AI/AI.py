#Hi, I'm OX, the AI for Quixo

from Settings import *
import copy, random

#Reused Function, will break out into a module later
def init_safe_pickup_spots():
    edges_of_The_board = []
    for i in range(5):
        edges_of_The_board.append("(0,"+str(i)+")")
    for i in range(5):
        edges_of_The_board.append("("+str(i)+",0)")
    for i in range(5):
        edges_of_The_board.append("(4,"+str(i)+")")
    for i in range(5):
        edges_of_The_board.append("("+str(i)+",4)")
    return edges_of_The_board

#CONST VARS
EDGES_OF_THE_BOARD = init_safe_pickup_spots()

#Refactor function
def apply_move(board, move_block_from, move_block_to, player_turn):
    if (move_block_to[1] != move_block_from[1]):
        #Were moving rows
        old_row = int(move_block_from[1])
        new_row = int(move_block_to[1])
        Col = int(move_block_from[3])

        blocks_to_shift = new_row - old_row
        if (blocks_to_shift > 0):
            for i in range(0, abs(blocks_to_shift)):            
               board[old_row + i][Col] = board[old_row + i + 1][Col]
        else:
            for i in range(0, abs(blocks_to_shift)):            
                board[old_row - i][Col] = board[old_row - i -+ 1][Col]
    else:
        #Were moving cols
        old_col = int(move_block_from[3])
        new_col = int(move_block_to[3])
        Row = int(move_block_from[1])

        blocks_to_shift = new_col - old_col
        if (blocks_to_shift > 0):
            for i in range(0, abs(blocks_to_shift)):            
                board[Row][old_col + i] = board[Row][old_col + i + 1]
        else:
            for i in range(0, abs(blocks_to_shift)):            
                board[Row][old_col - i] = board[Row][old_col - i -+ 1]

    board[int(move_block_to[1])][int(move_block_to[3])] = player_turn

def chars_to_board(chars):
    grid = [['' for _ in range(5)] for _ in range(5)]

    for i in range(5):
        for j in range(5):
            grid[i][j] = chars[i * 5 + j]

    return grid

def get_opponent(playing_as):
    if (playing_as == "X"):
        return "O"
    elif (playing_as == "O"):
        return "X"

def str_to_int_spot_data(x):
    spot_data = x[1:4].split(",")
    return int(spot_data[0]), int(spot_data[1])

def is_a_corner(spot_row, spot_col):
    if ((spot_row % 4 == 0) and spot_col % 4 == 0):
        return True
    return False

def check_for_streaks(board, team_looking_at):
    streaks = []

    for row in board:
        streaks.append(row.count(team_looking_at))

    for col in zip(*board):
        streaks.append(col.count(team_looking_at))

    team_in_downward_diagonal = 0
    for i in range(5):
        if (board[i][i] == team_looking_at):
            team_in_downward_diagonal += 1
    streaks.append(team_in_downward_diagonal)

    team_in_upward_diagonal = 0
    for i in range(5):
        if (board[i][len(board) - 1 - i] == team_looking_at):
            team_in_upward_diagonal += 1
    streaks.append(team_in_upward_diagonal)

    streaks.sort(reverse = True)
    return streaks

#Previously pushing middle, but that is not optimal because its too hard to finish off
def is_the_magic_bar(row, col):
    if (row == 3 and col == 4 or row == 3 and col == 1):
        return True
    return False

def score_pickup(spot_contains, player_turn, pickup_row, pickup_col, reasoning):
    pickup_score = 0

    reasoning = "Reasoning:"

    if (spot_contains == " "):
       pickup_score += 1500
       reasoning += " " + "Unclaimed piece" + ", "

    if (is_a_corner(pickup_row, pickup_col) and spot_contains == player_turn):
        pickup_score -= 1
        reasoning += " " + "Don't give up own corner" + ", "

    return pickup_score, reasoning

def generate_future_board(board, player_turn, pickup_row, pickup_col, placement_row, placement_col):
    future_board = copy.deepcopy(board)
    move_block_from = "(" + str(pickup_row) + "," + str(pickup_col) + ")"
    move_block_to = "(" + str(placement_row) + "," + str(placement_col) + ")"

    apply_move(future_board, move_block_from, move_block_to, player_turn)

    return future_board

def get_open_spots(board):
    total_open_spots = 0

    for x in EDGES_OF_THE_BOARD:
        pickup_row, pickup_col = str_to_int_spot_data(x)
        if (board[pickup_row][pickup_col] == " "):
            total_open_spots += 1

    return total_open_spots
    
def opponent_one_move_from_win(board, who_to_check_for):
    #get all the pieces your opp could move
    for move_from in EDGES_OF_THE_BOARD:
        move_from_data = move_from[1:4].split(",")
        row, col = int(move_from_data[0]), int(move_from_data[1])
        #check if a move for any leads to a win
        if (board[row][col] == who_to_check_for or board[row][col] == " "):
            list_of_placedowns = get_placements(row, col)
            for move_to in list_of_placedowns:
                move_to_data = move_to[1:4].split(",")
                placement_row, placement_col = int(move_to_data[0]), int(move_to_data[1])
                    
                super_future_board = generate_future_board(board, who_to_check_for, row, col, placement_row, placement_col)
                opp_super_future_streaks = check_for_streaks(super_future_board, who_to_check_for)[0]
                if (opp_super_future_streaks == 5):
                    return True
    return False

def get_pieces_on_board(board):
    total_pieces = 0
    for row in board:
        for item in row:
            if (item != " "):
                total_pieces += 1
    return total_pieces

def maybe_create_fork(future_board, opponent_as):
    top_streak = check_for_streaks(future_board, opponent_as)[0]
    second_from_top_streak = check_for_streaks(future_board, opponent_as)[1]

    if (top_streak == 4 and second_from_top_streak == 4):
        return True
    return False
        
def opp_pieces_on_edge(board, opponent_as):
    total_opp_spots = 0

    for x in EDGES_OF_THE_BOARD:
        pickup_row, pickup_col = str_to_int_spot_data(x)
        if (board[pickup_row][pickup_col] == opponent_as):
            total_opp_spots += 1

    return total_opp_spots

def score_placement(board, playing_as, pickup_row, pickup_col, placement_row, placement_col, reasoning):
    opponent_as = get_opponent(playing_as)

    #Board States
    future_board = generate_future_board(board, playing_as, pickup_row, pickup_col, placement_row, placement_col)
    
    #Streak Status
    your_current_streaks = check_for_streaks(board, playing_as)[0]
    your_future_streaks = check_for_streaks(future_board, playing_as)[0]
    opp_current_streaks = check_for_streaks(board, opponent_as)[0]
    opp_future_streaks = check_for_streaks(future_board, opponent_as)[0]

    placement_score = 0

    #DANGERS
    gives_up_a_free_piece = get_open_spots(future_board) > get_open_spots(board)
    no_open_spots_left = get_open_spots(board) == 0
    if (gives_up_a_free_piece and no_open_spots_left):
        placement_score -= 500
        reasoning += " " + "Don't give up a free piece" + ", "

    if (opp_future_streaks == 5):
        placement_score -= 5000
        reasoning += " " + "Gives Opp Win" + ", "

    if (opponent_one_move_from_win(future_board, opponent_as)):
        placement_score -= 10000
        reasoning += " " + "Sets up loss" + ", "

    if (maybe_create_fork(future_board, opponent_as)):
        placement_score -= 500
        reasoning += " " + "Creates fork?" + ", "

    if (your_future_streaks < your_current_streaks):
        placement_score -= 40
        reasoning += " " + "Hurts own max streak" + ", "

    #Does not add another opp to the rim
    if (opp_pieces_on_edge(board, opponent_as) < opp_pieces_on_edge(future_board, opponent_as)):
        placement_score -= 50
        reasoning += " " + "Gives opponent too much mobility" + ", "

    #POSITIVES
    if (board[2][2] == opponent_as and future_board[2][2] == playing_as):
        placement_score += 50
        reasoning += " " + "Takes Middle Piece" + ", "

    if (is_a_corner(placement_row, placement_col) and board[placement_row][placement_col] != playing_as):
        if (get_pieces_on_board(board) < 10):
            placement_score -= 5
            reasoning += " " + "Takes Corner too early" + ", "
        else:
            placement_score += 5
            reasoning += " " + "Takes Corner" + ", "

    if (opp_current_streaks > opp_future_streaks and opp_current_streaks == 3):
        placement_score += 100
        reasoning += " " + "Hurts Opponents Max Streak" + ", "

    if(future_board[2][2] == opponent_as):
        placement_score -= 50
        reasoning += " " + "Gives Opponent Middle" + ", "

    if (opp_current_streaks < 4 and is_the_magic_bar(placement_row, placement_col) and board[2][2] != playing_as):
        placement_score += 95
        reasoning += " " + "Push Middle" + ", "

    your_max_streak_inc = your_current_streaks < your_future_streaks
    opps_max_streak_does_not_get_scary = opp_future_streaks < 4
    if (your_max_streak_inc and opps_max_streak_does_not_get_scary):
        placement_score += 100 * your_future_streaks
        reasoning += " " + "Builds Streak and does not give opp 4 in a row" + ", "

    if (your_future_streaks == 5 and opp_future_streaks != 5):
        placement_score += 1000000
        reasoning += " " + "Wins" + ", "

    return placement_score, reasoning

def get_placements(row, col):
    spots = []

    spots.append("(" + str(row) + "," + str(0) + ")")
    spots.append("(" + str(row) + "," + str(4) + ")")
    spots.append("(" + str(0) + "," + str(col) + ")")
    spots.append("(" + str(4) + "," + str(col) + ")")
    spots.remove("(" + str(row) + "," + str(col) + ")")
    
    #Corners wll have their own spot twice, so we need an extra delete
    if is_a_corner(row, col):
        spots.remove("(" + str(row) + "," + str(col) + ")")

    return spots

def get_all_moves(board, playing_as):
    possible_moves = {}

    for x in EDGES_OF_THE_BOARD:
        pickup_row, pickup_col = str_to_int_spot_data(x)
        spot_contents = board[pickup_row][pickup_col]

        if (spot_contents == " " or spot_contents == playing_as):
            pickup_score = 0
            pickup_reasoning = ""
            pickup_score, pickup_reasoning = score_pickup(spot_contents, playing_as, pickup_row, pickup_col, pickup_reasoning)

            for spot in get_placements(pickup_row, pickup_col):
                placement_row, placement_col = str_to_int_spot_data(spot)
                placement_score = 0
                placement_reasoning = ""
                placement_score, placement_reasoning = score_placement(board, playing_as, pickup_row, pickup_col, placement_row, placement_col, placement_reasoning)

                combined_move = x + " " + spot
                if len(placement_reasoning) >= 2:
                    placement_reasoning = placement_reasoning[:-2]

                possible_moves[combined_move] = [(pickup_score + placement_score), (pickup_reasoning + placement_reasoning)]

    return possible_moves

def shuffle_scores_for_difficulty(possible_moves, difficulty):
    for move, score_reasoning in possible_moves.items():
        score_ding_amount = random.randint(-5000, 5000)
        score_reasoning[0] += score_ding_amount * difficulty
    return possible_moves


#1 Layer
#Get all possible moves with their scores
    #Generate all possible boards that could happen from opponent move
        #2 Layer
        #If there is a pin and not immediate loss select it
        #Add to the base score the #Of Winaable paths * 200
        #Get all possible moves with their scores
            #Generate all possible boards that could happen from opponent move
                #3 Layer
                #If there is a pin and not immediate loss select it
                #Add to the base score the #Of Winaable paths * 50

#How do I weight the current scores
#Do I add points to the current moves dictionary score
#Do I make it mega move scores

#I am keeping track of # of methods to win? Yes.
#Dont generate all possible moves, Check if opponent has no survivable moves (Searching for pin)

#You're not searching for the 3 move win, You're searching for the 3 move opponnet has lost
#THIS IS RIGHT

#All the right moves in all the right places, so yeah we're going down

#I think I should just check if it leads to certain death, if not then follow the fork/pin

def get_a_random_best_move(possible_moves):
    best_moves = [move for move, score in possible_moves.items() if int(score[0]) > (int(max(possible_moves.values())[0]) - 100)]
    random_best_move = random.choice(best_moves)
    return random_best_move.split(" ")

def get_best_moves(how_many_moves_to_get, possible_moves):
    sorted_moves = sorted(possible_moves.items(), key=lambda x: int(x[1][0]), reverse=True)
    return sorted_moves[:how_many_moves_to_get]

def new_request_ai_move(board, playing_as, difficulty):
    depth = 1

    possible_moves = None
    for i in range(depth):
        possible_moves = get_all_moves(board, playing_as)
        shuffle_scores_for_difficulty(possible_moves, difficulty)

        get_best_moves(10, possible_moves)
    spot_data = get_a_random_best_move(possible_moves)

    if (BUILD_OUTPUT_DATA_ON):
        for key, value in sorted(possible_moves.items(), key=lambda item: item[1]):
            print(f'{key}: {value}')
        if (playing_as == "X"):
            print("\n" + "\u001b[31m" + playing_as + " Move Chosen" + "\u001b[0m")
        elif (playing_as == "O"):
            print("\n" + "\u001b[35m" + playing_as + " Move Chosen" + "\u001b[0m")
        print(str(spot_data))
    
    return spot_data[0], spot_data[1]

new_request_ai_move(chars_to_board("                         "), "X", 0)

def request_ai_move(board, playing_as, difficulty):
    possible_moves = get_all_moves(board, playing_as)
    shuffle_scores_for_difficulty(possible_moves, difficulty) 

    #best_moves are moves with a rating within 100 of the max score in the moves list
    best_moves = [move for move, score in possible_moves.items() if int(score[0]) > (int(max(possible_moves.values())[0]) - 100)]
    random_best_move = random.choice(best_moves)
    spot_data = random_best_move.split(" ")
 
    if (BUILD_OUTPUT_DATA_ON):
        for key, value in sorted(possible_moves.items(), key=lambda item: item[1]):
            print(f'{key}: {value}')
        if (playing_as == "X"):
            print("\n" + "\u001b[31m" + playing_as + " Move Chosen" + "\u001b[0m")
        elif (playing_as == "O"):
            print("\n" + "\u001b[35m" + playing_as + " Move Chosen" + "\u001b[0m")
        print(str(spot_data))
    
    return spot_data[0], spot_data[1]