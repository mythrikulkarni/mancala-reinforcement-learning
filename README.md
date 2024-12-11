## Mancala Environment with Reinforcement Learning Bolt-On
This repo contains code related to simulating a game of Mancala, including a more advanced implementation of Q-learning that uses softmax + epsilon-greedy with epsilon and alpha decay. Every branch contains a specific person's adjustment to the baseline code (with the new reward system); please see the Contributions section (section 7) of our report to determine which branches correspond to which person. The master branch contains our final model, all figures/plots related to it, and our slides from the presentation.

## Group Names:
Angelina Cottone,
Nick Gomez,
Harris Habib,
Mythri Kulkarni,
Aatish Lobo,
Andrew Ortega,
Shriya Rudrashetty,
Alyssa Ann Toledo

### How to Play:

- Run train_mancala_agent.py to train the RL algorithm
- Run play_mancala.py to play a game of mancala

### Current Features
- Ability to play Mancala human vs human
- Ability to play Mancala human vs trained RL algorithm
- More Advanced Q Learning Implementation
- Model Saving/Loading to Iteratively Train and Play Against
