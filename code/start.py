# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 10:40:03 2017

@author: blamp
"""

from mancala import Mancala

# Script used for debugging and go-to place to interact with game

def main():
    environment = Mancala()
    environment.draw_board()
    environment.simulate_move(4,1); environment.draw_board()
    environment.simulate_move(0,1); environment.draw_board()
    return 0


if __name__ == "__main__":
    print("TODO: Add function definitions")
    main()