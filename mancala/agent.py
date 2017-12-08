# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 12:00:32 2017

@author: blamp
"""

import logging

class Agent:
    
    def __init__(self, max_actions=6 , load_agent=None):
        if load_agent is None:
            self.statemap = {}
            self.max_actions = max_actions
        else:
            self.statemap = {}
            self.max_actions = max_actions
            logging.warning('Missing code to load agent!')
            
    def update_q(self, state):
        
        # Convert state to a unique identifier
        hashed_state = hash(''.join(map(str, state)))
        
        q_set = self.statemap.get(hashed_state)
        
        # Add new dictionary key/value pairs for new states seen
        if q_set is None:
            self.statemap[hashed_state] =  [0]*self.max_actions