import os
import logging
import matplotlib.pyplot as plt
from mancala import Mancala
from agent import Agent
import numpy as np

def train_agent(n_games=1, games_per_checkpoint=1, model_save_dir='model/', base_filename = 'Mancala_agent', plot_save_folder='moving_averages_epsilon_decay'):

    # Ensure the save folder exists
    os.makedirs(plot_save_folder, exist_ok=True)

    total_runs = 5
    outcomes_all_runs = []  # To store outcomes from all runs for consistency analysis

    # Ensure the model directory exists
    if not os.path.exists(model_save_dir):
        os.makedirs(model_save_dir)

    total_games = n_games

    for run in range(1, 6):  # Run 5 times for fresh agents
        print(f"Starting Run {run}/5")

        # Define unique save path for this run
        model_save_path = os.path.join(model_save_dir, f"{base_filename}_{run}.pkl")

        # Start with a fresh agent for each run
        loaded_agent = Agent()

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
    train_agent(n_games=1000000, games_per_checkpoint=25000)
