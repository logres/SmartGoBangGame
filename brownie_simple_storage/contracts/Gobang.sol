pragma solidity ^0.8.0;

contract Gobang {
    // 定义玩家结构体
    struct Player {
        address addr;
        bool isBlack;
    }

    // 定义棋盘状态结构体
    struct Chessboard {
        uint8[15][15] cells;
    }

    mapping(address => Player) public playerMapping;
    Player[2] public playerList;

    // 定义棋盘状态
    Chessboard chessboard;

    // 定义当前玩家
    Player public currentPlayer;

    Player public winner;

    // 定义游戏结束标志
    bool public gameOver;

    function start(address _player1, address _player2) public {
        // 初始化玩家信息
        playerMapping[_player1] = Player(_player1, true);
        playerMapping[_player2] = Player(_player2, false);

        playerList[0] = playerMapping[_player1];
        playerList[1] = playerMapping[_player2];

        // 初始化棋盘状态
        for (uint8 i = 0; i < 15; i++) {
            for (uint8 j = 0; j < 15; j++) {
                chessboard.cells[i][j] = 0;
            }
        }

        // 初始化当前玩家
        currentPlayer = playerMapping[msg.sender];

        // 初始化游戏结束标志
        gameOver = false;
    }

    // 公开函数，用于接收玩家的落子请求
    function play(uint8 x, uint8 y) public {
        // 检查游戏是否已结束
        require(!gameOver, "Game over");
        // 检查玩家是否合法
        require(msg.sender == currentPlayer.addr, "Not your turn");
        // 检查落子坐标是否合法
        require(x >= 0 && x < 15 && y >= 0 && y < 15, "Invalid position");
        // 检查该位置是否已落子
        require(chessboard.cells[x][y] == 0 , "Position occupied");
        // 落子
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

    // 私有函数，用于检查游戏是否结束
    function checkWin(uint8 x, uint8 y) private view returns (bool) {
        // 检查水平方向是否连成五子
        if (checkLine(x, y, 1, 0)) return true;
        // 检查竖直方向是否连成五子
        if (checkLine(x, y, 0, 1)) return true;
        // 检查斜线方向是否连成五子
        if (checkLine(x, y, 1, 1)) return true;
        if (checkLine(x, y, -1, 1)) return true;
        return false;
    }

    // 私有函数，用于检查单行是否连成五子
    function checkLine(uint8 x, uint8 y, int8 dx, int8 dy) private view returns (bool) {
        uint8 color = chessboard.cells[x][y];
        uint8 count = 1;
        // 向左搜索
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
        // 向右搜索
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