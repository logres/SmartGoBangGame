import pygame
import socket
import json

class Game:

    address1 = ('127.0.0.1', 5001)
    address2 = ('127.0.0.1', 5002)

    def __init__(self):
        self.screen_size = (450, 450)
        self.board_size = 15
        self.board = []
        for _ in range(self.board_size):
            self.board.append([0] * self.board_size)
        self.piece_size = 30
        self.current_player = 1
        self.winner = 0

    def check_win(self, x, y):
        def check_line(x, y, dx, dy):
            count = 0
            piece = self.board[y][x]
            while 0 <= x < self.board_size and 0 <= y < self.board_size and self.board[y][x] == piece:
                count += 1
                x += dx
                y += dy
            return count

        for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
            count = check_line(x, y, dx, dy) + check_line(x, y, -dx, -dy) - 1
            if count >= 5:
                return self.board[y][x]
        return 0

    def check_line(self,x, y, dx, dy):
        count = 0
        piece = self.board[y][x]
        while 0 <= x < self.board_size and 0 <= y < self.board_size and self.board[y][x] == piece:
            count += 1
            x += dx
            y += dy
        return count

    def check_tie(self):
        for row in self.board:
            if 0 in row:
                return False
        return True


    def start(self):
        self.player = int(input("Player 1 or 2? "))
        self.address = self.address1 if self.player == 1 else self.address2
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.my_socket.setblocking(False)
        self.my_socket.bind(self.address)

        # Initialize game engine
        pygame.init()
        screen = pygame.display.set_mode(self.screen_size)

        # Set colors
        background_color, black, white = (
            128, 128, 128), (0, 0, 0), (255, 255, 255)

        # Game loop
        running = True
        while running:
            try:
                data, _ = self.my_socket.recvfrom(1024)
                data = data.decode('utf-8')
                data = json.loads(data)

                self.board = data['board']
                self.current_player = data['current_player']
                self.winner = data['winner']

                if self.winner:
                    running = False
                    print("Player {} wins!".format(self.winner))

            except ConnectionResetError:
                pass
            except BlockingIOError:
                pass
            
            changed = False

            # Deal with events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.winner = 3 - self.player
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.current_player != self.player:
                        continue
                    x, y = pygame.mouse.get_pos()
                    x = x // self.piece_size
                    y = y // self.piece_size
                    if x < self.board_size and y < self.board_size and self.board[y][x] == 0:
                        self.board[y][x] = self.player
                        self.current_player = 3 - self.player
                        changed = True
                        self.winner = self.check_win(x, y)
                        if self.winner:
                            running = False
                            print("Player {} wins!".format(self.winner))
                        elif self.check_tie():
                            running = False
                            print("Tie game!")

            if changed:
                data = {
                    'board': self.board,
                    'current_player': self.current_player,
                    'winner': self.winner 
                }
                data = json.dumps(data)
                self.my_socket.sendto(data.encode('utf-8'),self.address1 if self.player == 2 else self.address2)

            # Draw game board
            screen.fill(background_color)
            for i in range(self.board_size):
                for j in range(self.board_size):
                    piece = self.board[i][j]
                    if piece == 0:
                        continue
                    x = j * self.piece_size
                    y = i * self.piece_size
                    color = black if piece == 1 else white
                    pygame.draw.circle(
                        screen, color, (x + self.piece_size // 2, y + self.piece_size // 2), self.piece_size // 2 - 2)

            # Draw grid lines
            for i in range(self.board_size):
                x = i * self.piece_size
                pygame.draw.line(screen, black, (x, 0), (x, self.screen_size[1]))
                y = i * self.piece_size
                pygame.draw.line(screen, black, (0, y), (self.screen_size[0], y))

            # Update display
            pygame.display.update()

        # Quit game engine
        pygame.quit()


Game().start()
