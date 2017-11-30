# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 16:22:50 2017

@author: blamp
"""

import unittest
from mancala.mancala import Mancala

class FinalMove(unittest.TestCase):
    
    def setUp(self):
        pass
    
    # Bug seen at end of game when capture and game over occur in same move
    def test_bug1(self):
        environment = Mancala()
        environment.pockets = [1,0,1,0,0,0,22,0,0,1,0,0,0,23]
        environment.simulate_move(9,2)
        expected_result = [0,0,0,0,0,0,23,0,0,0,0,0,0,25]
        
        self.assertEqual(expected_result, environment.pockets)
        
if __name__ == '__main__':
    unittest.main()