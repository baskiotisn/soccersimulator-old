# -*- coding: utf-8 -*-
from random import *
import soccersimulator
from tools import *
from  soccersimulator.settings import *
from soccersimulator import BaseStrategy, KeyboardStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
import math, random

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

	def __init__(self, state, id_team, id_player,info = None):
		self.state = state
		self.id_team = id_team
		self.id_player = id_player
		self.info = info
		
	@property
	def idp(self):
		# mon id
		return self.id_player
		
	@property
	def idt(self):
		# l'id de ma team
		return self.id_team

	@property
	def step(self):
		# le temps
		return self.state.step
		
	@property
	def ma_position(self):
		#ma position
		return self.state.player_state(self.id_team,self.id_player).position
		
	@property
	def ma_position_initiale(self):
		#ma position initiale 1 vs 1 (15,45)
		return Vector2D(15,45)

		
	@property
	def ma_vitesse(self):
		#le vecteur vitesse = velocité
		return self.state.player_state(self.idt,self.idp).vitesse	
		
	def position(self,idt,idp):
		#position du joueur idp de la team idt
		return self.state.player_state(idt,idp).position
		
	def vitesse(self,idt,idp):
		#velocité du joueur idp de la team idt
		return self.state.player_state(idt,idp).vitesse
		
	@property
	def position_balle(self):	
		#position de la balle
		return self.state.ball.position
		
	@property
	def vitesse_balle(self):
		#vitesse de la balle
		return self.state.ball.vitesse
		
	@property
	def idt_adv(self):
		# l'id de la team adverse
		if self.idt ==1:
			return 2
		else:
			return 1
			
	@property
	def nbj(self):
		#nombre de joueur de ma team
		i=0
		for (idt,idp) in self.state.players:
			if idt == self.idt:
				i+=1
		return i
		
	@property
	def nbj_adv(self):
		#nombre de joueur de la team adv
		i=0
		for (idt,idp) in self.state.players:
			if idt != self.idt:
				i+=1
		return i
		
	@property
	def goal(self):
		# mes buts
		return lgoal_position()
		
	@property
	def goal_adv(self):
		# les buts adverse
		return rgoal_position()
		
	def distance(self,posA,posB):
		# distance entre A et B
		return posA.distance(posB)
		
	def ma_distance(self,p):
		# ma distance au point p
		return self.distance(self.ma_position,p)
		
	@property
	def ma_distance_balle(self):
		# ma distance a la balle
		return self.distance(self.ma_position,self.position_balle)
	
	@property
	def ma_distance_goal_adv(self):
		# ma distance a la position des buts adverse
		return self.distance(self.ma_position,self.goal_adv)
		
	@property
	def  ma_distance_goal(self):
		# ma distance a la position de mes buts
		return self.distance(self.ma_position,self.goal)
		
	@property
	def ma_distance_adv_plus_proche(self):
		# ma distance a l'adversaire le plus proche de moi 
		L=[]
		for (idt,idp) in self.state.players:
			if idt != self.idt:
				L.append(self.distance(self.ma_position,self.position(idt,idp)))
		return min(L)
	
	@property
	def ma_distance_j_plus_proche(self):
		# ma distance au joueur de l'equipe  le plus proche de moi 
		L=[]
		for (idt,idp) in self.state.players:
			if idt == self.idt and idp != self.id:
				L.append(self.distance(self.ma_position,self.position(idt,idp)))
		return min(L)
		
	@property	
	def mon_j_plus_proche(self):
		# id du joueur de la team le plus proche de moi
		L=[]
		Lbis=[]
		for (idt,idp) in self.state.players:
			if idt == self.idt and idp != self.id:
				L.append(self.distance(self.ma_position,self.position(idt,idp)))
				Lbis.append(idp)
		return Lbis[L.index(min(L))]
	
	"""@property	
	def mon_j_plus_proche1(self,idteam,idj):
		# id du joueur de la team le plus proche de moi
		L=[]
		Lbis=[]
		for (idt,idp) in self.state.players:
			if idt == self.idt and idp != idj:
				L.append(self.distance(self.position(idteam,idj),self.position(idt,idp)))
				Lbis.append(idp)
		return Lbis[L.index(min(L))]
		
	@property	
	def mon_j_plus_proche2(self,idteam,idj):
		# id du joueur de la team le plus proche de moi
		L=[]
		Lbis=[]
		for (idt,idp) in self.state.players:
			if idt != self.idt and idp != idj:
				L.append(self.distance(self.position(idteam,idj),self.position(idt,idp)))
				Lbis.append(idp)
		return Lbis[L.index(min(L))]
		
	@property	
	def le_joueur_safe_team(self,idj):
		# id du joueur  le plus  safe de la team
		mn = 100000
		id=idj
		dd=self.mon_j_plus_proche2(self.id,id)
		for (idt,idp) in self.state.players:
			if idp == id:
				continue
			d = self.mon_j_plus_proche2(self.id,idp)
			yy=(self.position(self.id,idp).y-self.position(self.id,id).y)*(self.position(self.id,idp).y-self.position(self.id,id).y)
			if d > dd and yy < GAME_HEIGHT:
				dst =(self.position(self.id,idp).x-self.goal)*(self.position(self.id,idp).x-self.goal)
				if mn > dst:
					mn = dst
					id = idp
		return id"""

	@property	
	def le_joueur_plus_proche_balle(self):
		# id du joueur  le plus proche de la balle
		L=[]
		Lbis=[]
		for (idt,idp) in self.state.players:
			L.append(self.distance(self.position_balle,self.position(idt,idp)))
			Lbis.append(idp)
		return Lbis[L.index(min(L))]
		
	@property	
	def le_joueur_plus_proche_balle_team(self):
		# id du joueur  le plus proche de la balle de ma team
		L=[]
		Lbis=[]
		for (idt,idp) in self.state.players:
			if idt == self.idt:
				L.append(self.distance(self.position_balle,self.position(idt,idp)))
				Lbis.append(idp)
		return Lbis[L.index(min(L))]
			
	@property	
	def mon_adv_plus_proche(self):
		# id de l'adversaire le plus proche de moi
		L=[]
		Lbis=[]
		for (idt,idp) in self.state.players:
			if idt != self.idt:
				L.append(self.distance(self.ma_position,self.position(idt,idp)))
				Lbis.append(idp)
		return Lbis[L.index(min(L))]
		
	@property
	def adv_plus_proche_balle(self):
		# adversaire le plus proche de la balle
		L=[]
		Lbis=[]
		for (idt,idp) in self.state.players:
			if idt != self.idt:
				L.append(self.distance(self.position(idt,idp),self.position_balle))
				Lbis.append(idp)
		return Lbis[L.index(min(L))]
		
	@property	
	def distance_adv_plus_proche_balle(self):
		# la distance entre la balle et le joueur  adversaire le plus proche de la balle
		L=[]
		for (idt,idp) in self.state.players:
			if idt != self.id_team:
				L.append(self.distance(self.position(idt,idp),self.position_balle))
		return min(L)
		
	def shoot(self,p):
		# tirer vers la position p
		return p-self.ma_position
	
	@property	
	def peut_shoot(self):
		# le joueur peut tirer
		if self.ma_distance_balle < PLAYER_RADIUS + BALL_RADIUS:
			return True
		else:
			return False

	@property			
	def adv_peut_shoot(self):
		# adversaire le  plus proche de la balle peut tirer
		if self.distance_adv_plus_proche_balle < PLAYER_RADIUS + BALL_RADIUS:
			return True
		else:
			return False

	def aller(self,p):
		# aller au point p
		return ((p-self.ma_position).normalize()*maxPlayerSpeed)
	def aller_test(self,p):
		# aller au point p
		return p-self.ma_position

		
	def aller_y(self,p):
		# aller au point p dans l'axe y seulement
		return ((Vector2D(0,p.y)-Vector2D(0,self.ma_position.y)).normalize()*maxPlayerSpeed)
		
	def aller_x(self,p):
		# aller au point p dans l'axe x seulement	
		return ((Vector2D(p.x,0)-Vector2D(self.ma_position.x,0)).normalize()*maxPlayerSpeed)
		
	@property
	def aller_balle(self):
		# aller vers la balle	
		return self.aller(self.position_balle)
		
	@property	
	def aller_y_balle(self):
		# aller vers la balle dans l'axe y seulement
		return self.aller_y(self.position_balle)
		
	@property	
	def aller_x_balle(self):
		# aller vers la balle dans l'axe x seulement
		return self.aller_x(self.position_balle)

	def ne_pas_aller(self,p):
		# Ne pas aller au point p = fuir le point p
		return ((self.ma_position-p).normalize()*maxPlayerSpeed)
		
	@property
	def ne_pas_aller_balle(self):
		# fuir la balle
		return self.ne_pas_aller(self.position_balle)

	def stopper_dest(self,p):
		#s'arreter a la position p
		vect=p-self.ma_position
		#distance entre la position p et ma position
		distance=self.ma_distance(p)
		#si distance et superieur on va faire une deceleration sinon on s'arrete
		if distance > 0:
			#vitesse pour atteindre destination
			vitesse= (distance/ 1)*0.3 #1.5-2(deceleration normale) constante de deceleration
			#vitesse min
			vitesse= min(vitesse,maxPlayerSpeed)
			return (vect*vitesse/distance)-self.ma_vitesse
		return Vector2D(0,0)
		
	"""@property
	def suivre_adv_proche(self):
		pos=self.position(self.idt_adv,self.mon_adv_plus_proche)
		a=math.sqrt((self.ma_vitesse*maxPlayerSpeed).dot(self.ma_vitesse*maxPlayerSpeed))
		if a > 0 :
			time = self.ma_distance(pos)/a
			pos=pos+self.vitesse(self.idt_adv,self.mon_adv_plus_proche)*time
		return self.aller(pos)"""
		
	@property
	def suivre_adv_proche(self):
		#suivre l'adv le plus proche
		vect=Vector2D()
		pos=self.position(self.idt_adv,self.mon_adv_plus_proche)
		a=math.sqrt((self.ma_vitesse*maxPlayerSpeed).dot(self.ma_vitesse*maxPlayerSpeed))
		if a > 0 :
			time = self.ma_distance(pos)/a
			vect=pos+self.vitesse(self.idt_adv,self.mon_adv_plus_proche)*time
		return self.aller(vect)
		
	@property
	def suivre_balle(self):
		#suivre la balle
		vect=Vector2D()
		pos=self.position_balle
		a=math.sqrt((self.ma_vitesse*maxPlayerSpeed).dot(self.ma_vitesse*maxPlayerSpeed))
		if a > 0 :
			time = self.ma_distance(pos)/a
			vect=pos+self.vitesse_balle*time
		return self.aller(vect)

	@property
	def fuir_adv_proche(self):
		#fuir l'adv le plus proche
		vect=Vector2D()
		pos=self.position(self.idt_adv,self.mon_adv_plus_proche)
		a=math.sqrt((self.ma_vitesse*maxPlayerSpeed).dot(self.ma_vitesse*maxPlayerSpeed))
		if a > 0 :
			time = self.ma_distance(pos)/a
			vect=pos+self.vitesse(self.idt_adv,self.mon_adv_plus_proche)*time
		return self.ne_pas_aller(vect)

	def bloquer(self,posB):
		midpoint = self.position_balle+posB/2
		a=math.sqrt((self.ma_vitesse*maxPlayerSpeed).dot(self.ma_vitesse*maxPlayerSpeed))
		if a > 0:
			time= self.ma_distance(midpoint)/a
			Apos= self.position_balle + self.vitesse_balle*time
			Bpos= posB + self.vitesse_balle * time
			midpoint= Apos+Bpos / 2
		return self.stopper_dest(midpoint)
	
	@property
	def zone_goal(self):
		#balle zone goal(true si danger false sinon)
		return self.distance(self.goal,self.position_balle) <= 40
		
	@property
	def loin_goal(self):
		#loin des cages true sinon false
		return self.distance(self.ma_position,self.position_interception) > 40
		
	@property
	def regarder_balle(self):
		#vecteur regarder la balle
		return (mystate.position_balle-mystate.ma_position).normalize().norm_max(0.000001)

		
	@property
	def position_interception(self):
		#position d'interception de la balle pour le goal
		a= (GAME_HEIGHT/2-GAME_GOAL_HEIGHT/2 + (self.position_balle.y)*GAME_GOAL_HEIGHT)/GAME_HEIGHT
		return Vector2D(self.goal.x,a)
		
	
		
		
	@property
	def ma_position_objectif(self):
		Lx=[]
		Ly=[]
		for x in range((GAME_WIDTH/2+5),(GAME_WIDTH-15)):
			for y in range(5,(GAME_HEIGHT-5)):
				if x%10 == 0 and y%10 == 0:
						Lx.append(x)
						Ly.append(y)
		i=randint(0,len(Lx)-1)
		return Vector2D(Lx[i],Ly[i])

	@property
	def attribut_arbre(self):
		return [self.ma_distance_balle,self.ma_distance_goal,self.ma_distance_goal_adv,self.ma_distance_adv_plus_proche,self.distance_adv_plus_proche_balle,self.distance(self.position(self.idt_adv,self.mon_adv_plus_proche),self.goal),self.distance(self.position(self.idt_adv,self.mon_adv_plus_proche),self.goal_adv)]
		
	def peut_faire_passe(self,posA,posB,posReceveur,norme):
		#
		nbj=self.nbj_adv
		test=0
		#true si adv ne peut intercepter la balle sinon false
		shoot= (posB - posA).norm_max(norme)
		for (idt,idp) in self.state.players:
			if idt != self.idt:
				#test simplifié (on doit changer de repere pour avoir un test correct)
				#si le joueur adv se trouve derriere moi	
				if self.position(idt,idp).x < 0:
					test+=1
					continue
				#si le joueur adv est loin de la position de passe
				if self.distance(posA,posB) < self.distance(self.position(idt,idp),posA):
					#si passe dans le vide receveur = -1
					if posReceveur != Vector2D():
						#si le receveur est plus pres de la position de passe que le joueur adv
						if self.distance(posB,posReceveur) < self.distance(self.position(idt,idp),posB):
							test+=1
							continue
					else:
						test+=1
						continue
				#calcul du temps que va mettre la balle pour arriver a la position de idp
				time= self.temps_distance_balle(posA,self.position(idt,idp),norme)	
				#la distance a parcourir par idp pour intercepter
				distI= self.vitesse(idt,idp)* maxPlayerSpeed * time + BALL_RADIUS + PLAYER_RADIUS	
				#si distance est inférieur a distI, la balle va etre intercepter 
				if self.distance(self.position(idt,idp),self.position_balle) < distI:
					continue
				#le joueur  est devant moi, il est pres de la position de passe mais 
				#mais il ne peut pas intercepter la balle
				test+=1
				continue
		if test == nbj:
			return True
		else:
			return False

	def peut_marquer(self,norme):
		# true si le joueur peut marquer sinon false	
		#il dispose de 10 tentatives
		essai = 9;	
		for i in range(essai):
			#trouve une position de but aléatoire 
			shoot=self.goal_adv
			lpos=rgoal_lcage_position().x-BALL_RADIUS
			rpos=rgoal_rcage_position().x+BALL_RADIUS
			shoot.x= random.uniform(lpos,rpos)
			#test si la balle atteindra les buts
			time= self.temps_distance_balle(self.position_balle,shoot,norme)
			#test si un adv peut intercepter le tir 
			if time > 0:
				if self.peut_faire_passe(self.position_balle,shoot,Vector2D(),norme) == True:
					return shoot
		return False
		
	"""def ball_next_position(self,step):
		# position de la balle apres un step de temps x = 1/2vt+v0t + x0 (x0=0,vect=v0t,x=1/2vt)
		vect= self.vitesse_balle * step
		x = (0.5*self.vitesse_balle*step )* self.vitesse_balle.normalize()
		return self.balle_position + vect + x


		
	@property
	def get_best_position(self,step):
		if step%2 == 0:
			bestScore=0
			Lx=[]
			Ly=[]
			Lscore=[]
			for x in range(GAME_WIDTH/2+5,GAME_WIDTH-15):
				for y in range(GAME_HEIGHT+5,GAME_HEIGHT-5):
					if x%10 == 0 and y%10 == 0:
						positionScore= 1
						if self.peut_faire_passe(self.ma_position,Vector2D(x,y),-1,2) == True:
							positionScore+=1
						if self.peut_marquer(self.ma_position,5) != False:
							positionScore+=2
						if positionScore > bestScore:
							Lx.append(x)
							Ly.append(y)
							bestScore=positionScore
							Lscore.append(bestScore)
			return Vector2D(Lx[max(Lscore)],Ly[max(Lscore)])
		return self.ma_position
		
	@property
	def adv_avoid(self):
		vision=40
		radar=self.ma_position+(self.ma_vitesse*maxPlayerSpeed).normalize()*vision
		radarbis=radar*0.5
		avoidforce=20
		advdangerpos= None 
		for (idt,idp) in self.state.players:
			if idt != self.id_team:
				if self.collision(radar,radarbis,idt,idp) and ( advdangerpos ==None or self.distance(self.ma_position,self.position(idt,idp)) < self.distance(self.ma_position,advdangerpos)):
					advdangerpos=self.position(idt,idp)
		avoid=Vector2D(0,0)
		if advdangerpos != None:
			avoid = radar - advdangerpos
			avoid.normalize()
			avoid.scale(avoidforce)
		else:
			avoid.scale(0)
		return avoid
		
	def collision(self,vect,vect1,idt,adv):
		return self.distance(self.position(idt,adv),vect) <= PLAYER_RADIUS+1 or self.distance(self.position(idt,adv),vect1) <= PLAYER_RADIUS+1
	

		
	
		
	def peut_faire_passe(self,posA,posB,receveur,norme):
		#test pour tous les adversaires
		nbj=self.nb_teamplayer
		test=0
		for (idt,idp) in self.state.players:
			if idt != self.id_team:	
				if peut_faire_passe_test(posA,posB,receveur,idp,norme) == True:
					test+=1
		if test == nbj:
			return True
		else:
			return False
			

		
	def meilleur_passe(receveur,passe,norme):
		#true si la meilleur passe est trouvé sinon false
		#calcul du temps que va mettre la balle pour arriver a receveur
		time= self.temps_distance_balle(self.position_balle,self.position(self.idt,receveur),norme)	
		#si la balle n'atteint pas le receveur false
		if time <= 0:
			return False
		#la distance d'interception de la balle par le receveur
		distIntercept= self.vitesse(self.idt,receveur)* maxPlayerSpeed * time
		#reduction du rayon d'interception
		distIntercept*= 0.25
		#point de tangence
		pos1=self.get_tangent_pos1(self.position(self.idt,receveur),distIntercept,self.position_balle)
		pos2=self.get_tangent_pos2(self.position(self.idt,receveur),distIntercept,self.position_balle)	
		#les positions possibles d'interceptions de la balle
		L = [pos1,self.position(self.idt,receveur),pos2]
		#parcours des differentes positions
		for i in range(3):
			#si le joueur peut faire la passe
			if self.peut_faire_passe(self.position_balle,L[i],receveur,norme) == True:
				passe=L[i]
				return passe
		return False
		
	def faire_passe(passeur,receveur,passe,norme,mindist):
		#toruver un joueur et faire la passe
		#mindist = distance minimale pour faire une passe
		shoot=Vector2D()
		#variable pour comparaison de distance initialisé avec une grand valeurs
		DISTFAKE=500
		for (idt,idp) in self.state.players:
			if idt == self.id_team:	
				#si le joueur n'est pas le passeur et que la distance de la passe est superieur a mindist^2
				if self.idt != passeur and self.distance(self.position(self.idt,passeur),self.ma_position) > mindist*mindist:
					if self.meilleur_passe(idp,shoot,norme) != False:
						shoot=self.meilleur_passe(idp,shoot,norme)
						#calcul de la distance
						distBut = self.distance(shoot.x,self.adv_goal.x)
						# si distance inférieur alors receveur est le joueur le plus pres des buts adv et la passe est faite
						if distBut < DISTFAKE:
							DISTFAKE=distBut
							receveur=idp
							passe = shoot
		#pas de receveur
		if receveur == -1:
			return False
		else:
			return receveur, passe
	
	#calcul de la tangente
	def get_tangent_pos1(position,distIntercept,ballPos):
		# calcul d'une distance entre a et b
		#X= Xb-Xa
		dx = position.x - ballPos.x
		#Y=Yb-Ya
		dy = position.y - ballPos.y
		#d= match.sqrt(x^2+y^2) 
		dd = math.sqrt(dx*dx+dy*dy)
		return math.atan2(dy,dx) + math.asin(distIntercept/dd)
		
	def get_tangent_pos2(position,distIntercept,ballPos):
		dx = position.x - ballPos.x
		dy = position.y - ballPos.y
		dd = math.sqrt(dx*dx+dy*dy)
		return math.atan2(dy,dx) - math.asin(distIntercept/dd)


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
			return 0"""

class StrategyG(BaseStrategy):
	def __init__(self):
		BaseStrategy.__init__(self, "Goal")
	def compute_strategy(self, state, id_team, id_player):
		mystate = PlayerStateDecorator(miroir(state,id_team), id_team, id_player)
		return Goal(mystate)
		
class StrategyGT2(BaseStrategy):
	def __init__(self):
		BaseStrategy.__init__(self, "Goal")
	def compute_strategy(self, state, id_team, id_player):
		mystate = PlayerStateDecorator(miroir(state,id_team), id_team, id_player)
		return GoalT2(mystate)


class StrategyP(BaseStrategy):
	def __init__(self):
		BaseStrategy.__init__(self, "Polyvalent")
	def compute_strategy(self, state, id_team, id_player):
		mystate = PlayerStateDecorator(miroir(state,id_team), id_team, id_player)	
		return Polyvalent(mystate)

class StrategyD(BaseStrategy):
	def __init__(self):
		BaseStrategy.__init__(self, "Defenseur")
	def compute_strategy(self, state, id_team, id_player):
		mystate = PlayerStateDecorator(miroir(state,id_team), id_team, id_player)
		return Defenseur(mystate)
						
class StrategyF(BaseStrategy):
	def __init__(self):
		BaseStrategy.__init__(self, "Fonceur")
		self.info=dict()
	def compute_strategy(self, state, id_team, id_player):	
		mystate = PlayerStateDecorator(miroir(state,id_team), id_team, id_player,self.info)
		return Fonceur(mystate)	

class StrategyA(BaseStrategy):
	def __init__(self):
		BaseStrategy.__init__(self, "Attaquant")
	def compute_strategy(self, state, id_team, id_player):
		mystate = PlayerStateDecorator(miroir(state,id_team), id_team, id_player)
		return Attaquant(mystate)
		
class StrategyAT2(BaseStrategy):
	def __init__(self):
		BaseStrategy.__init__(self, "Attaquant")
	def compute_strategy(self, state, id_team, id_player):
		mystate = PlayerStateDecorator(miroir(state,id_team), id_team, id_player)
		return AttaquantT2(mystate)
		
class DTreeStrategy(BaseStrategy):
    def __init__(self,tree,dic,gen_feat):
        BaseStrategy.__init__(self,"Tree Strategy")
        self.dic = dic
        self.tree = tree
        self.gen_feat= gen_feat
    def compute_strategy(self, state, id_team, id_player):
        label = self.tree.predict(self.gen_feat(state,id_team,id_player))[0]
        if label not in self.dic:
            print("Erreur : strategie %s non trouve" %(label,))
            return SoccerAction()
        return self.dic[label].compute_strategy(state,id_team,id_player)

strat_key = KeyboardStrategy()
strat_key.add("a",StrategyA())
strat_key.add("g",StrategyG())
strat_key.add("d",StrategyD())

###########################################
# JOUEUR TREE
###########################################

def Goal(mystate):
	shoot = Vector2D(0,0)
	vect = Vector2D(0,0)
	#print(mystate.ma_distance_goal)
	if mystate.ma_distance_goal >= 30:
		vect = mystate.aller(mystate.goal-Vector2D(-1.5,0))
	if mystate.position_balle.y > GAME_HEIGHT/2+GAME_GOAL_HEIGHT/2+GAME_GOAL_HEIGHT:
		vect = mystate.stopper_dest(lgoal_lcage_position()-Vector2D(-1.5,0))
	elif mystate.position_balle.y < GAME_HEIGHT/2-GAME_GOAL_HEIGHT/2-GAME_GOAL_HEIGHT:
		vect = mystate.stopper_dest(lgoal_rcage_position()-Vector2D(-1.5,0))
	elif mystate.position_balle.y <= GAME_HEIGHT/2+GAME_GOAL_HEIGHT/2+GAME_GOAL_HEIGHT and mystate.position_balle.y >= GAME_HEIGHT/2-GAME_GOAL_HEIGHT/2-GAME_GOAL_HEIGHT:
		vect = mystate.stopper_dest(mystate.goal-Vector2D(-1.5,0))
	if mystate.position_balle.y <= GAME_HEIGHT/2+GAME_GOAL_HEIGHT/2 and mystate.position_balle.y >= GAME_HEIGHT/2-GAME_GOAL_HEIGHT/2:
		if mystate.ma_distance_balle <5:
			vect=mystate.aller_y_balle
	if mystate.ma_distance_balle <25:
			vect=mystate.aller_balle	
	if mystate.peut_shoot:
		if mystate.position(mystate.idt_adv,mystate.mon_adv_plus_proche).y > mystate.ma_position.y :
			shoot = Vector2D(angle=random.uniform(6.1,5.7),norm=maxPlayerShoot)
		else:
			shoot = Vector2D(angle=random.uniform(0.2,0.6),norm=maxPlayerShoot)
	if mystate.idt == 2:
		return SoccerAction(miroir_v(vect),miroir_v(shoot))
	return SoccerAction(vect,shoot)

def Defenseur(mystate):
	shoot=Vector2D(0,0)
	vect = mystate.aller_y_balle
	if mystate.ma_position.x > mystate.position_balle.x:
		vect=mystate.aller_balle
	if mystate.ma_position.x  >  GAME_WIDTH/2:
		if mystate.ma_distance_balle >= 40 :
			vect = mystate.aller_balle
	else:
		if mystate.ma_distance_balle >= 20:
			vect = mystate.aller_balle
	if mystate.peut_shoot == True:
		shoot=mystate.shoot(mystate.goal_adv).norm_max(maxPlayerShoot)
	if mystate.idt ==2:	
		return SoccerAction(miroir_v(vect),miroir_v(shoot))
	return SoccerAction(vect,shoot)

def Attaquant(mystate):
	shoot = Vector2D(0,0)
	vect=mystate.aller_balle
	if mystate.ma_distance_adv_plus_proche < 8:
		if mystate.peut_shoot:
			if mystate.ma_position.x > mystate.position(mystate.idt_adv,mystate.mon_adv_plus_proche).x:
				shoot = mystate.shoot(mystate.goal_adv).norm_max(3)
			else:	
				shoot = mystate.shoot(mystate.goal_adv).norm_max(maxPlayerShoot)
	else:				
		if mystate.peut_shoot:
			shoot = mystate.shoot(mystate.goal_adv).norm_max(1)
	if mystate.ma_distance_goal_adv <= 20:
		shoot = mystate.shoot(mystate.goal_adv).norm_max(4)
	if mystate.idt == 2:
		return SoccerAction(miroir_v(vect),miroir_v(shoot))
	return SoccerAction(vect,shoot)
	
###########################################
# JOUEUR TEST
###########################################
	
def Random(mystate):
		return SoccerAction(Vector2D().create_random(-5,5),Vector2D().create_random())
	
def Fonceur(mystate):
	#shoot=mystate.shoot(mystate.goal_adv).norm_max(5)
	shoot=Vector2D()
	if mystate.step == 0:
		mystate.info[(mystate.idt,mystate.idp,"orig")]=mystate.ma_position_objectif
		#vect=mystate.stopper_dest(obj)
	#print(mystate.position_local(mystate.position(mystate.idt_adv,mystate.mon_adv_plus_proche)))
	if mystate.step%100 == 0:
		if int(mystate.ma_distance(mystate.info[(mystate.idt,mystate.idp,"orig")])) == 0:	
			#print("arrive")
			mystate.info[(mystate.idt,mystate.idp,"orig")]= Vector2D()
		if mystate.info[(mystate.idt,mystate.idp,"orig")] == Vector2D():
			#print("ajour")
			mystate.info[(mystate.idt,mystate.idp,"orig")]=mystate.ma_position_objectif

	#vect=mystate.stopper_dest(mystate.info[(mystate.idt,mystate.idp,"orig")])
	vect=mystate.stopper_dest(mystate.position_balle)
	#print("obj:",mystate.info)
	#if mystate.ma_position != obj:
	#	print(obj)
	#	vect=mystate.stopper_dest(obj)
	#if mystate.step%50
	#vect=mystate.aller_balle
	#print(mystate.ma_distance_balle,mystate.distance_adv_plus_proche_balle,mystate.peut_shoot,mystate.adv_peut_shoot)
	"""print "1,0 ",mystate.state.player_action(1,0)
	print "2,0 ",mystate.state.player_action(2,0)"""
	#print(mystate.peut_marquer(5) != False)
	if mystate.peut_shoot:
		if mystate.step%50 == 0:
			a=randint(3,4)
			
			if mystate.peut_marquer(a) != False:
				shoot=mystate.peut_marquer(a)
				#print("aaaa:",shoot)
			else:
				shoot=mystate.shoot(mystate.goal_adv).norm_max(1)
		#shoot=mystate.shoot(mystate.goal_adv).norm_max(0.5)
	
	"""if mystate.ma_position.x >= GAME_WIDTH/2+20:
		shoot=mystate.shoot(mystate.adv_goal).norm_max(2)
	else:
		if randint(0,1) == 0:
			shoot=mystate.shoot(Vector2D(mystate.adv_goal.x,mystate.adv_goal.y+20)).norm_max(5)
		else:
			shoot=mystate.shoot(Vector2D(mystate.adv_goal.x,mystate.adv_goal.y-20)).norm_max(5)	"""
	if mystate.idt ==2:
		return SoccerAction(miroir_v(vect),miroir_v(shoot))
	return SoccerAction(vect,shoot)
	
###########################################
# JOUEUR TEAM1
###########################################

def Polyvalent(mystate):
	shoot=Vector2D()
	vect=mystate.aller_balle
	if mystate.distance_adv_plus_proche_balle < mystate.ma_distance_balle:
		if mystate.ma_distance_goal  >  85:
			if mystate.ma_distance_balle >= 40 :
				vect=mystate.stopper_dest(mystate.position_balle)
			else:
				#vect=Vector2D()
				vect=mystate.aller_y_balle
				if mystate.distance(mystate.position(mystate.idt_adv,mystate.mon_adv_plus_proche),mystate.goal_adv) <= 6 or mystate.distance(mystate.position_balle,mystate.goal_adv) <= 6:
					vect=mystate.aller_balle
		if math.sqrt(mystate.vitesse(mystate.idt_adv,mystate.mon_adv_plus_proche).dot(mystate.vitesse(mystate.idt_adv,mystate.mon_adv_plus_proche))) < 0.6:
			vect=mystate.aller_balle
					
		else:
			if mystate.ma_distance_balle >= 25 :
				vect=mystate.stopper_dest(mystate.position_balle)
			else:
				vect=mystate.aller_y_balle
	else:
		vect=mystate.aller_balle
	
	if mystate.ma_position.x > mystate.position_balle.x:
			vect=mystate.aller_balle
	
	if mystate.peut_shoot and mystate.ma_position.x < GAME_WIDTH/2:
		if mystate.position(mystate.idt_adv,mystate.mon_adv_plus_proche).y > mystate.ma_position.y :
			shoot = Vector2D(angle=random.uniform(6.2,6.1),norm=maxPlayerShoot)
		else:
			shoot = Vector2D(angle=random.uniform(0.1,0.2),norm=maxPlayerShoot)
	elif mystate.peut_shoot and ( mystate.ma_position.x > GAME_WIDTH/2 or mystate.ma_position.x > mystate.position(mystate.idt_adv,mystate.mon_adv_plus_proche).x+1):
		shoot = mystate.shoot(mystate.goal_adv).norm_max(3)
		if mystate.ma_position.x > mystate.position(mystate.idt_adv,mystate.mon_adv_plus_proche).x+1 or mystate.ma_distance_goal_adv < 35:
			if mystate.position_balle.y < GAME_HEIGHT/2:
				shoot = mystate.shoot(Vector2D(mystate.goal_adv.x,mystate.goal_adv.y+GAME_GOAL_HEIGHT/2)-randint(1,3)).norm_max(4)
			else:
				shoot = mystate.shoot(Vector2D(mystate.goal_adv.x,mystate.goal_adv.y-GAME_GOAL_HEIGHT/2)+randint(1,3)).norm_max(4)
	if mystate.ma_distance_adv_plus_proche < 8:
		if mystate.peut_shoot:
			if mystate.ma_position.x > mystate.position(mystate.idt_adv,mystate.mon_adv_plus_proche).x:
				shoot = mystate.shoot(mystate.goal_adv).norm_max(3)
			else:	
				shoot = mystate.shoot(mystate.goal_adv).norm_max(maxPlayerShoot)
	else:				
		if mystate.peut_shoot:
			shoot = mystate.shoot(mystate.goal_adv).norm_max(0.4)
	if mystate.idt==2:
		return SoccerAction(miroir_v(vect),miroir_v(shoot))
	return SoccerAction(vect,shoot)
	
###########################################
# JOUEUR TEAM2
###########################################

def GoalT2(mystate):
	shoot = Vector2D(0,0)
	#vecteur regarder la balle
	vect=mystate.bloquer(mystate.position_interception)#(mystate.position_balle-mystate.ma_position).normalize().norm_max(0.000001)
	#print(mystate.position_balle.y)
	#print(mystate.ma_distance_goal)


	if mystate.loin_goal:
		vect = mystate.stopper_dest(mystate.goal-Vector2D(-2,0))
	if mystate.zone_goal:
		#vect=mystate.aller_balle
		vect=mystate.suivre_balle
	if mystate.ma_distance_balle <= 30:
		vect=mystate.aller_balle
	if mystate.peut_shoot:
		if mystate.position(mystate.idt_adv,mystate.mon_adv_plus_proche).y > mystate.ma_position.y :
			shoot = Vector2D(angle=random.uniform(6.2,6.1),norm=maxPlayerShoot)
		else:
			shoot = Vector2D(angle=random.uniform(0.1,0.2),norm=maxPlayerShoot)
		
	if mystate.idt == 2:
		return SoccerAction(miroir_v(vect),miroir_v(shoot))
	return SoccerAction(vect,shoot)
	
def AttaquantT2(mystate):
	shoot = Vector2D(0,0)
	vect=mystate.suivre_balle
	if mystate.position_balle.x < GAME_HEIGHT/2:
		if mystate.position(mystate.idt_adv,mystate.mon_adv_plus_proche).y > mystate.ma_position.y :
			vect= mystate.stopper_dest(Vector2D(GAME_WIDTH/2,GAME_HEIGHT))
		else:
			vect= mystate.stopper_dest(Vector2D(GAME_WIDTH/2,0))
	if mystate.ma_distance_balle < 30:
		vect=mystate.aller_balle
	if mystate.ma_distance_adv_plus_proche < 8:
		if mystate.peut_shoot:
			if mystate.ma_position.x > mystate.position(mystate.idt_adv,mystate.mon_adv_plus_proche).x:
				shoot = mystate.shoot(mystate.goal_adv).norm_max(3)
			else:	
				shoot = mystate.shoot(mystate.goal_adv).norm_max(maxPlayerShoot)
	else:				
		if mystate.peut_shoot:
			shoot = mystate.shoot(mystate.goal_adv).norm_max(1)
	if mystate.ma_distance_goal_adv <= 22:
		if mystate.position_balle.y < GAME_HEIGHT/2:
			shoot = mystate.shoot(Vector2D(mystate.goal_adv.x,mystate.goal_adv.y+GAME_GOAL_HEIGHT/2)-random.uniform(1.7,2.3)).norm_max(4)
		else:
			shoot = mystate.shoot(Vector2D(mystate.goal_adv.x,mystate.goal_adv.y-GAME_GOAL_HEIGHT/2)+random.uniform(1.7,2.3)).norm_max(4)
	if mystate.idt == 2:
		return SoccerAction(miroir_v(vect),miroir_v(shoot))
	return SoccerAction(vect,shoot)