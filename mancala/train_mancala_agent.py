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

def train_agent(n_games=1, games_per_checkpoint=1, model_save_path='model/mancala_agent.pkl'):

    # If model already exists, expand on it, otherwise start fresh
    loaded_agent = Agent(load_agent_path = model_save_path)
    environment = Mancala(loaded_agent)
    outcomes = []
    games_won = 0
    total_games = n_games

    while n_games>0:
        winner = environment.play_game(reinforcement_learning=True)

        if (winner == "Player 2"):
            outcomes.append(1)
            games_won += 1
        elif winner == "Player 1":
            outcomes.append(-1)
        else:
            outcomes.append(0)





        # Checkpoint
        if n_games%games_per_checkpoint == 0:
            environment.mancala_agent.save_agent(model_save_path)
            logging.info('Saved RL Agent Model!')
            print('Remaining Games: ', n_games)
        n_games -= 1

    # Save final agent model
    environment.mancala_agent.save_agent(model_save_path)
    print("Win Rate: ", games_won / total_games)

    plt.plot(outcomes, label='Game Outcomes')
    plt.title('Agent Performance over time (Every 10 games)')
    plt.xlabel('Games Played')
    plt.ylabel('Game outcome (1 = win, 0 = Draw, -1 = Loss)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return environment


if __name__ == "__main__":
    environment = train_agent(n_games = 1000, games_per_checkpoint=10)

