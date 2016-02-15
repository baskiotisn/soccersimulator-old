# -*- coding: utf-8 -*-

from soccersimulator import BaseStrategy
from PlayerStateDecorator import *
"""Stratégie pour le joueur"""


class MaStrategy(BaseStrategy):
	def __init__(self):
		BaseStrategy.__init__(self, "Random")

	def compute_strategy(self,state,id_team,id_player):
		mystate = PlayerStateDecorator(state,id_team,id_player)
		return attaquant(mystate)



"""Stratégie pour le goal team1"""


class MaStrategyGoal(BaseStrategy):
	def __init__(self):
		BaseStrategy.__init__(self, "Goal")

	def compute_strategy(self,state,id_team,id_player):
		mystate = PlayerStateDecorator(state,id_team,id_player)
		return goal_vers_ball(mystate)
