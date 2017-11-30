# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

class Mancala:
    
    def __init__(self):
        self.pockets = self.initialize_board()
        self.play_game()
        
    def play_game(self):
        
        # Reset board
        self.initialize_board()
        
        # Assume both players are humans for now
        player_1 = 'human'
        player_2 = 'human'
        
        player_turn = 1
        
        while not(self.check_game_over()):
            
            # Ask for move from corresponding player
            if player_turn == 1:
                if player_1 == 'human':
                    move = input("Choose Pocket 1-6: ")
                    move = convert_move(move, player=1)
                if player_2 == 'human':
                    move = input("Choose Pocket 1-6 on Other Side")
                    move = convert_move(move, player=2)
            
    def convert_move(self, move, player):
        """ Converts the standard 1-6 input of the player into the corresponding
        pocket for each player as needed
        """
        if player == 1:
            return move-1 # Shift left once to get the pocket position
        if player == 2:
            return move+6 # Shift right 6 spaces to refer to upper board spot
        return False # Error case handling
    
    def valid_move(self, pocket_position, player):
        
        # Move is invalid if player chooses anything other than own pockets
        player_1_side = (0 <= pocket_position <= 5)
        player_2_side = (7 <= pocket_position <= 12)
        
        # Must have stones in the pocket to be valid
        if self.pockets[pocket_position] > 0:
            if player_1_side and player==1:
                return True
            if player_2_side and player==2:
                return True
            
        # All other moves are false
        return False
    
    def initialize_board(self):
        
        pockets = [4]*14
        pockets[6] = 0
        pockets[13] = 0
        
        return pockets
    
    def check_game_over(self):
        """ Checks if all pockets are empty of stones. If so assigns all
            remaining stones to the appropriate mancala.
        """
        empty_player_1 = sum(self.pockets[:6]) == 0
        empty_player_2 = sum(self.pockets[7:13]) == 0
        
        # Check for empty player 1
        if empty_player_1:
            # Put remaining stones in player 2's mancala
            self.pockets[13] = sum(self.pockets[7:13])
            self.pockets[7:13] = [0]*6
            return True
        
        if empty_player_2:
            # Put remaining stones in player 2's mancala
            self.pockets[6] = sum(self.pockets[:6])
            self.pockets[:6] = [0]*6
            return True
        
        return False
    
    def determine_winner(self):
        
        if self.pockets[13]>self.pockets[6]:
            return "Player 2"
        elif self.pockets[13]<self.pockets[6]:
            return "Player 1"
        return "Draw"
    
    def switch_player(self, player):
        
        if player == 1:
            return 2
        return 1
    
    def capture(self, pocket_position, mancala_pocket):
        """ Captures all stones in the pocket and pocket opposite, goes into
        The proper mancala pocket specified as input
        """
        
        opposite_pocket_dict = {0: 12, 1:11, 2:10, 3:9, 4:8, 5:7,
                                7:5, 8:4, 9:3, 10:2, 11:1, 12:0}
        
        # Take the stone from the pocket itself
        self.pockets[mancala_pocket] += self.pockets[pocket_position]
        self.pockets[pocket_position] = 0
        
        # Take the stones from the opposite pocket
        opposite_pocket = opposite_pocket_dict[pocket_position]
        self.pockets[mancala_pocket] += self.pockets[opposite_pocket]
        self.pockets[opposite_pocket] = 0
        
        return True
    
    def simulate_move(self, pocket_position, player):
        
        # Condense to local version of pockets
        pockets = self.pockets
        
        stones_drawn = pockets[pocket_position]
        pockets[pocket_position] = 0
        
        # Inefficient loop, clean up in future
        while stones_drawn > 0:
            pocket_position += 1
            
            # Case to handle looping back to start of board
            if pocket_position > len(pockets)-1:
                pocket_position = 0
                
            # Consider special cases (mancala pocket) before normal stone drops
            mancala_1_position = pocket_position==6
            mancala_2_position = pocket_position==13
            player_1 = player == 1
            player_2 = player == 2
            if mancala_1_position and player_2:
                continue # Skip stone drop and proceeding logic
            if mancala_2_position and player_1:
                continue # Skip stone drop and proceeding logic
                
            # Stone drop
            pockets[pocket_position] += 1
            stones_drawn -= 1
        
        # Determine if capture occurs
        end_on_player_1_side = (0 <= pocket_position <= 5)
        end_on_player_2_side = (7 <= pocket_position <= 12)
        
        # Only capture if stone is empty (has 1 stone after placement)
        stone_was_empty = pockets[pocket_position] == 1
        
        # Player 1 capture
        if player_1 and end_on_player_1_side and stone_was_empty:
            self.capture(pocket_position, 6)
            
        # Player 2 capture
        if player_2 and end_on_player_2_side and stone_was_empty:
            self.capture(pocket_position, 13)
        
        # Determine next player
        if mancala_1_position and player_1:
            next_player = player # Player 1 Mancala gets another turn
        elif mancala_2_position and player_2:
            next_player = player # Player 2 Mancala gets another turn
        else:
            next_player = self.switch_player(player) # All else switch player
        
        return next_player
    
    def draw_board(self):
        
        # Unpack list of stones in each spot for readability
        pocket_1 = "{0:0>2}".format(self.pockets[0])
        pocket_2 = "{0:0>2}".format(self.pockets[1])
        pocket_3 = "{0:0>2}".format(self.pockets[2])
        pocket_4 = "{0:0>2}".format(self.pockets[3])
        pocket_5 = "{0:0>2}".format(self.pockets[4])
        pocket_6 = "{0:0>2}".format(self.pockets[5])
        mancala_1 = "{0:0>2}".format(self.pockets[6])
        
        pocket_7 = "{0:0>2}".format(self.pockets[7])
        pocket_8 = "{0:0>2}".format(self.pockets[8])
        pocket_9 = "{0:0>2}".format(self.pockets[9])
        pocket_10 = "{0:0>2}".format(self.pockets[10])
        pocket_11 = "{0:0>2}".format(self.pockets[11])
        pocket_12 = "{0:0>2}".format(self.pockets[12])
        mancala_2 = "{0:0>2}".format(self.pockets[13])
        
        lower_pockets = [pocket_1,pocket_2,pocket_3,pocket_4,pocket_5,pocket_6]
        upper_pockets = [pocket_12,pocket_11,pocket_10,pocket_9,pocket_8,pocket_7]
        
        print("___________________________________________________________________")
        print("|  ____     ____    ____    ____    ____    ____    ____          |")
        print("| |    |   [_{}_]  [_{}_]  [_{}_]  [_{}_]  [_{}_]  [_{}_]   ____  |".format(*upper_pockets))
        print("| | {} |                                                   |    | |".format(mancala_2))
        print("| |____|    ____    ____    ____    ____    ____    ____   | {} | |".format(mancala_1))
        print("|          [_{}_]  [_{}_]  [_{}_]  [_{}_]  [_{}_]  [_{}_]  |____| |".format(*lower_pockets))
        print("|_________________________________________________________________|")
        
        return True