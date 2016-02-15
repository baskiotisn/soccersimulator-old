import soccersimulator
import math
import random
from  soccersimulator import settings
from soccersimulator import BaseStrategy, SoccerAction 
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player , SoccerTournament
from Strategie import *
from Team import *
class RandomStrategy (BaseStrategy):
	def __init__ (self) :
	   BaseStrategy.__init__(self, "Random" )
	def compute_strategy (self, state, id_team, id_player):
	   return SoccerAction(Vector2D.create_random(),
			       Vector2D.create_random())


        



match = SoccerMatch(team1,team2,2000)
soccersimulator.show(match)

