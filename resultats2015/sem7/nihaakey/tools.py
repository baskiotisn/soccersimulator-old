# -*- coding: utf-8 -*-
from soccersimulator import Vector2D, SoccerAction
from  soccersimulator.settings import *

def lgoal_position():
	return Vector2D(GAME_WIDTH-GAME_WIDTH,GAME_HEIGHT/2)

def lgoal_lcage_position():
	return Vector2D(GAME_WIDTH-GAME_WIDTH,GAME_HEIGHT/2+GAME_GOAL_HEIGHT/2)

def lgoal_rcage_position():
	return Vector2D(GAME_WIDTH-GAME_WIDTH,GAME_HEIGHT/2-GAME_GOAL_HEIGHT/2)

def rgoal_position():
	return Vector2D(GAME_WIDTH,GAME_HEIGHT/2)

def rgoal_lcage_position():
	return Vector2D(GAME_WIDTH,GAME_HEIGHT/2-GAME_GOAL_HEIGHT)

def rgoal_rcage_position():
	return Vector2D(GAME_WIDTH,GAME_HEIGHT/2+GAME_GOAL_HEIGHT)
