# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import random
import numpy as np
import agent

class Mancala:
    
    def __init__(self):
        self.pockets = self.initialize_board()
        self.mancala_agent = agent.Agent()
        
    def play_game(self):
        
        # Reset board
        self.initialize_board()
        
        player_1 = 'computer'
        player_2 = 'computer'
        mancala_agent = self.mancala_agent
        mancala_agent.previous_state = self.get_state(player=2)
        
#        
#        # Assume both players are humans for now
#        player_1 = 'human'
#        player_2 = 'human'
#        
#        # Computer or human player 1
#        if input("Player 1 human? (y/n) ") == 'n':
#            player_1 = 'computer'
#            #mancala_agent = agent.Agent()
#        
#        # Proc user for computer or human opponent
#        if input("Player 2 human? (y/n) ") == 'n':
#            player_2 = 'computer'
#            mancala_agent = agent.Agent()
#            mancala_agent.previous_state = self.get_state(player=2)
        
        player_turn = 1
        previous_move = -1 # Previous move marked in board draw
        
        game_over = False
        while not(game_over):
            
            # Start by drawing the board
            self.draw_board(previous_move)
            
            # Ask for move from corresponding player
            if player_turn == 1:
                if player_1 == 'human':
                    move = int(input("Player 1 - Choose Pocket 1-6: "))
                    move = self.convert_move(move, player=1)
                else:
                    # Basic computer randomly chooses a Mancala position
                    valid_move = False
                    while not(valid_move):
                        move = self.convert_move(random.randint(1,6),player_turn)
                        valid_move = self.valid_move(move, player_turn)
            else:
                if player_2 == 'human':
                    move = int(input("Player 2 - Choose Pocket 1-6: "))
                    move = self.convert_move(move, player=2)
                else:
                    # Basic computer randomly chooses a Mancala position
                    valid_move = False
                    while not(valid_move):
                        computer_action = random.randint(0,5) # Raw 0-5 for reinforcement learning
                        computer_move = computer_action + 1 # Convert 0-5 to 1-6 for mancala usage
                        move = self.convert_move(computer_move,player_turn)
                        valid_move = self.valid_move(move, player_turn)
                        
                    # Inject the state into the agent for learning
                    mancala_agent.update_q(self.get_state(player_turn), computer_action)
                    
            # Check if move is valid prior to performing
            if not(self.valid_move(move, player_turn)):
                print("INVALID MOVE")
                continue
            
            # Perform assumed valid move and determine next to move
            player_turn, game_over = self.simulate_move(move, player_turn)
            
            # Update previous move
            previous_move = move
            
        # Assume mancala agent is player 2 for now
        mancala_agent.update_q(self.get_state(player=2), -1, self.pockets[13])
        
        print(mancala_agent.statemap)
        # Update agent for persistence
        self.mancala_agent = mancala_agent    
        
        # Draw final board and announce winner
        self.draw_board()
        winner = self.determine_winner()
        print("Winner: ", winner, "!!!")
            
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
        
        game_over = False
        
        empty_player_1 = sum(self.pockets[:6]) == 0
        empty_player_2 = sum(self.pockets[7:13]) == 0
        
        # If player 2 is empty, collect player 1's stones
        if empty_player_2:
            # Put remaining stones in player 2's mancala
            self.pockets[6] += sum(self.pockets[:6])
            self.pockets[:6] = [0]*6
            game_over = True
        
        # If player 1 is empty, collect player 1's stones
        if empty_player_1:
            # Put remaining stones in player 2's mancala
            self.pockets[13] += sum(self.pockets[7:13])
            self.pockets[7:13] = [0]*6
            game_over = True
        
        return game_over
    
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
        
        game_over = self.check_game_over()
        
        return next_player, game_over
    
    def draw_board(self, previous_move=-1):
        
        previous_move_marker = '__'
        
        # Create copy for modification
        pockets = list(self.pockets)
        
        # Convert the last board movement to a special marker to stand out
        # only if previous move is valid
        if previous_move >= 0:
            pockets[previous_move] = previous_move_marker
        
        # Unpack list of stones in each spot for readability
        pocket_1 = "{0:0>2}".format(pockets[0])
        pocket_2 = "{0:0>2}".format(pockets[1])
        pocket_3 = "{0:0>2}".format(pockets[2])
        pocket_4 = "{0:0>2}".format(pockets[3])
        pocket_5 = "{0:0>2}".format(pockets[4])
        pocket_6 = "{0:0>2}".format(pockets[5])
        mancala_1 = "{0:0>2}".format(pockets[6])
        
        pocket_7 = "{0:0>2}".format(pockets[7])
        pocket_8 = "{0:0>2}".format(pockets[8])
        pocket_9 = "{0:0>2}".format(pockets[9])
        pocket_10 = "{0:0>2}".format(pockets[10])
        pocket_11 = "{0:0>2}".format(pockets[11])
        pocket_12 = "{0:0>2}".format(pockets[12])
        mancala_2 = "{0:0>2}".format(pockets[13])
        
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
    
    def get_state(self, player):
        """ Returns the unique numeric state of the board for each player from
            the players own perspective. Mancala pockets not necessary but they
            can act as the reward to the computer at the end of the game.
        """
        
        assumed_max_stones_per_pocket = 16
        
        pocket_copy = list(self.pockets)
        
        # Flip the board interpretation if player 2
        if player == 1:
            relevant_pockets = pocket_copy[:6] + pocket_copy[7:13]
        else:
            relevant_pockets = pocket_copy[7:13] + pocket_copy[:6]
            
#        # Convert mancala base counting system to decimal for state
#        # Conversion similar to octal-2-decimal except the base number
#        # is max_stones+1
#        base_number = assumed_max_stones_per_pocket + 1
#        
#        # Use int64 due to massive number of combinations which may occur
#        # Should be optimized in the future to account for many situations
#        # which do not occur in practice (eg, 12 stones in all pockets)
#        multiplier_index = np.arange(len(relevant_pockets)-1,-1,-1, dtype='int64')
#        multipliers = base_number**multiplier_index
#        state_pieces = multipliers*np.array(relevant_pockets)
#        state = np.sum(state_pieces)
        
        return relevant_pockets