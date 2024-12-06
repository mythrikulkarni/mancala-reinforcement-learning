# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 12:00:32 2017

@author: blamp
"""

import random
import pickle

class Agent:
    
    def __init__(self, alpha=0.5, gamma=0.5, epsilon=0.9, max_actions=6, load_agent_path=None, reward=0):
        if load_agent_path:
            try:
                with open(load_agent_path, 'rb') as infile:
                    self.model = pickle.load(infile)
            except FileNotFoundError:
                self.statemap1 = {}
                self.statemap2 = {}
        else:
            self.statemap1 = {}
            self.statemap2 = {}
        
        # Parameters not saved in pkl file
        self.max_actions = max_actions
        self.previous_state = 0
        self.previous_action = 0
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.reward = reward


    def update_q(self, current_state, reward=0):
        # Convert state to a unique identifier
        hashed_current_state = tuple(current_state)
        hashed_previous_state = tuple(self.previous_state)
        
        if hashed_current_state not in self.statemap1:
            self.statemap1[hashed_current_state] = [0] * self.max_actions
            self.statemap2[hashed_current_state] = [0] * self.max_actions
        if hashed_previous_state not in self.statemap1:
            self.statemap1[hashed_previous_state] = [0] * self.max_actions
            self.statemap2[hashed_previous_state] = [0] * self.max_actions 
        
        if random.random() < 5:
            # Update statemap1
            max_action = self.statemap1[hashed_current_state].index(max(self.statemap1[hashed_current_state]))
            q_target = reward + self.gamma * self.statemap2[hashed_current_state][max_action]
            self.statemap1[hashed_previous_state][self.previous_action] += \
                self.alpha * (q_target - self.statemap1[hashed_previous_state][self.previous_action])
        else:
            # Update Q2
            max_action = self.statemap2[hashed_current_state].index(
                max(self.statemap2[hashed_current_state])
            )
            q_target = reward + self.gamma * self.statemap1[hashed_current_state][max_action]
            self.statemap2[hashed_previous_state][self.previous_action] += \
                self.alpha * (q_target - self.statemap2[hashed_previous_state][self.previous_action])

        self.previous_state = current_state
        return True
    
    def take_action(self, current_state):
        # Random action epsilon percent of the time
        hashed_current_state = tuple(current_state)
        if hashed_current_state not in self.statemap1:
            self.statemap1[hashed_current_state] = [0] * self.max_actions
            self.statemap2[hashed_current_state] = [0] * self.max_actions

        if random.random() < self.epsilon:
            action = random.randint(0, self.max_actions - 1)
        else:
            q_values = [q1 + q2 for q1, q2 in zip(self.statemap1[hashed_current_state], self.statemap2[hashed_current_state])]
            action = q_values.index(max(q_values))

        self.previous_action = action
        return action + 1
    
    def save_agent(self, save_path):
        with open(save_path, 'wb') as outfile:
            pickle.dump({'statemap1': self.statemap1, 'statemap2': self.statemap2}, outfile)