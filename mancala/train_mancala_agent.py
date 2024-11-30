# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 10:40:03 2017

@author: blamp
"""

import os
import logging
import matplotlib.pyplot as plt
from mancala import Mancala
from agent import Agent
import pickle
import numpy as np

def train_agent(n_games=1, games_per_checkpoint=1, model_save_path='model/mancala_agent.pkl', initial_epsilon=1.0, min_epsilon = 0.05, epsilon_decay = 0.999, initial_alpha=0.3, min_alpha=0.01, alpha_decay=0.999, initial_temperature = 1.0, temperature_decay = 0.999, min_temperature =0.1):
    """
    Updated function to train Mancala agent with a combination of softmax and epsilon-greedy methods. 
    Added epsilon, alpha, and temperature decay for exploration and learning rate control
    """

    model_dir = os.path.dirname(model_save_path)
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    # If model already exists, expand on it, otherwise start fresh
    loaded_agent = Agent(load_agent_path = None, temperature = initial_temperature, epsilon=initial_epsilon, alpha = initial_alpha)
    environment = Mancala(loaded_agent)
    
    # Track game outcomes
    outcomes = []
    recent_outcomes = []
    games_won = 0
    total_games = n_games

    # Train agent for specific number of games
    while n_games>0:
        winner = environment.play_game(reinforcement_learning=True)
        
        # Assumes agent is Player 2
        if winner == "Player 2":
            games_won += 1
            recent_outcomes.append(1)
        elif winner == "Player 1":
            recent_outcomes.append(-1)
        else:
            recent_outcomes.append(0)

        # Update epsilon, alpha, and temperature    
        loaded_agent.update_epsilon(epsilon_decay, min_epsilon)
        loaded_agent.update_alpha(alpha_decay, min_alpha)
        loaded_agent.update_temperature(temperature_decay, min_temperature)
        
        # Checkpoint
        if n_games%games_per_checkpoint == 0:
            outcomes.append(np.mean(recent_outcomes[-games_per_checkpoint:]))
            environment.mancala_agent.save_agent(model_save_path)
            print('Remaining Games: ', n_games)
        n_games -= 1

    # Save final agent model
    environment.mancala_agent.save_agent(model_save_path)

    with open(model_save_path, "wb") as outfile:
        pickle.dump(loaded_agent.statemap, outfile)

    print("Win Rate: ", games_won / total_games)
    plt.plot(outcomes, label='Game Outcomes (Moving Average)')
    plt.title('Moving Average of Agent Performance)')
    plt.xlabel('Number of checkpoints (25k games is 1 checkpoint)')
    plt.ylabel('Average outcome')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
    return environment

if __name__ == "__main__":
    environment = train_agent(n_games = 1000000, games_per_checkpoint=25000)