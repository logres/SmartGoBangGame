import pygame
from web3 import Web3
import json
import os
import dotenv
import time

dotenv.load_dotenv()


class Game:

    def __init__(self):
        self.screen_size = (450, 450)
        self.board_size = 15
        self.board = []
        for _ in range(self.board_size):
            self.board.append([0] * self.board_size)
        self.piece_size = 30
        self.current_player = 1
        self.winner = 0

        self.w3 = Web3(Web3.HTTPProvider(os.getenv('Web3Provider')))
        contract_address = Web3.toChecksumAddress(os.getenv('Contract_Address'))
        contract_abi = json.load(open("Gobang.json"))['abi']
        self.contract = self.w3.eth.contract(address=contract_address, abi=contract_abi)

    def web3_play(self, x, y):
        tx = self.contract.functions.play(x, y).buildTransaction({
            'chainId': 5,
            'from': self.account.address,
            'nonce': self.w3.eth.getTransactionCount(self.account.address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.account._private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        print(tx_receipt)

    def web3_start(self, address1, address2):
        tx = self.contract.functions.start(self.w3.toChecksumAddress(address1),
                                                self.w3.toChecksumAddress(address2)).buildTransaction({
                                                    'chainId': 5,
                                                    'from': self.account.address,
                                                    'nonce': self.w3.eth.getTransactionCount(self.account.address),})
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.account._private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        print(tx_receipt)

    def start(self):

        clock = pygame.time.Clock()
        self.player = int(input("Choose player (1 or 2): "))
        self.private_key = os.getenv("PRIVATE_KEY1") if self.player == 1 else os.getenv("PRIVATE_KEY2")

        self.account = self.w3.eth.account.from_key(self.private_key)

        # 初始化合约
        if self.player == 1:
            address1 = self.w3.toChecksumAddress(os.getenv("ADDRESS1"))
            address2 = self.w3.toChecksumAddress(os.getenv("ADDRESS2"))
            self.web3_start(address1, address2)

        self.event = self.contract.events.ChessSet.createFilter(fromBlock='latest')

        # Initialize game engine
        pygame.init()
        screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Gobang"+str(self.player))

        # Set colors
        background_color, black, white = (
            128, 128, 128), (0, 0, 0), (255, 255, 255)

        # Game loop
        running = True
        while running:
            clock.tick(60)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    x = x // self.piece_size
                    y = y // self.piece_size
                    self.web3_play(x, y)

            # Sync data
            events = self.event.get_new_entries()
            for event in events:
                x = event['args']['x']
                y = event['args']['y']
                player = event['args']['player']
                self.board[y][x] = 1 if player == self.w3.toChecksumAddress(os.getenv("ADDRESS1")) else 2

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
