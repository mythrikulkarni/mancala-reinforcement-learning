# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 12:00:32 2017

@author: blamp
"""

import logging

class Agent:
    
    def __init__(self, alpha=0.5, gamma=0.5, max_actions=6 , load_agent=None):
        if load_agent is None:
            self.statemap = {}
            self.max_actions = max_actions
            self.previous_state = 0
            self.previous_action = 0
            self.alpha = alpha
            self.gamma = gamma
        else:
            self.statemap = {}
            self.max_actions = max_actions
            self.previous_state = 0
            self.previous_action = 0
            self.alpha = alpha
            self.gamma = gamma
            logging.warning('Missing code to load agent!')
            
    def update_q(self, current_state, current_move, reward=0):
        
        # Assume no reward unless explicitly specified

        # Convert state to a unique identifier
        hashed_current_state = hash(''.join(map(str, current_state)))
        hashed_previous_state = hash(''.join(map(str, self.previous_state)))
        
        current_q_set = self.statemap.get(hashed_current_state)
        previous_q_set = self.statemap.get(hashed_current_state)
        
        # Add new dictionary key/value pairs for new states seen
        if current_q_set is None:
            self.statemap[hashed_current_state] =  [0]*self.max_actions
            current_q_set = [0]*self.max_actions
        if previous_q_set is None:
            self.statemap[hashed_previous_state] =  [0]*self.max_actions
            
        # Q update formula
        q_s_a = self.statemap[hashed_previous_state][self.previous_action]
        q_s_a = q_s_a + self.alpha*(reward+self.gamma*max(current_q_set)-q_s_a)

        # Update Q
        self.statemap[hashed_previous_state][self.previous_action] = q_s_a

        # Update previous move (after converting from 1-6)
        self.previous_action = current_move-1

        return True