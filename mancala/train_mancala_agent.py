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

def train_agent(n_games=1, games_per_checkpoint=1, model_save_path='model/mancala_agent.pkl', initial_temperature = 1.0, temperature_decay=0.99):
    # Ensure model directory exists, create if not
    model_dir = os.path.dirname(model_save_path)
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    # If model already exists, expand on it, otherwise start fresh
    loaded_agent = Agent(load_agent_path = None, temperature=initial_temperature)
    environment = Mancala(loaded_agent)

    results = []
    temperatures = []
    current_temperature = initial_temperature

    while n_games>0:
        # Update temperature
        loaded_agent.update_temperature(temperature_decay)
        environment.play_game(reinforcement_learning=True)

        # Track game results
        winner = environment.determine_winner()
        if winner == "Player 2":
            results.append(1)
        elif winner == "Player 1":
            results.append(-1)
        else:
            results.append(0)

        # Track temperature
        temperatures.append(loaded_agent.temperature)

        # Save model at checkpoints
        if n_games%games_per_checkpoint == 0:
            environment.mancala_agent.save_agent(model_save_path)
            logging.info('Saved RL Agent Model!')
            print('Remaining Games: ', n_games)

        if np.mean(results[-100:]) > 0.8:
            temperature_decay = max(temperature_decay * 0.98, 0.9)

        # Temperature decay
        current_temperature *= temperature_decay
        n_games -= 1
        
    # Save final agent model
    environment.mancala_agent.save_agent(model_save_path)

    # Plots results
    plot_all(results, initial_temp=initial_temperature, decay_rate=temperature_decay, n_games=n_games, temperatures=temperatures)

    # Save Q-table
    with open(model_save_path, "wb") as outfile:
        pickle.dump(loaded_agent.q_table, outfile)
        
    return environment

def plot_all(results, initial_temp, decay_rate, n_games, temperatures, interval=5000, moving_avg_window=5000, win_rate_window = 5000):

    # Sample results for plotting at intervals
    sampled_results = results[::interval]
    sampled_games = list(range(interval, len(results) + 1, interval))

    # Moving average
    moving_avg = [np.mean(results[max(0, i - moving_avg_window + 1): i + 1]) for i in range(len(results))]


    # Win, loss, draw counts
    win_count = results.count(1)
    loss_count = results.count(-1)
    draw_count = results.count(0)

    # Cumulative reward calculation
    cumulative_reward = np.cumsum(results)

    # Plot for agent performance over time
    print("Plotting Agent Performance Over Time...")
    plt.figure(figsize=(8, 6))
    plt.plot(sampled_games, sampled_results, label="Game Results", marker="o")
    plt.xlabel("Game #")
    plt.ylabel("Result (Win = 1, Loss = -1)")
    plt.title("Agent Performance Over Time")
    plt.axhline(y=0, color='gray', linestyle='--', label="Draw")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Win/Loss/Draw Counts
    print("Plotting Win/Loss/Draw Counts")
    plt.figure(figsize=(8, 6))
    plt.pie([win_count, loss_count, draw_count], labels=['Wins', 'Losses', 'Draws'],
            autopct='%1.1f%%', startangle=90, colors=['green', 'red', 'gray'])
    plt.title("Win/Loss/Draw Distribution")
    plt.show()

    # Plot for moving average
    print("Plotting Moving Average Over Time...")
    plt.figure(figsize=(8, 6))
    plt.plot(range(len(moving_avg)), moving_avg, label=f"Moving Average (window={moving_avg_window})", color="orange", linewidth=2)
    plt.xlabel("Game #")
    plt.ylabel("Moving Average (Win/Loss)")
    plt.title("Agent Performance (Moving Average)")
    plt.axhline(y=0, color='gray', linestyle='--', label="Draw")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plot cumulative rewards
    print("Plotting Cumulative Rewards Over Time...")
    plt.figure(figsize=(8, 6))
    plt.plot(range(len(results)), cumulative_reward, label="Cumulative Reward", color="blue")
    plt.xlabel("Game #")
    plt.ylabel("Cumulative Reward")
    plt.title("Cumulative Reward Over Time")
    plt.axhline(y=0, color='gray', linestyle='--', label="Baseline")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    environment = train_agent(n_games = 1000000, games_per_checkpoint=25000)