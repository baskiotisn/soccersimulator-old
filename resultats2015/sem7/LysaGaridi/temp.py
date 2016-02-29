# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

from soccersimulator import AbstractStrategy, Vector2D

class MaStrategy(AbstractStrategy):
    def __init__(self):
        AbstractStrategy.__init__(self, "Random")
        
        
    def compute_strategy(self, state, id_team, id_player):
        return SoccerAction()