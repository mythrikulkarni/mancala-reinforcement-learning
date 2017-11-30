# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 10:40:03 2017

@author: blamp
"""

from mancala.mancala import Mancala

# Script used for debugging and go-to place to interact with game

def main():
    environment = Mancala()
    environment.play_game()
    return environment


if __name__ == "__main__":
    print("TODO: Add function definitions")
    environment = main()