# -*- coding: utf-8 -*-
from random import *
import soccersimulator
from tools import *
from  soccersimulator.settings import *
from soccersimulator import BaseStrategy, KeyboardStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
import math

def miroir_v(v):
	return Vector2D(-v.x,v.y)
def miroir_p(v):
	return Vector2D(GAME_WIDTH-v.x,v.y)

def miroir(state,idteam):
	if idteam == 1:
		return state
	res = state.copy()
	res.ball.position = miroir_p(state.ball.position)
	res.ball.vitesse = miroir_v(state.ball.vitesse)
	for (idt,idp) in state.players:
		res.player_state(idt,idp).position = miroir_p(state.player_state(idt,idp).position)
		res.player_state(idt,idp).vitesse = miroir_v(state.player_state(idt,idp).vitesse)
	return res

class PlayerStateDecorator:
	def __init__(self, state, id_team, id_player):
		self.state = state
		self.id_team = id_team
		self.id_player = id_player
			
	@property
	def my_position(self):
		#ma position
		return self.state.player_state(self.id_team,self.id_player).position
			
	def position(self,idt,idp):
		#position du joueur idp de la team idt
		return self.state.player_state(idt,idp).position
		
	@property
	def ball_position(self):	
		#position de la balle
		return self.state.ball.position
	
	@property
	def my_vitesse(self):
		#ma vitesse
		return self.state.player_state(self.id_team,self.id_player).vitesse	
	
	def vitesse(self,idt,idp):
		#vitesse du joueur idp de la team idt
		return self.state.player_state(idt,idp).vitesse
		
	@property
	def ball_vitesse(self):
		#vitesse de la balle
		return self.state.ball.vitesse
		
	def aller(self,p):
		# aller au point p
		return p-self.my_position
		
	def aller_y(self,p):
		# aller au point p dans l'axe y seulement
		return Vector2D(0,p.y)-Vector2D(0,self.my_position.y)
		
	def aller_x(self,p):
		# aller au point p dans l'axe x seulement	
		return Vector2D(p.x,0)-Vector2D(self.my_position.x,0)
		
	@property
	def aller_ball(self):
		# aller vers la balle	
		return self.ball_position-self.my_position
		
	@property	
	def aller_y_ball(self):
		# aller vers la balle dans l'axe y seulement
		return self.aller_y(self.ball_position)
		
	@property	
	def aller_x_ball(self):
		# aller vers la balle dans l'axe x seulement
		return self.aller_x(self.ball_position)
		
	@property
	def get_my_idteam(self):
		# ma team
		return self.id_team
		
	@property
	def get_idteam_adv(self):
		# team adverse
		if self.id_team ==1:
			return 2
		else:
			return 1
			
	@property
	def nb_teamplayer(self):
		#nombre de joueur de ma team
		i=0
		for (idt,idp) in self.state.players:
			if idt != self.id_team:
				i+=1
		return i
		
	def my_distance(self,p):
		# ma distance au point p
		return self.my_position.distance(p)
		
	@property
	def my_distance_ball(self):
		# ma distance a la balle
		return self.my_position.distance(self.ball_position)
		
	def my_distance_adv(self,idt,idp):
		# ma distance a l'adversaire idp de la team idt
		return self.my_position.distance(self.position(idt,idp))	
		
	@property
	def my_distance_adv_plus_proche(self):
		# ma distance a l'adversaire le plus proche de moi 
		L=[]
		for (idt,idp) in self.state.players:
			if idt != self.id_team:
				L.append(self.my_distance_adv(idt,idp))
		return min(L)
		
	@property	
	def my_adv_plus_proche(self):
		# adversaire le plus proche de moi
		L=[]
		Lbis=[]
		for (idt,idp) in self.state.players:
			if idt != self.id_team:
				L.append(self.my_distance_adv(idt,idp))
				Lbis.append(idp)
		return Lbis[L.index(min(L))]
		
	@property
	def adv_plus_proche_ball(self):
		# adversaire le plus proche de la balle
		L=[]
		Lbis=[]
		for (idt,idp) in self.state.players:
			if idt != self.id_team:
				L.append(self.distance_ball(idt,idp))
				Lbis.append(idp)
		return Lbis[L.index(min(L))]
		
	@property
	def my_goal(self):
		# mes buts
		return lgoal_position()
		
	@property
	def adv_goal(self):
		# les buts adverse
		return rgoal_position()
		
	@property
	def my_distance_my_goal_position(self):
		# ma distance a la position de mes buts
		return self.my_position.distance(lgoal_position())
		
	@property
	def my_distance_adv_goal_position(self):
		# ma distance a la position des buts adverse
		return self.my_position.distance(rgoal_position())
	
	def distance_ball(self,idt,idp):
		# la distance entre la balle et le joueur idp de  la team idt
		return self.position(idt,idp).distance(self.ball_position)
		
	@property	
	def distance_adv_plus_proche_ball(self):
		# la distance entre la balle et le joueur  adversaire le plus proche de la balle
		L=[]
		for (idt,idp) in self.state.players:
			if idt != self.id_team:
				L.append(self.distance_ball(idt,idp))
		return min(L)
		
	def shoot(self,p):
		# tirer vers la position p
		return p-self.my_position
	
	@property	
	def peut_shoot(self):
		# le joueur peut tirer
		if self.my_distance_ball < PLAYER_RADIUS + BALL_RADIUS:
			return True
		else:
			return False

	@property			
	def adv_peut_shoot(self):
		# adversaire le  plus proche de la balle peut tirer
		if self.distance_adv_plus_proche_ball < PLAYER_RADIUS + BALL_RADIUS:
			return True
		else:
			return False

	@property			
	def a_la_balle(self):
		# si le joueur a la balle		
		if self.my_distance_ball < PLAYER_RADIUS - BALL_RADIUS:
			return True
		else:
			return False

	@property
	def team_a_la_balle(self):
		# si une team a la balle (adversaire= -1, personne =0, ma team =1)		
		if self.a_la_balle == True:
			if self.get_my_idteam == 1:
					return 1
			else:
					return -1
		else:
			return 0

	@property			
	def my_position_relative_ball(self):
		# ma position relative / balle (1)
		return math.sqrt(self.ball_position-self.my_position.dot(self.ball_position-self.my_position))

	@property		
	def my_vitesse_relative_ball(self):
		# ma vitesse relative / balle (2)
		return math.sqrt(self.ball_vitesse-self.my_vitesse.dot(self.ball_vitesse-self.my_vitesse))

	@property		
	def position_interception_ball(self):
		#position interception de la balle avec (1) et (2)
		if self.my_position_relative_ball != 0 and self.my_vitesse_relative_ball != 0:
			time=my_position_relative_ball/self.my_vitesse_relative_ball		
			return self.ball_position+self.ball_vitesse*time
		return 0
		
	def my_position_relative(self,idt,idp):
		# ma position relative / joueur idp de la team idt(1)
		return math.sqrt(self.position(idt,idp)-self.my_position.dot(self.position(idt,idp)-self.my_position))
		
	def my_vitesse_relative(self,idt,idp):
		# ma vitesse relative / joueur  idp de la team idt(2)
		return math.sqrt(self.vitesse(idt,idp)-self.my_vitesse.dot(self.vitesse(idt,idp)-self.my_vitesse))

	def position_interception(self,idt,idp):
		#position interception du joueur adv le plus proche avec (1) et (2)
		if self.my_position_relative(idt,idp) != 0 and self.my_vitesse_relative(idt,idp) != 0:
			time=self.my_position_relative(idt,idp)/self.my_vitesse_relative(idt,idp)
			return self.ball_position+self.ball_vitesse*time
		return 0
	
	def regardez_ball(self):
		#change l'angle 
		return math.degrees(math.atan2(-mystate.ball_position.y+mystate.my_position.y, mystate.ball_position.x-mystate.my_position.x))
	def __getattr__(self,name):
		return getattr(self.state,name)

class StrategyG(BaseStrategy):
	def __init__(self):
		BaseStrategy.__init__(self, "Goal")
	def compute_strategy(self, state, id_team, id_player):
		mystate = PlayerStateDecorator(miroir(state,id_team), id_team, id_player)
		return Goal(mystate)

class StrategyD(BaseStrategy):
	def __init__(self):
		BaseStrategy.__init__(self, "Defenseur")
	def compute_strategy(self, state, id_team, id_player):
		mystate = PlayerStateDecorator(miroir(state,id_team), id_team, id_player)
		return Defenseur(mystate)

class StrategyA(BaseStrategy):
	def __init__(self):
		BaseStrategy.__init__(self, "Attaquant")
	def compute_strategy(self, state, id_team, id_player):
		mystate = PlayerStateDecorator(miroir(state,id_team), id_team, id_player)
		return Attaquant(mystate)
		
class StrategyP(BaseStrategy):
	def __init__(self):
		BaseStrategy.__init__(self, "Polyvalent")
	def compute_strategy(self, state, id_team, id_player):
		mystate = PlayerStateDecorator(miroir(state,id_team), id_team, id_player)	
		return Polyvalent(mystate)

class StrategyR(BaseStrategy):
	def __init__(self):
		BaseStrategy.__init__(self, "Renvoyeur")
	def compute_strategy(self, state, id_team, id_player):
		mystate = PlayerStateDecorator(miroir(state,id_team), id_team, id_player)
		return Renvoyeur(mystate)
						
class StrategyF(BaseStrategy):
	def __init__(self):
		BaseStrategy.__init__(self, "Fonceur")
	def compute_strategy(self, state, id_team, id_player):	
		mystate = PlayerStateDecorator(miroir(state,id_team), id_team, id_player)
		return Fonceur(mystate)

class StrategyI(BaseStrategy):
	def __init__(self):
		BaseStrategy.__init__(self, "Intercepteur")
	def compute_strategy(self, state, id_team, id_player):
		mystate = PlayerStateDecorator(miroir(state,id_team), id_team, id_player)
		return Intercepteur(mystate)

class StrategyDR(BaseStrategy):
	def __init__(self):
		BaseStrategy.__init__(self, "Dribbleur")
	def compute_strategy(self, state, id_team, id_player):
		mystate = PlayerStateDecorator(miroir(state,id_team), id_team, id_player)
		return Dribbleur(mystate)

"""strat = KeyboardStrategy()
strat.add("d",StrategyD())
strat.add("a",StrategyA())
strat.add("g",StrategyG())"""


def Goal(mystate):
	shoot = Vector2D(0,0)
	vect = Vector2D(0,0)
	err=2
	print(mystate.my_position.x,mystate.my_position.y,mystate.my_goal-Vector2D(-5,0))
	#si loin de mes buts  revenir au buts
	if mystate.my_distance_my_goal_position >= 30:
		vect = mystate.aller(mystate.my_goal-Vector2D(-5,0))
	#si l'adversaire depasse le milieu du terrain
	if mystate.position(mystate.get_idteam_adv,mystate.my_adv_plus_proche).x <= GAME_WIDTH/2 :
		#si la balle se trouve a gauche du terrain  je me positionne a gauche des buts
		if mystate.ball_position.y > GAME_HEIGHT/2+GAME_GOAL_HEIGHT/2 :
			if mystate.my_position.x >=  5-err and mystate.my_position.x <= 5+err and mystate.my_position.y >= 50-err and mystate.my_position.y <= 50+err:
				vect = Vector2D(0,0)
			else:
				vect = mystate.aller(lgoal_lcage_position()-Vector2D(-5,0))
		#sinon si la balle se trouve a droite du terrain  je me positionne a droite des buts
		elif mystate.ball_position.y < GAME_HEIGHT/2-GAME_GOAL_HEIGHT/2 :
			if mystate.my_position.x >=  5-err and mystate.my_position.x <= 5+err and mystate.my_position.y >= 40-err and mystate.my_position.y <= 40+err:
				vect = Vector2D(0,0)
			else:	
				vect = mystate.aller(lgoal_rcage_position()-Vector2D(-5,0))
		#sinon si la balle se trouve dans la zone des buts
		elif mystate.ball_position.y <= GAME_HEIGHT/2+GAME_GOAL_HEIGHT/2 and mystate.ball_position.y >= GAME_HEIGHT/2-GAME_GOAL_HEIGHT/2:
			#si l'adversaire est proche des buts et qu'il peut tirer  et que la balle a une vitesse > 0.4 => signifie que le joueur a tiré 
			if  mystate.position(mystate.get_idteam_adv,mystate.my_adv_plus_proche).x <= GAME_WIDTH/2-50 and mystate.adv_peut_shoot == True and math.sqrt(mystate.ball_vitesse.dot(mystate.ball_vitesse)) > 0.4:
				#if mystate.position_interception_ball != 0:
					#vect = mystate.aller(mystate.position_interception_ball)
				#else:
				bis = mystate.copy()
				for i in range(7):
					bis.ball.next(Vector2D())
				vect = mystate.aller_y_ball					
			else:
				if mystate.my_position.x >=  5-err and mystate.my_position.x <= 5+err and mystate.my_position.y >= 45-err and mystate.my_position.y <= 45+err:
					vect = Vector2D(0,0)
				else:
					vect = mystate.aller(mystate.my_goal-Vector2D(-5,0))
		else:
			vect = mystate.aller(mystate.my_goal-Vector2D(-5,0))
	if mystate.peut_shoot == True:
		shoot = mystate.shoot(mystate.adv_goal).norm_max(5)
	if mystate.get_my_idteam == 2:	
		return SoccerAction(miroir_v(vect),miroir_v(shoot))
	return SoccerAction(vect,shoot)
	
"""def Goal(mystate):
	shoot = Vector2D(0,0)	
	vect =Vector2D(0,0)	
	
	
	pos_x= mystate.ball_position.x-mystate.my_position.x
	pos_y=mystate.ball_position.y-mystate.my_position.y
	vect.angle= math.degrees(math.atan2(-pos_y, pos_x))
	if mystate.my_distance_my_goal_position >= 5:
		vect = mystate.aller(mystate.my_goal-Vector2D(-5,0))
		vect.angle=mystate.ball_position.angle
	#
	if (vect.angle >= 360) or (vect.angle < -360):
            vect.angle = 0
	
	
	vect = mystate.aller(mystate.my_goal-Vector2D(-5,0))
	print(vect.angle)
	
	print(mystate.my_position.x,mystate.my_position.y,mystate.my_goal-Vector2D(-5,0))
	#si loin de mes buts  revenir au buts
	if mystate.my_distance_my_goal_position >= 30:
		vect = mystate.aller(mystate.my_goal-Vector2D(-5,0))
	#si l'adversaire depasse le milieu du terrain
	if mystate.position(mystate.get_idteam_adv,mystate.my_adv_plus_proche).x <= GAME_WIDTH/2 :
		#si la balle se trouve a gauche du terrain  je me positionne a gauche des buts
		if mystate.ball_position.y > GAME_HEIGHT/2+GAME_GOAL_HEIGHT/2 :
			if mystate.my_position.x >=  5-err and mystate.my_position.x <= 5+err and mystate.my_position.y >= 50-err and mystate.my_position.y <= 50+err:
				vect = Vector2D(0,0)
			else:
				vect = mystate.aller(lgoal_lcage_position()-Vector2D(-5,0))
		#sinon si la balle se trouve a droite du terrain  je me positionne a droite des buts
		elif mystate.ball_position.y < GAME_HEIGHT/2-GAME_GOAL_HEIGHT/2 :
			if mystate.my_position.x >=  5-err and mystate.my_position.x <= 5+err and mystate.my_position.y >= 40-err and mystate.my_position.y <= 40+err:
				vect = Vector2D(0,0)
			else:	
				vect = mystate.aller(lgoal_rcage_position()-Vector2D(-5,0))
		#sinon si la balle se trouve dans la zone des buts
		elif mystate.ball_position.y <= GAME_HEIGHT/2+GAME_GOAL_HEIGHT/2 and mystate.ball_position.y >= GAME_HEIGHT/2-GAME_GOAL_HEIGHT/2:
			#si l'adversaire est proche des buts et qu'il peut tirer  et que la balle a une vitesse > 0.4 => signifie que le joueur a tiré 
			if  mystate.position(mystate.get_idteam_adv,mystate.my_adv_plus_proche).x <= GAME_WIDTH/2-50 and mystate.adv_peut_shoot == True and math.sqrt(mystate.ball_vitesse.dot(mystate.ball_vitesse)) > 0.4:
				#if mystate.position_interception_ball != 0:
					#vect = mystate.aller(mystate.position_interception_ball)
				#else:
				bis = mystate.copy()
				for i in range(7):
					bis.ball.next(Vector2D())
				vect = mystate.aller_y_ball					
			else:
				if mystate.my_position.x >=  5-err and mystate.my_position.x <= 5+err and mystate.my_position.y >= 45-err and mystate.my_position.y <= 45+err:
					vect = Vector2D(0,0)
				else:
					vect = mystate.aller(mystate.my_goal-Vector2D(-5,0))
		else:
			vect = mystate.aller(mystate.my_goal-Vector2D(-5,0))
	if mystate.peut_shoot == True:
		shoot = mystate.shoot(mystate.adv_goal).norm_max(5)
	if mystate.get_my_idteam == 2:	
		return SoccerAction(miroir_v(vect),miroir_v(shoot))
	return SoccerAction(vect,shoot)"""


def Defenseur(mystate):
	shoot = Vector2D(0,0)
	vect = Vector2D(0,0)
	if mystate.position(mystate.get_idteam_adv,mystate.my_adv_plus_proche).x <= GAME_WIDTH/2:
		if mystate.position(mystate.get_idteam_adv,mystate.my_adv_plus_proche).x >= 45:
				vect = mystate.aller_ball
		elif mystate.my_distance_adv_plus_proche <= 20:
			if mystate.my_distance_ball < mystate.distance_adv_plus_proche_ball:
				#if mystate.position_interception_ball != 0:
					#vect = mystate.aller(mystate.position_interception_ball)
				#else:
				vect = mystate.aller_ball
			else:
				vect = mystate.aller_y_ball
		else:
			#if mystate.position_interception(mystate.get_idteam_adv,mystate.my_adv_plus_proche) != 0:
				#vect = mystate.aller(mystate.position_interception(mystate.get_idteam_adv,mystate.my_adv_plus_proche))
			#else:
			vect = mystate.aller(mystate.position(mystate.get_idteam_adv,mystate.my_adv_plus_proche))
	else:
		vect = mystate.aller(mystate.my_goal-Vector2D(-45,0))		
	if mystate.peut_shoot == True:
		if mystate.ball_position.y < GAME_HEIGHT/2:
			shoot = mystate.shoot(Vector2D(mystate.adv_goal.x,mystate.adv_goal.y+GAME_GOAL_HEIGHT/2)-1).norm_max(5)
		elif mystate.ball_position.y >= GAME_HEIGHT/2:
			shoot = mystate.shoot(Vector2D(mystate.adv_goal.x,mystate.adv_goal.y-GAME_GOAL_HEIGHT/2)+1).norm_max(5)
	if mystate.get_my_idteam == 2:	
		return SoccerAction(miroir_v(vect),miroir_v(shoot))
	return SoccerAction(vect,shoot)

def Renvoyeur(mystate):
	shoot=Vector2D(0,0)
	vect = mystate.aller_y_ball
	if mystate.my_position.x > mystate.ball_position.x:
		vect=mystate.aller_ball
	if mystate.my_distance_ball >= 35:
		vect = mystate.aller_x_ball
	if mystate.peut_shoot == True:
		shoot=mystate.shoot(mystate.adv_goal)
	if mystate.get_my_idteam ==2:	
		return SoccerAction(miroir_v(vect),miroir_v(shoot))
	return SoccerAction(vect,shoot)

def Fonceur(mystate):
	shoot=Vector2D(0,0)
	vect=mystate.aller_ball
	if mystate.my_position.x >= GAME_WIDTH/2+20:
		shoot=mystate.shoot(mystate.adv_goal).norm_max(2)
	else:
		if randint(0,1) == 0:
			shoot=mystate.shoot(Vector2D(mystate.adv_goal.x,mystate.adv_goal.y+20)).norm_max(5)
		else:
			shoot=mystate.shoot(Vector2D(mystate.adv_goal.x,mystate.adv_goal.y-20)).norm_max(5)	
	
	if mystate.get_my_idteam ==2:
		return SoccerAction(miroir_v(vect),miroir_v(shoot))
	return SoccerAction(vect,shoot)
	
def Attaquant(mystate):
	shoot = Vector2D(0,0)
	technique = 0
	vect = mystate.aller_ball
	print(mystate.my_distance_adv_goal_position <= 35)
	if mystate.my_distance_ball > PLAYER_RADIUS and mystate.distance_adv_plus_proche_ball > PLAYER_RADIUS:
		if mystate.my_distance_ball < mystate.distance_adv_plus_proche_ball:
			vect = mystate.aller_ball
		else:
			if mystate.my_position.x > mystate.ball_position.x:
				vect = mystate.aller_ball
			if mystate.my_distance_ball >= 35:
				vect = mystate.aller_ball
	if mystate.my_distance_adv_goal_position <= 38 and mystate.my_distance_adv_plus_proche > 20:
		shoot = mystate.shoot(mystate.adv_goal).norm_max(5)
	if mystate.my_distance_ball <= PLAYER_RADIUS:
		if mystate.peut_shoot == True:
			if mystate.my_distance_adv_plus_proche < 5 or mystate.my_distance_adv_plus_proche > 40 and mystate.my_distance_adv_goal_position > 30:
				if mystate.my_position.y < GAME_HEIGHT/2:
					technique = 2
				elif mystate.my_position.y > GAME_HEIGHT/2:
					technique = -2
				else:
					if randint(0,1) == 0:
						technique = 2
					else:
						technique = -2
				shoot = Vector2D(mystate.my_position.x+2,mystate.my_position.y+technique)-Vector2D(mystate.my_position.x,mystate.my_position.y)
			elif mystate.my_distance_adv_goal_position <= 35:
				if mystate.ball_position.y < GAME_HEIGHT/2:
					shoot = mystate.shoot(Vector2D(mystate.adv_goal.x,mystate.adv_goal.y+GAME_GOAL_HEIGHT/2)-1).norm_max(5)
				elif mystate.ball_position.y >= GAME_HEIGHT/2:
					shoot = mystate.shoot(Vector2D(mystate.adv_goal.x,mystate.adv_goal.y-GAME_GOAL_HEIGHT/2)+1).norm_max(5)
			else:
				if randint(0,1) == 0:
					shoot = mystate.shoot(Vector2D(mystate.adv_goal.x,mystate.adv_goal.y+GAME_GOAL_HEIGHT/2)).norm_max(5)
				else:
					shoot = mystate.shoot(Vector2D(mystate.adv_goal.x,mystate.adv_goal.y-GAME_GOAL_HEIGHT/2)).norm_max(5)
				shoot = Vector2D(mystate.my_position.x+0.7,0)-Vector2D(mystate.my_position.x,0)
	if mystate.distance_adv_plus_proche_ball <= PLAYER_RADIUS:
		if mystate.my_position.x > mystate.ball_position.x:
			vect = mystate.aller_ball
		if mystate.my_distance_ball >= 35:
			vect = mystate.aller_ball
	if mystate.get_my_idteam == 2:
		return SoccerAction(miroir_v(vect),miroir_v(shoot))
	return SoccerAction(vect,shoot)
	
def Dribbleur(mystate):
	shoot = Vector2D(0,0)
	vect = mystate.aller_ball
	if mystate.my_distance_adv_plus_proche > 40 or mystate.my_distance_adv_plus_proche < 8:
		if mystate.my_distance_ball < PLAYER_RADIUS + BALL_RADIUS:
			shoot = mystate.shoot(mystate.adv_goal).norm_max(3)+Vector2D(0.5,0)
	else:					
		if mystate.my_distance_ball < PLAYER_RADIUS + BALL_RADIUS:
			shoot = Vector2D(mystate.my_position.x+0.4,0)-Vector2D(mystate.my_position.x,0)
	if mystate.get_my_idteam == 2:
		return SoccerAction(miroir_v(vect),miroir_v(shoot))
	return SoccerAction(vect,shoot)

def Random(mystate):
		return SoccerAction(Vector2D().create_random(-5,5),Vector2D().create_random())

def Intercepteur(mystate):
	vect = mystate.aller_y_ball
	shoot = Vector2D()
	if mystate.distance_adv_plus_proche_ball > mystate.my_distance_ball+0.2:
		vect = mystate.aller_ball
	elif mystate.my_distance_ball >= 34:
		vect = mystate.aller_x_ball
	elif mystate.distance_adv_plus_proche_ball <= PLAYER_RADIUS+BALL_RADIUS:
		bis = mystate.copy()
		for i in range(10):
			bis.ball.next(Vector2D())
		vect = mystate.aller_ball
	if mystate.peut_shoot == True:
		shoot = mystate.shoot(mystate.adv_goal).norm_max(5)
	if mystate.get_my_idteam == 2:	
		return SoccerAction(miroir_v(vect),miroir_v(shoot))
	return SoccerAction(vect,shoot)

"""def Poly(mystate):
	vect=Vector2D()
	shoot=Vector2D()
	technique=0
	if mystate.distance_adv_plus_proche_ball > mystate.my_distance_ball+0.2:
		vect=mystate.aller_ball
		if mystate.peut_shoot == True:
			if mystate.my_position.y < GAME_HEIGHT/2:
				technique = 2
			elif mystate.my_position.y > GAME_HEIGHT/2:
				technique = -2
			else:
				if randint(0,1) == 0:
					technique = 2
				else:
					technique = -2
			if mystate.my_distance_adv_plus_proche > 40 or mystate.my_distance_adv_plus_proche < 10 and mystate.my_distance_adv_goal_position > 30:
				shoot = Vector2D(mystate.my_position.x+2,mystate.my_position.y+technique)-Vector2D(mystate.my_position.x,mystate.my_position.y)	
			elif mystate.my_distance_adv_goal_position <= 30:
				if mystate.ball_position.y < GAME_HEIGHT/2:
					shoot = mystate.shoot(Vector2D(mystate.adv_goal.x,mystate.adv_goal.y+GAME_GOAL_HEIGHT/2)-2).norm_max(5)
				elif mystate.ball_position.y >= GAME_HEIGHT/2:
					shoot = mystate.shoot(Vector2D(mystate.adv_goal.x,mystate.adv_goal.y-GAME_GOAL_HEIGHT/2)+2).norm_max(5)
			else:
				shoot = Vector2D(mystate.my_position.x+0.4,0)-Vector2D(mystate.my_position.x,0)
	else:	
		
			vect = mystate.aller(mystate.my_goal-Vector2D(-5,0))		
		
		if mystate.peut_shoot == True:
			if mystate.ball_position.y < GAME_HEIGHT/2:
				shoot = mystate.shoot(Vector2D(mystate.adv_goal.x,mystate.adv_goal.y+GAME_GOAL_HEIGHT/2)-1).norm_max(5)
			elif mystate.ball_position.y >= GAME_HEIGHT/2:
				shoot = mystate.shoot(Vector2D(mystate.adv_goal.x,mystate.adv_goal.y-GAME_GOAL_HEIGHT/2)+1).norm_max(5)
	if mystate.get_my_idteam ==2:
		return SoccerAction(miroir_v(vect),miroir_v(shoot))
	return SoccerAction(vect,shoot)"""
	
def Polyvalent(mystate):
	vect=Vector2D()
	shoot=Vector2D()
	technique=0
	print(mystate.distance_adv_plus_proche_ball > mystate.my_distance_ball)
	#si je suis plus pres de la balle que mon adv je fonce sur la balle sinon je reste a une certaine distance
	if mystate.distance_adv_plus_proche_ball > mystate.my_distance_ball+0.00001:
		vect=mystate.aller_ball
		#je dribble si pres d'un adv
		if mystate.my_distance_adv_plus_proche <= 5:
			if mystate.my_position.y < GAME_HEIGHT/2:
					technique = 2
			elif mystate.my_position.y > GAME_HEIGHT/2:
				technique = -2
			else:
				if randint(0,1) == 0:
					technique = 2
				else:
					technique = -2
			if mystate.peut_shoot:
				shoot = Vector2D(mystate.my_position.x+2,mystate.my_position.y+technique)-Vector2D(mystate.my_position.x,mystate.my_position.y)
		#j'avance la balle si loin de l'adv
		elif mystate.my_distance_adv_plus_proche > 5:
			if mystate.peut_shoot:
				shoot = Vector2D(mystate.my_position.x+1.5,0)-Vector2D(mystate.my_position.x,0)
		#si pres des buts je tire
		elif mystate.my_distance_adv_goal_position <= 30:
			if mystate.ball_position.y < GAME_HEIGHT/2:
				if mystate.peut_shoot:
					shoot = mystate.shoot(Vector2D(mystate.adv_goal.x,mystate.adv_goal.y+GAME_GOAL_HEIGHT/2)-2).norm_max(5)
			elif mystate.ball_position.y >= GAME_HEIGHT/2:
				if mystate.peut_shoot:
					shoot = mystate.shoot(Vector2D(mystate.adv_goal.x,mystate.adv_goal.y-GAME_GOAL_HEIGHT/2)+2).norm_max(5)
	else:
		#si je suis loin je me rapproche de la balle sinon je reste dans le meme axe y que la balle
		if mystate.my_distance_ball >= 34:
			vect = mystate.aller_ball
		else:
			if mystate.my_distance_adv_plus_proche < 9 and mystate.ball_position.x > mystate.my_position.x:	
				vect = mystate.aller_ball
			else:	
				if mystate.ball_position.x < mystate.my_position.x:
					vect=mystate.aller(mystate.my_goal-Vector2D(-5,0))
				else:
					vect = mystate.aller_y_ball			
					#vect = mystate.aller_ball
				
		if mystate.ball_position.y < GAME_HEIGHT/2:
			if mystate.peut_shoot:
				shoot = mystate.shoot(Vector2D(mystate.adv_goal.x,mystate.adv_goal.y+GAME_GOAL_HEIGHT/2)-2).norm_max(5)
		elif mystate.ball_position.y >= GAME_HEIGHT/2:
			if mystate.peut_shoot:
				shoot = mystate.shoot(Vector2D(mystate.adv_goal.x,mystate.adv_goal.y-GAME_GOAL_HEIGHT/2)+2).norm_max(5)	
	
	if mystate.get_my_idteam ==2:
		return SoccerAction(miroir_v(vect),miroir_v(shoot))
	return SoccerAction(vect,shoot)
	
	
"""class Toutdl(BaseStrategy):
        def __init__(self):
                BaseStrategy.__init__(self, "Att+deff")
	
        def compute_strategy(self, state, id_team, id_player):
		if id_team ==1:
			advCAGE=rgoal_position()
		else:
			advCAGE=lgoal_position()
		ratio = 0.3
		alpha = 0.7
		L=[1,2,3,4,5]
		if random() < ratio:
			Nbj=len(state.players)/2
			Tx=range(GAME_WIDTH)
			Ty=range(GAME_HEIGHT)
			#a= choice(L)
			dist1=15
			dist2=10
			distloin=20
			distmarq=3
			p=Vector2D(choice(Tx),choice(Ty))
			if a == 1:
				#se deplacer vers un point
				vect=p-my_position(state,id_team,id_player)
				if my_position(state,id_team,id_player).distance(my_position(state,2,id_player)) <= 2*PLAYER_RADIUS:
					p=Vector2D(choice(Tx),choice(Ty))
					vect=p-my_position(state,id_team,id_player)
			if a == 2:
				#se deplacer vers un point en groupe
				if id_player == 0:
					if my_position(state,id_team,id_player).distance(my_position(state,1,1)) > dist1:
						vect=my_position(state,1,1)-my_position(state,id_team,id_player)
					elif my_position(state,id_team,id_player).distance(my_position(state,1,1)) < dist2:
						vect=my_position(state,id_team,id_player)-my_position(state,1,1)
					else:
						vect=p-my_position(state,id_team,id_player)
				else:
					if my_position(state,id_team,id_player).distance(my_position(state,1,0)) > dist1:
						vect=my_position(state,1,0)-my_position(state,id_team,id_player)
					elif my_position(state,id_team,id_player).distance(my_position(state,1,0)) < dist2:
						vect=my_position(state,id_team,id_player)-my_position(state,1,0)
					else:
						vect=p-my_position(state,id_team,id_player)
				
			if a==3:
				#se positionner
				if id_player == 0:
					if my_position(state,id_team,id_player).distance(my_position(state,1,1)) > dist1:
						vect=my_position(state,1,1)-my_position(state,id_team,id_player)
					elif my_position(state,id_team,id_player).distance(my_position(state,1,1)) < dist2:
						vect=my_position(state,id_team,id_player)-my_position(state,1,1)
					else:
						vect=p-my_position(state,id_team,id_player)
					if p.distance(my_position(state,1,1)) <= dist2 and p.distance(my_position(state,2,id_player)) >= distloin:
						vect=p-my_position(state,id_team,id_player)
					if my_position(state,id_team,id_player).distance(my_position(state,2,id_player)) <= 2*PLAYER_RADIUS:
						p=Vector2D(choice(Tx),choice(Ty))
						vect=p-my_position(state,id_team,id_player)
			if a==4:
				#marquer un adversaire
				if id_team == 1:
					if p.distance(my_position(state,2,id_player)) <= PLAYER_RADIUS+distmarq:
						vect=p-my_position(state,id_team,id_player)
				elif my_position(state,id_team,id_player).distance(my_position(state,2,id_player)) <= distmarq:	
					vect=my_position(state,id_team,id_player)-my_position(state,2,id_player)
				else:
					vect=my_position(state,2,id_player)-my_position(state,id_team,id_player)
			if a==5:
				#aller vers le joueur adv
				vect=my_position(state,2,0)-my_position(state,id_team,id_player)
			if a==6:
				#si plus pres que le joueur adv foncer sur la balle 
				if my_position(state,2,0).distance(ball_position(state)) > my_position(state,id_team,id_player).distance(ball_position(state))+0.2:
					vect=ball_position(state)-my_position(state,id_team,id_player)
			if a==7:
				#si ma distance avec la balle superieur a 34 se rapprocher de la balle
				if my_position(state,id_team,id_player).distance(ball_position(state)) >= 34:
					vect = Vector2D(ball_position(state).x,0)-Vector2D(my_position(state,id_team,id_player).x,0)
			if a==8:
				#shooter la balle dans une direction d
				d=Vector2D(choice(Tx),choice(Ty))
				shoot=d-my_position(state,id_team,id_player)
		#else:
			
		#	a= argmax/L { R(s,a) + V(f) }
		#}
		#r(s,a)= R(s,a)
		#for ( state in espaceEtats){
		#	V(s) = max/L { r(s,a)+ alpha * V(f) }
		
		shoot=Vector2D()
		point=ball_position(state)
		
		return SoccerAction(aller(point),shoot)"""