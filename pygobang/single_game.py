import pygame


# Initialize game engine
pygame.init()

# Set game screen size
screen_size = (450, 450)
screen = pygame.display.set_mode(screen_size)

# Set colors
background_color = (128, 128, 128)
black = (0, 0, 0)
white = (255, 255, 255)

# Game board
board_size = 15
board = []
for i in range(board_size):
    board.append([0] * board_size)

# Piece size
piece_size = 30

# Player moves
player = 1

def check_win(board, x, y):
    def check_line(x, y, dx, dy):
        count = 0
        piece = board[y][x]
        while 0 <= x < board_size and 0 <= y < board_size and board[y][x] == piece:
            count += 1
            x += dx
            y += dy
        return count

    for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
        count = check_line(x, y, dx, dy) + check_line(x, y, -dx, -dy) - 1
        if count >= 5:
            return board[y][x]
    return 0

def check_line(x, y, dx, dy):
    count = 0
    piece = board[y][x]
    while 0 <= x < board_size and 0 <= y < board_size and board[y][x] == piece:
        count += 1
        x += dx
        y += dy
    return count

def check_tie(board):
    for row in board:
        if 0 in row:
            return False
    return True


# Game loop
running = True
while running:

    # Deal with events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            x = x // piece_size
            y = y // piece_size
            if x < board_size and y < board_size and board[y][x] == 0:
                board[y][x] = player
                player = 3 - player
                winner = check_win(board, x, y)
                if winner:
                    running = False
                    print("Player {} wins!".format(winner))
                elif check_tie(board):
                    running = False
                    print("Tie game!")

    # Draw game board
    screen.fill(background_color)
    for i in range(board_size):
        for j in range(board_size):
            piece = board[i][j]
            if piece == 0:
                continue
            x = j * piece_size
            y = i * piece_size
            color = black if piece == 1 else white
            pygame.draw.circle(screen, color, (x + piece_size // 2, y + piece_size // 2), piece_size // 2 - 2)

    # Draw grid lines
    for i in range(board_size):
        x = i * piece_size
        pygame.draw.line(screen, black, (x, 0), (x, screen_size[1]))
        y = i * piece_size
        pygame.draw.line(screen, black, (0, y), (screen_size[0], y))

    # Update display
    pygame.display.update()

# Quit game engine
pygame.quit()
