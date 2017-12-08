# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 10:40:03 2017

@author: blamp
"""

from mancala import Mancala

# Script used for debugging and go-to place to interact with game

def main(n_games=1):
    
    environment = Mancala()
    
    while n_games>0:
        environment.play_game(reinforcement_learning=True)
        n_games -= 1
        
    # Save agent
    environment.mancala_agent.save_agent('model/mancala_agent.pkl')
        
    return environment


if __name__ == "__main__":
    print("TODO: Add function definitions")
    environment = main(n_games = 1000000)
    
    # Output agent state mapping
    print(environment.mancala_agent.statemap)
    