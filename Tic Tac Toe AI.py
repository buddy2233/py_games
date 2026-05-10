import random

board = [' ' for _ in range(9)]

def print_board():
    row1 = '|1. {}  |2. {}  |3. {}  |'.format(board[0], board[1], board[2])
    row2 = '|4. {}  |5. {}  |6. {}  |'.format(board[3], board[4], board[5])
    row3 = '|7. {}  |8. {}  |9. {}  |'.format(board[6], board[7], board[8])


    print()
    print(row1)
    print(row2)
    print(row3)
    print()

def check_win():
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] != ' ':
            return board[condition[0]]
    if ' ' not in board:
        return 'Tie'
    return False

def bot_move():
    possible_moves = [i for i, x in enumerate(board) if x == ' ']
    move = random.choice(possible_moves)
    board[move] = 'O'

def game():
    while True:
        print_board()
        move = input("Enter your move (1-9): ")
        if board[int(move) - 1] == ' ':
            board[int(move) - 1] = 'X'
            result = check_win()
            if result:
                print_board()
                if result == 'Tie':
                    print("It's a tie!")
                else:
                    print("Player {} wins! Congratulations!".format(result))
                break
            bot_move()
            result = check_win()
            if result:
                print_board()
                if result == 'Tie':
                    print("It's a tie!")
                else:
                    print("Player {} wins! Congratulations!".format(result))
                break
        else:
            print("Invalid move, try again.")

if __name__ == "__main__":
    game()
