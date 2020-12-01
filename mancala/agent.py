# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 12:00:32 2017

@author: blamp
"""

import random
import pickle

class Agent:
    
    def __init__(self, alpha=0.5, gamma=0.5, epsilon=0.9, max_actions=6 , load_agent_path=None):
        try:
            with open(load_agent_path, 'rb') as infile:
                self.statemap = pickle.load(infile)
        except FileNotFoundError:
            print("No pretrained agent exists. Creating new agent")
            self.statemap = {}
        
        # Parameters not saved in pkl file
        self.max_actions = max_actions
        self.previous_state = 0
        self.previous_action = 0
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
            
    def update_q(self, current_state, reward=0):
        
        # Assume no reward unless explicitly specified

        # Convert state to a unique identifier
        hashed_current_state = hash(''.join(map(str, current_state)))
        hashed_previous_state = hash(''.join(map(str, self.previous_state)))
        
        current_q_set = self.statemap.get(hashed_current_state)
        previous_q_set = self.statemap.get(hashed_previous_state)
        
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

        # Track previous state for r=delayed reward assignment problem
        self.previous_state = current_state

        return True
    
    def take_action(self, current_state):
        
        # Random action 1-epsilon percent of the time
        if random.random()>self.epsilon:
            action = random.randint(0,5)
        else:
            # Greedy action taking
            hashed_current_state = hash(''.join(map(str, current_state)))
            current_q_set = self.statemap.get(hashed_current_state)
            if current_q_set is None:
                self.statemap[hashed_current_state] =  [0]*self.max_actions
                current_q_set = [0]*self.max_actions
            action = current_q_set.index(max(current_q_set)) # Argmax of Q
            
        self.previous_action = action
        
        # Convert computer randomness to appropriate action for mancala usage
        converted_action = action+1
        
        return converted_action
    
    def save_agent(self, save_path):
        with open(save_path, 'wb') as outfile:
            pickle.dump(self.statemap, outfile)