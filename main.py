import pygame
import random

# game modes
PVP = 1
PVE = 2

# constants
WINDOW_SIZE = (300, 350)
CELL_SIZE = 100
CELL_PADDING = 10
LINE_WIDTH = 5
GRAY = (128, 128, 128)

# initialize Pygame
pygame.init()

# create the game window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Tic Tac Toe")

# create the game font
font = pygame.font.SysFont(None, 50)

# create the game board
board = [["", "", ""],
         ["", "", ""],
         ["", "", ""]]

# create the game variables
turn = "X"
winner = ""
game_mode = PVE

def draw_board():
    # draw the lines of the board
    pygame.draw.line(screen, GRAY, (CELL_SIZE, 0), (CELL_SIZE, WINDOW_SIZE[1]), LINE_WIDTH)
    pygame.draw.line(screen, GRAY, (2*CELL_SIZE, 0), (2*CELL_SIZE, WINDOW_SIZE[1]), LINE_WIDTH)
    pygame.draw.line(screen, GRAY, (0, CELL_SIZE), (WINDOW_SIZE[0], CELL_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, GRAY, (0, 2*CELL_SIZE), (WINDOW_SIZE[0], 2*CELL_SIZE), LINE_WIDTH)

    # draw the X's and O's on the board
    for row in range(3):
        for col in range(3):
            if board[row][col] == "X":
                x = col * CELL_SIZE + CELL_PADDING
                y = row * CELL_SIZE + CELL_PADDING
                pygame.draw.line(screen, GRAY, (x, y), (x+CELL_SIZE-2*CELL_PADDING, y+CELL_SIZE-2*CELL_PADDING), LINE_WIDTH)
                pygame.draw.line(screen, GRAY, (x+CELL_SIZE-2*CELL_PADDING, y), (x, y+CELL_SIZE-2*CELL_PADDING), LINE_WIDTH)
            elif board[row][col] == "O":
                x = col * CELL_SIZE + CELL_SIZE//2
                y = row * CELL_SIZE + CELL_SIZE//2
                pygame.draw.circle(screen, GRAY, (x, y), CELL_SIZE//2 - CELL_PADDING, LINE_WIDTH)

def check_win():
    global winner

    # check rows for a win
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != "":
            winner = board[row][0]
            return True

    # check columns for a win
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != "":
            winner = board[0][col]
            return True

    # check diagonals for a win
    if board[0][0] == board[1][1] == board[2][2] != "":
        winner = board[0][0]
        return True
    elif board[0][2] == board[1][1] == board[2][0] != "":
        winner = board[0][2]
        return True

    # check for a tie
    if all(cell != "" for row in board for cell in row):
        winner = "Tie"
        return True

    return False

def get_player_move():
    # get the row and column of the clicked cell
    row, col = pygame.mouse.get_pos()
    row //= CELL_SIZE
    col //= CELL_SIZE

    # update the board with the player's move
    if board[row][col] == "":
        board[row][col] = turn
        return True

    return False

def get_ai_move():
    # choose a random empty cell for the AI's move
    empty_cells = []
    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                empty_cells.append((row, col))
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = turn
        return True

    return False

def switch_turn():
    global turn
    if turn == "X":
        turn = "O"
    else:
        turn = "X"

def reset_game():
    global board, turn, winner
    board = [["", "", ""],
             ["", "", ""],
             ["", "", ""]]
    turn = "X"
    winner = ""

running = True
while running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP and game_mode == PVP:
            if get_player_move():
                if check_win():
                    print(winner)
                else:
                    switch_turn()
        elif event.type == pygame.MOUSEBUTTONUP and game_mode == PVE:
            if get_player_move():
                if check_win():
                    print(winner)
                else:
                    switch_turn()
                    get_ai_move()
                    if check_win():
                        print(winner)
                    else:
                        switch_turn()

    # draw the game board
    screen.fill((255, 255, 255))
    draw_board()

    # draw the game over message
    if winner != "":
        text = font.render(winner + " wins!", True, GRAY)
        screen.blit(text, (WINDOW_SIZE[0]//2 - text.get_width()//2, 310))
        pygame.display.update()
        pygame.time.wait(3000)
        reset_game()

    # update the screen
    pygame.display.update()

# quit Pygame
pygame.quit()

