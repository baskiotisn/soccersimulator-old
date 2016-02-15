# -*- coding: utf-8 -*-
 
import soccersimulator, soccersimulator.settings
from soccersimulator import BaseStrategy, Vector2D, SoccerAction, SoccerMatch, SoccerTeam, Player, SoccerTournament, settings
import math




class PlayerStateDecorator:
	def __init__(self, state, idteam, idplayer): 
		self.state = state
		self.idteam = idteam
		self.idplayer = idplayer
	
# renvoie position du joueur
	@property
	def position(self):
		return self.state.player_state(self.idteam, self.idplayer).position
	
# renvoie position de la balle
	@property
	def ball_position(self):
		return self.state.ball.position

# renvoie distance entre la balle et le joueur
	@property
	def distance_ball(self):
		return self.state.ball_position.distance(self.position)
	
# renvoie la position des buts adversaire
	@property
	def goal_adv(self):
		if (self.idteam == 1):
			return Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2)
		return Vector2D(0,settings.GAME_HEIGHT/2)
	
	@property
	def mes_goal(self):
		if (self.idteam == 1):
			return Vector2D(0,settings.GAME_HEIGHT/2)
		return Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2)

# shoot que si la distance ball/joueur 
#	def distance 

	
# le joueur shoot avec une accélération nulle
	def shoot(self,p):
#		return SoccerAction(Vector2D(),0)
#		return SoccerAction(Vector2D(),Vector2D(0,50))
#		return SoccerAction(Vector2D(),Vector2D(50,0))
#		return SoccerAction(Vector2D(),Vector2D(50,50))


		return SoccerAction(Vector2D(),self.position-p)

# le joueur accélère avec un shoot nul
	def aller(self,p):
		return SoccerAction(p-self.position,Vector2D())


# mystate = PlayerStateDecorator(state,idteam,idplayer)


# shoot vers les buts adverses

def shoot_but(me):
	return me.shoot(me.goal_adv)

def attaquant(me):
	return me.aller(me.ball_position)+me.shoot(me.goal_adv)



def goal_vers_ball(me):
	if (me.position - me.ball_position < settings.GAME_WIDTH/4):
		return me.aller(me.ball_position)
	return me.aller(me.mes_goal)

def goal_pousse_ball(me):
	return me.shoot(me.goal_adv)

















