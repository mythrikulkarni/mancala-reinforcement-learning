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