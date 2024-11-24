# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 10:40:03 2017

@author: blamp
"""

from mancala import Mancala
from agent import Agent
import os

def play_game():
    # Create model path if doesn't exist
    base_cwd = os.getcwd()
    model_dir = base_cwd + "/model"
    if not os.path.exists(model_dir):
        os.mkdir(model_dir)
    model_path = model_dir + "/mancala_agent.pkl"

    loaded_agent = Agent(load_agent_path = model_path)
    environment = Mancala(loaded_agent)
    environment.play_game()
    return 0

if __name__ == "__main__":
    play_game()