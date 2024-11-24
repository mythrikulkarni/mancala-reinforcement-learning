# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 12:00:32 2017

@author: blamp
"""

import random
import pickle
import numpy as np
import os

class Agent:
    
    def __init__(self, alpha=0.5, gamma=0.5, temperature = 1.0, epsilon=0.9, max_actions=6 , load_agent_path=None):
        if load_agent_path and os.path.exists(load_agent_path):
            try:
                with open(load_agent_path, 'rb') as infile:
                    self.statemap = pickle.load(infile)
            except FileNotFoundError:
                print("No pretrained agent exists. Creating new agent")
                self.statemap = {}
        else:
            print("No pretrained agent exists. Creating new agent")
            self.statemap = {}

        self.temperature = temperature # Parameter to control exploration
        
        # Parameters not saved in pkl file
        self.max_actions = max_actions
        self.previous_state = 0
        self.previous_action = 0
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        self.q_table = {} # Initialize Q-table

        # Load agent if path is provided
        if load_agent_path:
            self.load_agent(load_agent_path)

    def softmax(self, q_values):
        # Compute softmax probabilities for Q-values
        q_values = q_values - np.max(q_values) # Prevent overflow
        exp_values = np.exp(q_values / self.temperature)
        probabilities = exp_values / np.sum(exp_values)
        return probabilities
            
    def update_q(self, current_state, reward=0):
        # Update Q value for previous state-action pair
        if self.previous_state is None or self.previous_action is None:
            self.previous_state = current_state
            return

        # Assume no reward unless explicitly specified

        # Convert state to a unique identifier
        hashed_current_state = hash(''.join(map(str, current_state)))
        hashed_previous_state = hash(''.join(map(str, self.previous_state)))
        
        # Initialize Q-values for new states if needed
        if hashed_current_state not in self.q_table:
            self.q_table[hashed_current_state] = np.zeros(self.max_actions)
        if hashed_previous_state not in self.q_table:
            self.q_table[hashed_previous_state] = np.zeros(self.max_actions)
        

        # Update Q-value using Q-learning formula
        prev_q_value = self.q_table[hashed_previous_state][self.previous_action]
        max_future_q = np.max(self.q_table[hashed_current_state])
        self.q_table[hashed_previous_state][self.previous_action] = (prev_q_value + self.alpha * (reward + self.gamma * max_future_q - prev_q_value))
        
        # Update previous state-action pair
        self.previous_state = current_state
    
    def take_action(self, current_state):

        # Choose an action using Softmax exploration
        hashed_state = hash(tuple(current_state))

        # Initialize Q-values for unseen states
        if hashed_state not in self.q_table:
            self.q_table[hashed_state] = np.zeros(self.max_actions)

        # Get Q-values for current state
        q_values = self.q_table[hashed_state]

        # Compute Softmax probabilities and sample action
        probabilities = self.softmax(q_values)
        action = np.random.choice(len(probabilities), p = probabilities)

        # Save chosen action for future updates
        self.previous_state = current_state
        self.previous_action = action

        return action + 1
    
    def save_agent(self, save_path):
        with open(save_path, 'wb') as outfile:
            pickle.dump(self.statemap, outfile)

    def update_temperature(self, decay_rate, min_temperature = 0.01):
        # Apply temperature decay over time
        self.temperature = max(self.temperature * decay_rate, min_temperature)

    def load_agent(self, path):
        with open(path, 'rb') as infile:
            self.q_table = pickle.load(infile)