# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 10:40:03 2017

@author: blamp
"""

import logging
from mancala import Mancala

def train_agent(n_games=1, games_per_checkpoint=1, model_save_path='model/mancala_agent.pkl'):
    
    environment = Mancala()
    
    while n_games>0:
        environment.play_game(reinforcement_learning=True)
        # Checkpoint
        if n_games%games_per_checkpoint == 0:
            environment.mancala_agent.save_agent(model_save_path)
            logging.info('Saved RL Agent Model!')
        n_games -= 1
        
    # Save final agent model
    environment.mancala_agent.save_agent(model_save_path)
        
    return environment


if __name__ == "__main__":
    environment = train_agent(n_games = 1000, games_per_checkpoint=100)
    
    