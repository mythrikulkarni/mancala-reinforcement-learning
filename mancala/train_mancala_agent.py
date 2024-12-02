# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 10:40:03 2017

@author: blamp
"""

import os
import logging
from mancala import Mancala
from agent import Agent
import matplotlib.pyplot as plt
import numpy as np

def train_agent(n_games=1, games_per_checkpoint=1, model_save_path='model/mancala_agent.pkl'):
    runs = 5 #for 5 model iterations
    run_outcomes = []
    tot_games = n_games
    for run in range(1,6):
        loaded_agent = Agent(load_agent_path = model_save_path)
        environment = Mancala(loaded_agent)
        outcomes = []
        latest_outcomes = []
        num_wins = 0
        n_games = tot_games
        while n_games>0:
            environment.play_game(reinforcement_learning=True)
            if environment.determine_winner() == "Player 1": #lose
                latest_outcomes.append(-1)
            elif environment.determine_winner() == "Player 2": #win
                latest_outcomes.append(1)
                num_wins += 1
            else:
                latest_outcomes.append(0) #draw
       
        # Checkpoint
            if n_games%games_per_checkpoint == 0:
                outcomes.append(np.mean(latest_outcomes[-games_per_checkpoint:]))
                environment.mancala_agent.save_agent(model_save_path)
                logging.info('Saved RL Agent Model!')
                print('Remaining Games: ', n_games)
            n_games -= 1
        plt.figure()
        plt.plot(outcomes, label = "Game Outcomes - Moving Average")
        plt.title(f"Run {run} - Moving Average of Agent Performance")
        plt.xlabel("Number of Checkpoints - {} games per checkpoint".format(games_per_checkpoint))
        plt.ylabel("Average Outcome")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()
        run_outcomes.append(outcomes)
    run_outcomes = np.array(run_outcomes)
    mean_outcomes = np.mean(run_outcomes, axis=0)
    stand_outcomes = np.std(run_outcomes, axis = 0)
    plt.figure()
    plt.plot(mean_outcomes, label = "Mean Outcome Across Runs")
    plt.fill_between(range(len(mean_outcomes)), mean_outcomes - stand_outcomes, mean_outcomes + stand_outcomes, color = 'gray', alpha = 0.3, label = "Standard Deviation")
    plt.title("Consistency of Agent Performance - 5 Runs")
    plt.xlabel('Number of Checkpoints ({} games per checkpoint)'.format(games_per_checkpoint))
    plt.ylabel('Average Outcome')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()    
    # Save final agent model
    environment.mancala_agent.save_agent(model_save_path)
    return environment


if __name__ == "__main__":
    environment = train_agent(n_games = 1000000, games_per_checkpoint=25000)


if __name__ == "__main__":
    environment = train_agent(n_games = 1000000, games_per_checkpoint=25000)
    
    
