import tkinter as tk
from tkinter import messagebox

class AlphaBetaPruning:
    def __init__(self, game_state):
        self.board = game_state
        self.ai_player = 'O'
        self.human_player = 'X'

    def is_terminal(self, state):
        return self.check_winner(state, self.ai_player) or self.check_winner(state, self.human_player) or ' ' not in state

    def heuristic(self, state):
        score = 0
        win_conditions = [
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        ]
        for condition in win_conditions:
            ai_count = sum(1 for pos in condition if state[pos] == self.ai_player)
            human_count = sum(1 for pos in condition if state[pos] == self.human_player)
            if ai_count > 0 and human_count == 0:
                score += ai_count
            elif human_count > 0 and ai_count == 0:
                score -= human_count
        return score

    def alphabeta(self, state, depth, alpha, beta, maximizing_player):
        if self.is_terminal(state):
            return self.heuristic(state)

        if maximizing_player:
            best_score = float('-inf')
            for i in range(9):
                if state[i] == ' ':
                    state[i] = self.ai_player
                    score = self.alphabeta(state, depth + 1, alpha, beta, False)
                    state[i] = ' '
                    best_score = max(best_score, score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if state[i] == ' ':
                    state[i] = self.human_player
                    score = self.alphabeta(state, depth + 1, alpha, beta, True)
                    state[i] = ' '
                    best_score = min(best_score, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
            return best_score

    def best_move(self, state):
        best_score = float('-inf')
        move = -1
        for i in range(9):
            if state[i] == ' ':
                state[i] = self.ai_player
                score = self.alphabeta(state, 0, float('-inf'), float('inf'), False)
                state[i] = ' '
                if score > best_score:
                    best_score = score
                    move = i
        return move

    def check_winner(self, state, player):
        win_conditions = [
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        ]
        return any(all(state[pos] == player for pos in condition) for condition in win_conditions)


class TicTacToeGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe – Alpha Beta Pruning")
        self.board = [' '] * 9
        self.ai = AlphaBetaPruning(self.board)
        self.buttons = []
        self.create_board()

    def create_board(self):
        for i in range(9):
            button = tk.Button(self.window, text=' ', font=('Arial', 32), width=5, height=2,
                               command=lambda i=i: self.player_move(i))
            button.grid(row=i//3, column=i%3)
            self.buttons.append(button)

    def player_move(self, index):
        if self.board[index] == ' ':
            self.board[index] = 'X'
            self.buttons[index]['text'] = 'X'
            if self.ai.check_winner(self.board, 'X'):
                self.end_game("You win!")
                return
            elif ' ' not in self.board:
                self.end_game("It's a draw!")
                return
            self.ai_move()

    def ai_move(self):
        move = self.ai.best_move(self.board)
        if move != -1:
            self.board[move] = 'O'
            self.buttons[move]['text'] = 'O'
            if self.ai.check_winner(self.board, 'O'):
                self.end_game("AI wins!")
            elif ' ' not in self.board:
                self.end_game("It's a draw!")

    def end_game(self, message):
        messagebox.showinfo("Game Over", message)
        self.window.after(500, self.window.destroy)

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    game = TicTacToeGUI()
    game.run()
