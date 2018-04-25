# This is a dummy AI example to help you doing program assignment 2.
# We implemented the file I/O part. 
# You may focus on the method, _get_next_move(), 
# which is a method to decide where to place your stone based on the current game state,
# including (1) valid position, (2) your position, (3) your opponent position, 
# (4) board and (5) the winner of first game.
# !! Remember to change the team number in main() !!

import os
from random import randint

class Agent:
    """
    Game agent.
    The procedure:
        1. process_state_info: check game state
        2. is_my_turn: if it is my turn, decide a position to put stone
        3. step: call get_next_move and write the result to move file
    """
    def __init__(self, team_number):
        self.team_number = team_number
        self.stat_file = "state_" + str(team_number) + ".txt"
        self.move_file = "move_" + str(team_number) + ".txt"

        self.cur_move = -1
        self.next_first_move = -1
        self.first_winner = -1
        self.game_stop = False

        self.valid_pos = []
        self.my_pos = []
        self.opponent_pos = []
    
    def process_state_info(self):
        """
        Read state file and get valid position.
        If not my turn to make move, return an empty list.
        """
        self.valid_pos = []
        self.my_pos = []
        self.opponent_pos = []

        # get state file info
        try:
            if not os.path.isfile(self.stat_file):
                return

            sfile = open(self.stat_file, "r")
            if os.stat(self.stat_file).st_size == 0:
                return

            move = int(sfile.readline())
            self.board = map(int, sfile.readline().split())
            self.first_winner = int(sfile.readline())
            sfile.close()
        except:
            return

        if move == -100:
            self.game_stop = True
            return

        # The only condition of move read from state file being less than our record move (cur_move)
        # is that the second game starts.
        # So, if move is less than cur_move and is not next_first_move,
        # just skip it
        if move > self.cur_move or (move == self.next_first_move and self.cur_move != self.next_first_move):
            # If we are making the first move of first game,
            # record the first move of the second game
            if self.cur_move == -1:
                self.next_first_move = 2 if move == 1 else 1
            
            # Record current move
            self.cur_move = move

            self.valid_pos = [i for i in range(217) if self.board[i] == 0]
            self.my_pos = [i for i in range(217) if self.board[i] == 1]
            self.opponent_pos = [i for i in range(217) if self.board[i] == 2]
        else:
            return

    def step(self):
        """
        Get the next move and write it into move file.
        """
        pos = self._get_next_move()
        self._write_move(pos)

    def _get_next_move(self):
        """
        Get a position from valid_pos randomly.
        You should implement your algorithm here.
        These utilities may be helpful:
            self.get_valid_pos()
            self.get_my_pos()
            self.get_opponent_pos()
            self.get_board()

        Check them below for more detail
        """
        return self.valid_pos[randint(0, len(self.valid_pos)-1)]

    def _write_move(self, pos):
        """
        Write my move into move file.
        """
        with open(self.move_file, "w") as mfile:
            mfile.write(str(self.cur_move) + " " + str(pos))

    def is_my_turn(self):
        """
        If the valid position is not empty, it is my turn.
        """
        return len(self.valid_pos) != 0

    def is_game_stop(self):
        return self.game_stop

    # some utilities to get the game state
    def get_valid_pos(self):
        """
        Get the valid position where you can put your stone.
        A list of int. e.g. [0, 1, 3, 5, 6, 9, 12,...]
        """
        return self.valid_pos

    def get_my_pos(self):
        """
        Get the position where you have put.
        A list of int. e.g. [2, 4, 7, 8, ...]
        """
        return self.my_pos

    def get_opponent_pos(self):
        """
        Get the position where your opponent have put.
        A list of int. e.g. [10, 11, 13, ...]
        """
        return self.opponent_pos

    def get_board(self):
        """
        Get current board. 0: valid pos, 1: your pos, 2: opponent pos
        A list of int. e.g. [0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 2, 2, 0, 2...]
        """
        return self.board

    def is_first_winner(self):
        """
        Are you the winner of first game?
        Return -1: the first game is still continuing.
                1: yes, you are.
                0: no, you are not.
        """
        return self.first_winner

def main():
    # Change the team number to yours.
    agent = Agent(5566)

    while True:
        agent.process_state_info()
        if (agent.is_game_stop()):
            break

        if (agent.is_my_turn()):
            agent.step()


if __name__ == "__main__":
    main()