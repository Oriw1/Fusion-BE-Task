

class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.current_player = 'X'
        self.winner = None

    def make_move(self, position: int) -> bool:
        if self.board[position] != ' ' or self.winner:
            return False
        self.board[position] = self.current_player
        if self.check_winner():
            self.winner = self.current_player
        elif ' ' not in self.board:
            self.winner = 'Draw'
        else:
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def check_winner(self) -> bool:
        b = self.board
        lines = [
            [b[0], b[1], b[2]], [b[3], b[4], b[5]], [b[6], b[7], b[8]],
            [b[0], b[3], b[6]], [b[1], b[4], b[7]], [b[2], b[5], b[8]],
            [b[0], b[4], b[8]], [b[2], b[4], b[6]]
        ]
        return any(line == [self.current_player]*3 for line in lines)

    def get_state(self):
        return {
            "board": self.board,
            "current_player": self.current_player,
            "winner": self.winner
        }

    def reset(self):
        self.board = [" "] * 9
        self.current_player = "X"
        self.winner = None
