# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 10:40:03 2017

@author: blamp
"""

import logging
from mancala import Mancala
from agent import Agent

# Script used for debugging and go-to place to interact with game

def play_game(model_path='model/mancala_agent.pkl'):
    
    loaded_agent = Agent(load_agent_path = model_path)
    environment = Mancala(loaded_agent)
    environment.play_game()
    
    return 0


if __name__ == "__main__":
    print("TODO: Add function definitions")
    play_game()
    
    