# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

class Mancala:
    
    def __init__(self):
        self.pockets = self.initialize_board()
    
    def initialize_board(self):
        
        pockets = [4]*14
        pockets[6] = 0
        pockets[13] = 0
        
        return pockets
    
    def determine_winner(self):
        
        if self.pockets[13]>self.pockets[6]:
            return "Player 2"
        elif self.pockets[13]<self.pockets[6]:
            return "Player 1"
        return "Draw"
    
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
        
        # For normal stone drop conditions switch player
        if player == 1:
            next_player = 2
        else:
            next_player = 1
        
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