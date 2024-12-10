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

def train_agent(n_games=1, games_per_checkpoint=1, model_save_dir='model/', base_filename = 'Mancala_agent', plot_save_folder='moving_averages_softmax', initial_epsilon=1.0, min_epsilon = 0.05, epsilon_decay = 0.999, initial_alpha=0.4, min_alpha=0.01, alpha_decay=0.999, initial_temperature = 1.0, temperature_decay = 0.999, min_temperature =0.1):
    """
    Updated function to train Mancala agent with a combination of softmax and epsilon-greedy methods. 
    Added epsilon, alpha, and temperature decay for exploration and learning rate control
    """

    os.makedirs(plot_save_folder, exist_ok=True)
    
    total_runs = 5
    outcomes_all_runs = []  # To store outcomes from all runs for consistency analysis

    total_games = n_games

    for run in range(1, 6):  # Run 5 times for fresh agents
        print(f"Starting Run {run}/5")

        # Define unique save path for this run
        model_save_path = os.path.join(model_save_dir, f"{base_filename}_{run}.pkl")
        model_dir = os.path.dirname(model_save_path)
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

        # Start with a fresh agent for each run
        loaded_agent = Agent(load_agent_path = None, temperature = initial_temperature, epsilon=initial_epsilon, alpha = initial_alpha)
        environment = Mancala(loaded_agent)

        outcomes = []
        recent_outcomes = []
        games_won = 0
        n_games = total_games # Gets reset every run

        while n_games > 0:
            winner = environment.play_game(reinforcement_learning=True)

            if winner == "Player 2":
                recent_outcomes.append(1)
                games_won += 1
            elif winner == "Player 1":
                recent_outcomes.append(-1)
            else:
                recent_outcomes.append(0)

            loaded_agent.update_epsilon(epsilon_decay, min_epsilon)
            loaded_agent.update_alpha(alpha_decay, min_alpha)
            loaded_agent.update_temperature(temperature_decay, min_temperature)

            # Checkpoint
            if n_games % games_per_checkpoint == 0:
                outcomes.append(np.mean(recent_outcomes[-games_per_checkpoint:]))
                environment.mancala_agent.save_agent(model_save_path)
                print(f"Checkpoint saved. Remaining games: {n_games}")
            n_games -= 1

        # Save the final agent for this run
        environment.mancala_agent.save_agent(model_save_path)
        print("Win Rate for Run {}: {:.2f}%".format(run, (games_won / total_games) * 100))
        plt.figure()
        plt.plot(outcomes, label='Game Outcomes (Moving Average)')
        plt.title(f'Run {run} - Moving Average of Agent Performance')
        plt.xlabel('Number of Checkpoints ({} games per checkpoint)'.format(games_per_checkpoint))
        plt.ylabel('Average Outcome')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plot_path = os.path.join(plot_save_folder, f'moving_average_run_{run}.png')
        plt.savefig(plot_path)
        plt.close()
        print(f"Plot saved to {plot_path}")

        outcomes_all_runs.append(outcomes)  # Store this run's outcomes

    # Calculate and plot the standard deviation
    outcomes_all_runs = np.array(outcomes_all_runs)
    mean_outcomes = np.mean(outcomes_all_runs, axis=0)
    std_outcomes = np.std(outcomes_all_runs, axis=0)

    plt.figure()
    plt.plot(mean_outcomes, label='Mean Outcome Across Runs')
    plt.fill_between(range(len(mean_outcomes)),
                     mean_outcomes - std_outcomes,
                     mean_outcomes + std_outcomes,
                     color='gray', alpha=0.3, label='Standard Deviation')
    plt.title('Consistency of Agent Performance (5 Runs)')
    plt.xlabel('Number of Checkpoints ({} games per checkpoint)'.format(games_per_checkpoint))
    plt.ylabel('Average Outcome')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    consistency_plot_path = os.path.join(plot_save_folder, 'consistency_plot.png')
    plt.savefig(consistency_plot_path)
    plt.close()
    print(f"Consistency plot saved to {consistency_plot_path}")

if __name__ == "__main__":
    environment = train_agent(n_games = 1000000, games_per_checkpoint=25000)
