pragma solidity ^0.8.0;

contract Gobang {
    // ������ҽṹ��
    struct Player {
        address addr;
        bool isBlack;
    }

    // ��������״̬�ṹ��
    struct Chessboard {
        uint8[15][15] cells;
    }

    mapping(address => Player) public playerMapping;
    Player[2] public playerList;

    // ��������״̬
    Chessboard chessboard;

    // ���嵱ǰ���
    Player public currentPlayer;

    Player public winner;

    // ������Ϸ������־
    bool public gameOver;

    function start(address _player1, address _player2) public {
        // ��ʼ�������Ϣ
        playerMapping[_player1] = Player(_player1, true);
        playerMapping[_player2] = Player(_player2, false);

        playerList[0] = playerMapping[_player1];
        playerList[1] = playerMapping[_player2];

        // ��ʼ������״̬
        for (uint8 i = 0; i < 15; i++) {
            for (uint8 j = 0; j < 15; j++) {
                chessboard.cells[i][j] = 0;
            }
        }

        // ��ʼ����ǰ���
        currentPlayer = playerMapping[msg.sender];

        // ��ʼ����Ϸ������־
        gameOver = false;
    }

    // �������������ڽ�����ҵ���������
    function play(uint8 x, uint8 y) public {
        // �����Ϸ�Ƿ��ѽ���
        require(!gameOver, "Game over");
        // �������Ƿ�Ϸ�
        require(msg.sender == currentPlayer.addr, "Not your turn");
        // ������������Ƿ�Ϸ�
        require(x >= 0 && x < 15 && y >= 0 && y < 15, "Invalid position");
        // ����λ���Ƿ�������
        require(chessboard.cells[x][y] == 0 , "Position occupied");
        // ����
        chessboard.cells[x][y] = currentPlayer.isBlack ? 1 : 2;
        emit ChessSet(x, y, msg.sender);
        if (checkWin(x,y)) {
            gameOver = true;
            winner = currentPlayer;
            emit GameOver(msg.sender);
        }else{
            currentPlayer = playerList[currentPlayer.isBlack ? 1 : 0];
        }
    }

    // ˽�к��������ڼ����Ϸ�Ƿ����
    function checkWin(uint8 x, uint8 y) private view returns (bool) {
        // ���ˮƽ�����Ƿ���������
        if (checkLine(x, y, 1, 0)) return true;
        // �����ֱ�����Ƿ���������
        if (checkLine(x, y, 0, 1)) return true;
        // ���б�߷����Ƿ���������
        if (checkLine(x, y, 1, 1)) return true;
        if (checkLine(x, y, -1, 1)) return true;
        return false;
    }

    // ˽�к��������ڼ�鵥���Ƿ���������
    function checkLine(uint8 x, uint8 y, int8 dx, int8 dy) private view returns (bool) {
        uint8 color = chessboard.cells[x][y];
        uint8 count = 1;
        // ��������
        uint8 i = uint8(int8(x) + dx);
        uint8 j = uint8(int8(y) + dy);
        for (; i >= 0 && i < 15 && j >= 0 && j < 15;) {
            if (chessboard.cells[i][j] == color) {
                count++;
                if (count == 5) return true;
            } else {
                break;
            }
            i = uint8(int8(i) + dx);
            j = uint8(int8(j) + dy);
        }
        // ��������
        i = uint8(int8(x) - dx);
        j = uint8(int8(y) - dy);
        for (; i >= 0 && i < 15 && j >= 0 && j < 15;) {
            if (chessboard.cells[i][j] == color) {
                count++;
                if (count == 5) return true;
            } else {
                break;
            }
        i = uint8(int8(i) - dx);
        j = uint8(int8(j) - dy);
        }
        return false;
    }

    event GameOver(address winner);

    event ChessSet(uint8 x, uint8 y, address player);
}