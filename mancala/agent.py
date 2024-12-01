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
    
    def __init__(self, alpha=0.4, gamma=0.5, temperature = 1.0, epsilon=1.0, max_actions=6, load_agent_path=None, reward = 0):
        """
        Updated class to include temperature, epsilon, and alpha decay
        """

        if load_agent_path:
            try:
                with open(load_agent_path, 'rb') as infile:
                    self.model = pickle.load(infile)
            except FileNotFoundError:
                self.statemap = {}

        # Parameters not saved in pkl file
        self.temperature = temperature
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.max_actions = max_actions
        self.previous_state = 0
        self.previous_action = 0
        self.reward = reward

        if load_agent_path:
            self.load_agent(load_agent_path)

    def softmax(self, q_values):
        """
        Softmax function converts q-values to probabilities for action selection.
        """
        q_values = q_values - np.max(q_values)
        exp_values = np.exp(q_values / self.temperature) # Apply softmax w/ temperature scaling
        return exp_values / np.sum(exp_values) # Normalize for probability

    def epsilon_softmax_action(self,q_values):
        """
        Action is selected using combination of epsilon greedy & softmax approaches
        """
        if np.random.rand() < self.epsilon:
            return np.random.randint(len(q_values)) # Random action for exploration
        else:
            probabilities = self.softmax(q_values) # Softmax action selection
            return np.random.choice(len(probabilities), p = probabilities)

    def update_q(self, current_state, reward=0):
        # Assume no reward unless explicitly specified

        if self.previous_state is None or self.previous_action is None:
            self.previous_state = current_state
            return

        # Convert state to unique identifier
        hashed_current_state = hash(tuple(current_state))
        hashed_previous_state = hash(tuple(self.previous_state))

        # Initialize Q-values for unseen states
        if hashed_current_state not in self.statemap:
            self.statemap[hashed_current_state] = [0] * self.max_actions
        if hashed_previous_state not in self.statemap:
            self.statemap[hashed_previous_state] = [0] * self.max_actions

        # Q update 
        q_s_a = self.statemap[hashed_previous_state][self.previous_action]
        max_future_q = np.max(self.statemap[hashed_current_state])
        q_s_a = q_s_a + self.alpha*(reward+self.gamma* max_future_q - q_s_a)
        self.statemap[hashed_previous_state][self.previous_action] = q_s_a
        self.previous_state = current_state

        return True

    def take_action(self, current_state):
        hashed_state = hash(tuple(current_state)) # Hash state
        if hashed_state not in self.statemap:
            self.statemap[hashed_state] = [0] * self.max_actions # Initialize state if not seen before

        # Select action using epsilon-softmax function
        action = self.epsilon_softmax_action(self.statemap[hashed_state])
        self.previous_state = current_state
        
        self.previous_action = action

        # Convert computer randomness to appropriate action for mancala usage
        converted_action = action + 1
        return converted_action

    def save_agent(self, save_path):
        with open(save_path, 'wb') as outfile:
            pickle.dump(self.statemap, outfile)

    def update_temperature(self, temperature_decay, min_temperature):
        """
        Decay temperature after every move, ensuring it doesn't drop below min_temperature
        """
        self.temperature = max(self.temperature * temperature_decay, min_temperature)

    def update_epsilon(self, epsilon_decay, min_epsilon):
        """
        Decay epsilon after every move, ensuring it doesn't drop below min_epsilon
        """
        self.epsilon = max(self.epsilon * epsilon_decay, min_epsilon)

    def update_alpha(self, alpha_decay, min_alpha):
        """
        Decay alpha after every move, ensuring it doesn't drop below min_alpha
        """
        self.alpha = max(self.alpha * alpha_decay, min_alpha)

    def load_agent(self, path):
        with open(path, 'rb') as infile:
            self.statemap = pickle.load(infile)
