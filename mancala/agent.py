# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 12:00:32 2017

@author: blamp
"""

import random
import pickle

class Agent:
    
    def __init__(self, alpha=0.5, gamma=0.5, epsilon=0.9, max_actions=6 , load_agent_path=None):
        try:
            with open(load_agent_path, 'rb') as infile:
                self.statemap = pickle.load(infile)
        except FileNotFoundError:
            print("No pretrained agent exists. Creating new agent")
            self.statemap = {}
        
        # Parameters not saved in pkl file
        self.max_actions = max_actions
        self.previous_state = 0
        self.previous_action = 0
        self.previous_potential = 0
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    #create a function for the potential function
    def potential(self, state):
        #FIRST REWARD (stones in agent store - stones in opponent store)
        difference_in_stones_reward = sum(state[:self.max_actions // 2]) - sum(state[self.max_actions // 2:])
        #return difference_in_stones_reward

        #SECOND REWARD (reward for capturing stones)
        #more specifically, reward for adding stones to the agent's own store
        capture_marbles_reward = self.reward_for_addingmarblestostore(state) 

        #THIRD REWARD (reward for capturing stones)
        #more specifically, reward for getting stones from the opponent
        capture_stones_reward = self.reward_forgettingopponentsmarbles(state)

        #FOURTH REWARD (reward for getting extra turns, ie when the agent's marble lands in the agent's own store)
        extra_turns_reward = self.reward_for_extra_turns(state)
        
        #FIFTH REWARD (leaving the opponent with empty pits, agent can potentially get the opponent's marbles this way)
        #call reward_for_empty_pits(self, state)
        empty_pits_reward = self.reward_for_empty_pits(state)

        potential_value = 3.0 * difference_in_stones_reward + 3.0 * extra_turns_reward + 2.0 * capture_stones_reward + 1.0 * empty_pits_reward + 3.0 * capture_marbles_reward
        return potential_value

        #
    def reward_for_empty_pits(self, state):
        #empty pits that are left on the opponents side
        empty_pit_sum = 0
        for opponent_pit in state[self.max_actions // 2:]:
            if (opponent_pit == 0):
                empty_pit_sum = empty_pit_sum + 1
        return empty_pit_sum
    
    def reward_for_addingmarblestostore(self, state):
        agent_store = (self.max_actions // 2 - 1)
        marbles_in_store_before = self.previous_state[agent_store]
        marbles_in_store_now = state[agent_store]
        return (marbles_in_store_now - marbles_in_store_before)
    
    def reward_for_gettingopponentmarbles(self, state):
        opponent_pitbefore =  sum(self.previous_state[self.max_actions // 2: self.max_actions - 1])
        opponent_pitafter =  sum(state[self.max_actions // 2: self.max_actions - 1])
        if (opponent_pitbefore - opponent_pitafter > 0):
            return (opponent_pitbefore - opponent_pitafter)
        else:
            return 0
        
    def reward_for_extra_turns(self, state):
        #agent gets an extra turn when the last marble lands in its own store
        nummarbles = state[self.previous_action] #number of marble in the pit that was chosen for the previous turn
        landing_pit = (self.previous_action + nummarbles) % len(state) #accounting for the counterclockwise distribution of stones

        agent_store = (self.max_actions // 2 - 1)
        if (landing_pit == agent_store):
            return 1
        else:
            return 0




    def update_q(self, current_state, reward=0):
        
        # Assume no reward unless explicitly specified

        # Convert state to a unique identifier
        hashed_current_state = hash(''.join(map(str, current_state)))
        hashed_previous_state = hash(''.join(map(str, self.previous_state)))
        
        current_q_set = self.statemap.get(hashed_current_state)
        previous_q_set = self.statemap.get(hashed_previous_state)
        
        # Add new dictionary key/value pairs for new states seen
        if current_q_set is None:
            self.statemap[hashed_current_state] =  [0]*self.max_actions
            current_q_set = [0]*self.max_actions
        if previous_q_set is None:
            self.statemap[hashed_previous_state] =  [0]*self.max_actions

        #include the potential function rewards
        currentpotential = self.potential(current_state)
        rewardshaping = self.gamma * currentpotential - self.previous_potential

        # Q update formula
        q_s_a = self.statemap[hashed_previous_state][self.previous_action]
        q_s_a = q_s_a + self.alpha*(reward + rewardshaping + self.gamma * max(current_q_set) - q_s_a)

        # Update Q
        self.statemap[hashed_previous_state][self.previous_action] = q_s_a

        # Track previous state for r=delayed reward assignment problem
        self.previous_state = current_state
        self.previous_potential = currentpotential

        return True
    
    def take_action(self, current_state):
        
        # Random action 1-epsilon percent of the time
        if random.random()>self.epsilon:
            action = random.randint(0,5)
        else:
            # Greedy action taking
            hashed_current_state = hash(''.join(map(str, current_state)))
            current_q_set = self.statemap.get(hashed_current_state)
            if current_q_set is None:
                self.statemap[hashed_current_state] =  [0]*self.max_actions
                current_q_set = [0]*self.max_actions
            action = current_q_set.index(max(current_q_set)) # Argmax of Q
            
        self.previous_action = action
        
        # Convert computer randomness to appropriate action for mancala usage
        converted_action = action+1
        
        return converted_action
    
    def save_agent(self, save_path):
        with open(save_path, 'wb') as outfile:
            pickle.dump(self.statemap, outfile)
