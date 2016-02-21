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

"""wait=0
revenir=1
aller=2
suivre=3
shooter=4
dribbler=5"""
class PlayerStateDecorator:

	def __init__(self, state, id_team, id_player):
		self.state = state
		self.id_team = id_team
		self.id_player = id_player
		#self.mood = wait
		
	@property
	def idp(self):
		# mon id
		return self.id_player
		
	@property
	def idt(self):
		# l'id de ma team
		return self.id_team
		
	@property
	def mon_mood(self):
		#mon etat
		return self.mood
		
	@property
	def ma_position(self):
		#ma position
		return self.state.player_state(self.id_team,self.id_player).position
		
	@property
	def ma_position_initiale(self):
		#ma position initiale
		if self.state.step == 0:
			return self.state.player_state(self.id_team,self.id_player).position
		
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
		return self.distance(self.ma_position,self.goal_adv)
		
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
			if idt == self.idt:# and idp != self.id:
				L.append(self.distance(self.ma_position,self.position_balle))#self.position(idt,idp)))
				Lbis.append(idp)
		return Lbis[L.index(min(L))]
		
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
		return ((p-self.ma_position).normalize()*maxPlayerSpeed)-self.ma_vitesse
		
	def aller_y(self,p):
		# aller au point p dans l'axe y seulement
		return ((Vector2D(0,p.y)-Vector2D(0,self.ma_position.y)).normalize()*maxPlayerSpeed)-self.ma_vitesse
		
	def aller_x(self,p):
		# aller au point p dans l'axe x seulement	
		return ((Vector2D(p.x,0)-Vector2D(self.ma_position.x,0)).normalize()*maxPlayerSpeed)-self.ma_vitesse
		
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
		return ((self.ma_position-p).normalize()*maxPlayerSpeed)-self.ma_vitesse
		
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
			vitesse= (distance/ 1.5)*0.3 #1.5-2(deceleration normale) constante de deceleration
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
		
		
	@property
	def ma_position_objectif(self):
		Lx=[]
		Ly=[]
		for x in range(GAME_WIDTH/2+5,GAME_WIDTH-15):
			for y in range(GAME_HEIGHT+5,GAME_HEIGHT-5):
				if x%10 == 0 and y%10 == 0:
						Lx.append(x)
						Ly.append(y)
		i=randint(0,len(Lx)-1)
		return Vector2D(Lx[i],Ly[i])
			
	"""def changer_mood(self,idp):
		d=self.ma_distance_balle
		obj=self.ma_position_objectif
		if self.idt == idp:
			if self.mood != suivre or self.mood != shooter or self.mood != dribbler:
				if d < 20:
					if self.peut_shoot:
						if self.ma_distance_adv_plus_proche < 8:
							self.mood = dribbler
						else:
							self.mood = shooter
				else:
					self.mood = suivre
					
		elif self.mood == wait:
			if self.idt == idp:
				self.mood = suivre
			elif self.position_balle.x < GAME_WIDTH/2:
				if self.distance(self.ma_position,self.ma_position_initiale) > 20:
					self.mood = revenir
			elif self.position_balle.x > GAME_WIDTH/2:
				if self.distance(self.ma_position,obj) > 20:
					self.mood = aller
					
		elif self.mood == suivre:
            if d < 20 and self.idt == idp:
                self.mood = shooter
            elif d > 100 and self.idt != idp:
                self.mood = attendre
        elif self.mood == revenir:
            if self.ma_position.x - self.ma_position_initiale.x > -10:
                if self.ma_position.y - self.ma_position_initiale.y > -10:
                    if self.ma_position.x - self.ma_position_initiale.x < 10:
                        if self.ma_position.y - self.ma_position_initiale.y < 10:
                            self.mood = attendre
            if self.idt == idp:
                self.mood = suivre
            elif self.position_balle.x < GAME_WIDTH/2:
                if self.distance(self.ma_position,obj) > 20:
                    self.mood = aller
        elif self.mood == aller:
            if self.ma_position.x - obj.x > -10:
                if self.ma_position.y - obj.y > -10:
                    if self.ma_position.x - obj.x < 10:
                        if self.ma_position.y - obj.y < 10:
                            self.mood = attendre
            if self.idt == idp:
                self.mood = suivre
            elif self.position_balle.x < GAME_WIDTH/2:
                if self.distance(self.ma_position,self.ma_position_initiale) > 20:
                    self.mood = revenir
        elif self.mood == shooter:
            if self.idt == idp:
                self.mood = suivre
            else:
                self.mood = aller"""
	
		
	"""def ball_next_position(self,step):
		# position de la balle apres un step de temps x = 1/2vt+v0t + x0 (x0=0,vect=v0t,x=1/2vt)
		vect= self.vitesse_balle * step
		x = (0.5*self.vitesse_balle*step )* self.vitesse_balle.normalize()
		return self.balle_position + vect + x

	def temps_distance_balle(self,posA,posB,norme):
		#temps que met la balle pour parcourir la distance entre la position A et la position B t=d/v
		return self.distance(posA,pos,B)/self.ball_vitesse.norm_max(norme)
		
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
	
	#@property		
	#def interpose(self):
		#vect = (self.position(self.get_idteam_adv,self.my_adv_plus_proche) + self.ma_position)/2
		#time= self.my_distance(vect)/self.ma_vitesse*maxPlayerSpeed
		#Apos= (self.position(self.get_idteam_adv,self.my_adv_plus_proche) + (self.vitesse(self.get_idteam_adv,self.my_adv_plus_proche)*time
		#Bpos= self.ma_position + self.ma_vitesse * time
		#midpoint= Apos+Bpos / 2
		#return self.stopper_dest(midpoint)


			
		

		
	def peut_faire_passe_test(self,posA,posB,receveur,idadv,norme):
		#true si adv ne peut intercepter la balle sinon false
		shoot= (posB - posA).norm_max(norme)
		#test simplifié (on doit changer de repere pour avoir un test correct)
		#si le joueur adv se trouve derriere moi	
		if self.position(self.idt,idadv).x < 0:
			return True
		#si le joueur adv est loin de la position de passe
		if self.distance(posA,posB) < self.distance(self.position(self.idt_adv,idadv),posA):
			#si passe dans le vide idp = -1
			if receveur != -1:
				#si le joueur idp est plus pres de la position de passe que le joueur adv
				if self.distance(posB,receveur) < self.distance(self.position(self.idt_adv,idadv),posB):
					return True
			else:
				return True
		#calcul du temps que va mettre la balle pour arriver a y de idadv
		time= temps_distance_balle(self.ma_position,Vector2D(self.position(self.idt_adv,idadv),0),norme)	
		#la distance a parcourir par idadv pour intercepter
		distIntercept= self.vitesse(self.idt_adv,idadv)* maxPlayerSpeed * time + BALL_RADIUS + PLAYER_RADIUS	
		#si distance est inférieur a distIntercept, la balle va etre intercepter 
		if self.distance(self.position(self.idt_adv,idadv),self.position_balle) < distIntercept:
			return False
		return True
		
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
			
	def peut_marquer(self,norme):
		# true si le joueur peut marquer sinon false	
		#il dispose de 10 tentatives
		essai = 9;	
		for i in range(essai):
			#trouve une position de but aléatoire 
			shoot=self.goal_adv
			lpos=lgoal_lcage_position()-BALL_RADIUS
			rpos=lgoal_rcage_position()+BALL_RADIUS
			shoot.x= randint(lpos,rpos)
			#test si la balle atteindra les buts
			time= self.temps_distance_balle(self.position_balle,shoot,norme)
			#test si un adv peut intercepter le tir 
			if time > 0:
				if self.peut_faire_passe(self.position_balle,shoot,-1,norme) == True:
					return shoot
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

"""class StrategyT(BaseStrategy):
	def __init__(self):
		BaseStrategy.__init__(self, "Test")
	def compute_strategy(self, state, id_team, id_player):
		mystate = PlayerStateDecorator(miroir(state,id_team), id_team, id_player)
		return Test(mystate)
		
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
		return Attaquant(mystate)"""
		
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
"""
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
		return Dribbleur(mystate)"""

"""strat = KeyboardStrategy()
strat.add("d",StrategyD())
strat.add("a",StrategyA())
strat.add("r",StrategyR())"""
"""
def Test(mystate):
	shoot = Vector2D(0,0)
	vect = Vector2D(0,0)
	mystate.changer_mood(mystate.mon_j_plus_proche)
	if mystate.mon_mood == suivre:
		vect = mystate.aller(mystate.position_balle)
	elif mystate.mon_mood == revenir:
		vect = mystate.stopper_dest(mystate.ma_position_initiale)
	elif mystate.mon_mood == aller:
		vect = mystate.stopper_dest(mystate.ma_position_objectif)
	elif mystate.mon_mood == shooter:
		shoot=shoot=mystate.shoot(mystate.goal_adv).norm_max(5)
		
	if mystate.idt == 2:
		return SoccerAction(miroir_v(vect),miroir_v(shoot))
	return SoccerAction(vect,shoot)
"""
"""def Goal(mystate):
	shoot = Vector2D(0,0)
	vect = Vector2D(0,0)
	#vect = mystate.aller_balle
	#print()
	if mystate.ma_distance_goal >= 30:
		vect = mystate.stopper_dest(mystate.goal-Vector2D(-1.5,0))
	if mystate.position(mystate.idt_adv,mystate.mon_adv_plus_proche).x <= GAME_WIDTH/2 :
		if mystate.position_balle.y > GAME_HEIGHT/2+GAME_GOAL_HEIGHT/2+GAME_GOAL_HEIGHT:
			vect = mystate.stopper_dest(lgoal_lcage_position()-Vector2D(-1.5,0))
		elif mystate.position_balle.y < GAME_HEIGHT/2-GAME_GOAL_HEIGHT/2-GAME_GOAL_HEIGHT:
			vect = mystate.stopper_dest(lgoal_rcage_position()-Vector2D(-1.5,0))
		elif mystate.position_balle.y <= GAME_HEIGHT/2+GAME_GOAL_HEIGHT/2+GAME_GOAL_HEIGHT and mystate.position_balle.y >= GAME_HEIGHT/2-GAME_GOAL_HEIGHT/2-GAME_GOAL_HEIGHT:
			vect = mystate.stopper_dest(mystate.my_goal-Vector2D(-1.5,0))
		if mystate.position_balle.y <= GAME_HEIGHT/2+GAME_GOAL_HEIGHT/2 and mystate.position_balle.y >= GAME_HEIGHT/2-GAME_GOAL_HEIGHT/2:
			vect=mystate.stopper_dest(mystate.position_balle)
			if mystate.ma_distance_balle <5:
				vect=mystate.aller_y_ball
			
	if mystate.peut_shoot == True:
		shoot = Vector2D().create_random()#mystate.shoot(mystate.goal_adv).norm_max(5)
	if mystate.idt == 2:
		return SoccerAction(miroir_v(vect),miroir_v(shoot))
	return SoccerAction(vect,shoot)
	
def Goal(mystate):
	shoot = Vector2D(0,0)	
	vect =Vector2D(0,0)	
	
	
	pos_x= mystate.position_balle.x-mystate.ma_position.x
	pos_y=mystate.position_balle.y-mystate.ma_position.y
	vect.angle= math.degrees(math.atan2(-pos_y, pos_x))
	if mystate.my_distance_my_goal_position >= 5:
		vect = mystate.aller(mystate.my_goal-Vector2D(-5,0))
		vect.angle=mystate.position_balle.angle
	#
	if (vect.angle >= 360) or (vect.angle < -360):
            vect.angle = 0
	
	
	vect = mystate.aller(mystate.my_goal-Vector2D(-5,0))
	print(vect.angle)
	
	print(mystate.ma_position.x,mystate.ma_position.y,mystate.my_goal-Vector2D(-5,0))
	#si loin de mes buts  revenir au buts
	if mystate.my_distance_my_goal_position >= 30:
		vect = mystate.aller(mystate.my_goal-Vector2D(-5,0))
	#si l'adversaire depasse le milieu du terrain
	if mystate.position(mystate.get_idteam_adv,mystate.my_adv_plus_proche).x <= GAME_WIDTH/2 :
		#si la balle se trouve a gauche du terrain  je me positionne a gauche des buts
		if mystate.position_balle.y > GAME_HEIGHT/2+GAME_GOAL_HEIGHT/2 :
			if mystate.ma_position.x >=  5-err and mystate.ma_position.x <= 5+err and mystate.ma_position.y >= 50-err and mystate.ma_position.y <= 50+err:
				vect = Vector2D(0,0)
			else:
				vect = mystate.aller(lgoal_lcage_position()-Vector2D(-5,0))
		#sinon si la balle se trouve a droite du terrain  je me positionne a droite des buts
		elif mystate.position_balle.y < GAME_HEIGHT/2-GAME_GOAL_HEIGHT/2 :
			if mystate.ma_position.x >=  5-err and mystate.ma_position.x <= 5+err and mystate.ma_position.y >= 40-err and mystate.ma_position.y <= 40+err:
				vect = Vector2D(0,0)
			else:	
				vect = mystate.aller(lgoal_rcage_position()-Vector2D(-5,0))
		#sinon si la balle se trouve dans la zone des buts
		elif mystate.position_balle.y <= GAME_HEIGHT/2+GAME_GOAL_HEIGHT/2 and mystate.position_balle.y >= GAME_HEIGHT/2-GAME_GOAL_HEIGHT/2:
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
				if mystate.ma_position.x >=  5-err and mystate.ma_position.x <= 5+err and mystate.ma_position.y >= 45-err and mystate.ma_position.y <= 45+err:
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


def Defenseur(mystate):
	shoot = Vector2D(0,0)
	vect = mystate.aller(mystate.my_goal-Vector2D(-45,0))+mystate.aller_y(mystate.position(mystate.get_idteam_adv,mystate.my_adv_plus_proche))
	#print(mystate.position(mystate.get_idteam_adv,mystate.my_adv_plus_proche).x)
	if mystate.position(mystate.get_idteam_adv,mystate.my_adv_plus_proche).x <= GAME_WIDTH/2:
		if mystate.position(mystate.get_idteam_adv,mystate.my_adv_plus_proche).x >= 45:
				vect = mystate.aller_ball
		elif mystate.my_distance_adv_plus_proche <= 20:
			if mystate.my_distance_ball < mystate.distance_adv_plus_proche_ball:
				vect = mystate.aller_ball
			else:
				vect = mystate.aller_y_ball
		else:
			vect = mystate.aller(mystate.position(mystate.get_idteam_adv,mystate.my_adv_plus_proche))
	else:
		vect = mystate.aller(mystate.my_goal-Vector2D(-45,0))+mystate.aller_y(mystate.position(mystate.get_idteam_adv,mystate.my_adv_plus_proche))
			
	if mystate.peut_shoot == True:
		if mystate.position_balle.y < GAME_HEIGHT/2:
			shoot = mystate.shoot(Vector2D(mystate.adv_goal.x,mystate.adv_goal.y+GAME_GOAL_HEIGHT/2)-1).norm_max(5)
		elif mystate.position_balle.y >= GAME_HEIGHT/2:
			shoot = mystate.shoot(Vector2D(mystate.adv_goal.x,mystate.adv_goal.y-GAME_GOAL_HEIGHT/2)+1).norm_max(5)
	if mystate.get_my_idteam == 2:	
		return SoccerAction(miroir_v(vect),miroir_v(shoot))
	return SoccerAction(vect,shoot)
"""
def Renvoyeur(mystate):
	shoot=Vector2D(0,0)
	vect = mystate.aller_y_balle
	if mystate.ma_position.x > mystate.position_balle.x:
		vect=mystate.aller_balle
	if mystate.ma_distance_balle >= 35:
		vect = mystate.aller_x_balle
	if mystate.peut_shoot == True:
		shoot=mystate.shoot(mystate.goal_adv)
	if mystate.idt ==2:	
		return SoccerAction(miroir_v(vect),miroir_v(shoot))
	return SoccerAction(vect,shoot)

def Fonceur(mystate):
	shoot=mystate.shoot(mystate.goal_adv).norm_max(5)
	#shoot=Vector2D()
	#print(mystate.ma_position_initiale)
	vect=mystate.aller_balle
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
"""	
def Attaquant(mystate):
	shoot = Vector2D(0,0)
	technique = 0
	vect = mystate.aller_ball
	#print(mystate.my_distance_adv_goal_position <= 35)
	if mystate.my_distance_ball > PLAYER_RADIUS and mystate.distance_adv_plus_proche_ball > PLAYER_RADIUS:
		if mystate.my_distance_ball < mystate.distance_adv_plus_proche_ball:
			vect = mystate.aller_ball
		else:
			if mystate.ma_position.x > mystate.position_balle.x:
				vect = mystate.aller_ball
			if mystate.my_distance_ball >= 35:
				vect = mystate.aller_ball
	if mystate.my_distance_adv_goal_position <= 38 and mystate.my_distance_adv_plus_proche > 20:
		shoot = mystate.shoot(mystate.adv_goal).norm_max(5)
	if mystate.my_distance_ball <= PLAYER_RADIUS:
		if mystate.peut_shoot == True:
			if mystate.my_distance_adv_plus_proche < 5 or mystate.my_distance_adv_plus_proche > 40 and mystate.my_distance_adv_goal_position > 30:
				if mystate.ma_position.y < GAME_HEIGHT/2:
					technique = 2
				elif mystate.ma_position.y > GAME_HEIGHT/2:
					technique = -2
				else:
					if randint(0,1) == 0:
						technique = 2
					else:
						technique = -2
				shoot = Vector2D(mystate.ma_position.x+2,mystate.ma_position.y+technique)-Vector2D(mystate.ma_position.x,mystate.ma_position.y)
			elif mystate.my_distance_adv_goal_position <= 35:
				if mystate.position_balle.y < GAME_HEIGHT/2:
					shoot = mystate.shoot(Vector2D(mystate.adv_goal.x,mystate.adv_goal.y+GAME_GOAL_HEIGHT/2)-2)
				elif mystate.position_balle.y >= GAME_HEIGHT/2:
					shoot = mystate.shoot(Vector2D(mystate.adv_goal.x,mystate.adv_goal.y-GAME_GOAL_HEIGHT/2)+2)
			else:
				if randint(0,1) == 0:
					shoot = mystate.shoot(Vector2D(mystate.adv_goal.x,mystate.adv_goal.y+GAME_GOAL_HEIGHT/2))
				else:
					shoot = mystate.shoot(Vector2D(mystate.adv_goal.x,mystate.adv_goal.y-GAME_GOAL_HEIGHT/2))
				shoot = Vector2D(mystate.ma_position.x+0.7,0)-Vector2D(mystate.ma_position.x,0)
	if mystate.distance_adv_plus_proche_ball <= PLAYER_RADIUS:
		if mystate.ma_position.x > mystate.position_balle.x:
			vect = mystate.aller_ball
		if mystate.my_distance_ball >= 35:
			vect = mystate.aller_ball
	if mystate.get_my_idteam == 2:
		return SoccerAction(miroir_v(vect),miroir_v(shoot))
	return SoccerAction(vect,shoot)
	
def Dribbleur(mystate):
	shoot = Vector2D(0,0)
	vect =Vector2D(0,0)
	technique = 0
	print(mystate.my_distance_j_plus_proche)

	if mystate.ma_position.x <= mystate.position(mystate.get_my_idteam,mystate.my_j_plus_proche).x + 35:
		vect=mystate.aller(mystate.adv_goal)
	else:
		vect=mystate.aller(mystate.my_goal)
	if mystate.my_distance_ball < 30:
		vect=mystate.aller_ball
		
	if mystate.my_distance_adv_plus_proche > 40 or mystate.my_distance_adv_plus_proche < 8:
		if mystate.my_distance_ball < PLAYER_RADIUS + BALL_RADIUS:
			shoot = mystate.shoot(mystate.adv_goal).norm_max(3)+Vector2D(0.5,0)
	else:					
		if mystate.my_distance_ball < PLAYER_RADIUS + BALL_RADIUS:
			shoot = Vector2D(mystate.ma_position.x+0.4,0)-Vector2D(mystate.ma_position.x,0)
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
		#bis = mystate.copy()
		#for i in range(10):
			#bis.ball.next(Vector2D())
		vect = mystate.aller_ball
	if mystate.peut_shoot == True:
		shoot = mystate.shoot(mystate.adv_goal).norm_max(5)
	if mystate.get_my_idteam == 2:	
		return SoccerAction(miroir_v(vect),miroir_v(shoot))
	return SoccerAction(vect,shoot)
"""	
def Polyvalent(mystate):
	#distance parcouru depend de la norme, norme = 1 <=> d =~10 ( observation) 
	#print(math.sqrt(mystate.vitesse(mystate.get_idteam_adv,mystate.my_adv_plus_proche).dot(mystate.vitesse(mystate.get_idteam_adv,mystate.my_adv_plus_proche))),math.sqrt(mystate.vitesse(mystate.get_idteam_adv,mystate.my_adv_plus_proche).dot(mystate.vitesse(mystate.get_idteam_adv,mystate.my_adv_plus_proche))) < 0.6)
	shoot=Vector2D()
	vect=mystate.aller_balle
	if mystate.distance_adv_plus_proche_balle < mystate.ma_distance_balle+1:
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
			shoot = Vector2D(angle=6.1,norm=5)
		else:
			shoot = Vector2D(angle=0.2,norm=5)
	elif mystate.peut_shoot and ( mystate.ma_position.x > GAME_WIDTH/2 or mystate.ma_position.x > mystate.position(mystate.idt_adv,mystate.mon_adv_plus_proche).x+1):
		shoot = mystate.shoot(mystate.goal_adv).norm_max(0.7)
		if mystate.ma_position.x > mystate.position(mystate.idt_adv,mystate.mon_adv_plus_proche).x+1 or mystate.ma_distance_goal_adv < 35:
			if mystate.position_balle.y < GAME_HEIGHT/2:
				shoot = mystate.shoot(Vector2D(mystate.goal_adv.x,mystate.goal_adv.y+GAME_GOAL_HEIGHT/2)-randint(1,3)).norm_max(4)
			else:
				shoot = mystate.shoot(Vector2D(mystate.goal_adv.x,mystate.goal_adv.y-GAME_GOAL_HEIGHT/2)+randint(1,3)).norm_max(4)
		
	if mystate.idt==2:
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
				vect=p-ma_position(state,id_team,id_player)
				if ma_position(state,id_team,id_player).distance(ma_position(state,2,id_player)) <= 2*PLAYER_RADIUS:
					p=Vector2D(choice(Tx),choice(Ty))
					vect=p-ma_position(state,id_team,id_player)
			if a == 2:
				#se deplacer vers un point en groupe
				if id_player == 0:
					if ma_position(state,id_team,id_player).distance(ma_position(state,1,1)) > dist1:
						vect=ma_position(state,1,1)-ma_position(state,id_team,id_player)
					elif ma_position(state,id_team,id_player).distance(ma_position(state,1,1)) < dist2:
						vect=ma_position(state,id_team,id_player)-ma_position(state,1,1)
					else:
						vect=p-ma_position(state,id_team,id_player)
				else:
					if ma_position(state,id_team,id_player).distance(ma_position(state,1,0)) > dist1:
						vect=ma_position(state,1,0)-ma_position(state,id_team,id_player)
					elif ma_position(state,id_team,id_player).distance(ma_position(state,1,0)) < dist2:
						vect=ma_position(state,id_team,id_player)-ma_position(state,1,0)
					else:
						vect=p-ma_position(state,id_team,id_player)
				
			if a==3:
				#se positionner
				if id_player == 0:
					if ma_position(state,id_team,id_player).distance(ma_position(state,1,1)) > dist1:
						vect=ma_position(state,1,1)-ma_position(state,id_team,id_player)
					elif ma_position(state,id_team,id_player).distance(ma_position(state,1,1)) < dist2:
						vect=ma_position(state,id_team,id_player)-ma_position(state,1,1)
					else:
						vect=p-ma_position(state,id_team,id_player)
					if p.distance(ma_position(state,1,1)) <= dist2 and p.distance(ma_position(state,2,id_player)) >= distloin:
						vect=p-ma_position(state,id_team,id_player)
					if ma_position(state,id_team,id_player).distance(ma_position(state,2,id_player)) <= 2*PLAYER_RADIUS:
						p=Vector2D(choice(Tx),choice(Ty))
						vect=p-ma_position(state,id_team,id_player)
			if a==4:
				#marquer un adversaire
				if id_team == 1:
					if p.distance(ma_position(state,2,id_player)) <= PLAYER_RADIUS+distmarq:
						vect=p-ma_position(state,id_team,id_player)
				elif ma_position(state,id_team,id_player).distance(ma_position(state,2,id_player)) <= distmarq:	
					vect=ma_position(state,id_team,id_player)-ma_position(state,2,id_player)
				else:
					vect=ma_position(state,2,id_player)-ma_position(state,id_team,id_player)
			if a==5:
				#aller vers le joueur adv
				vect=ma_position(state,2,0)-ma_position(state,id_team,id_player)
			if a==6:
				#si plus pres que le joueur adv foncer sur la balle 
				if ma_position(state,2,0).distance(position_balle(state)) > ma_position(state,id_team,id_player).distance(position_balle(state))+0.2:
					vect=position_balle(state)-ma_position(state,id_team,id_player)
			if a==7:
				#si ma distance avec la balle superieur a 34 se rapprocher de la balle
				if ma_position(state,id_team,id_player).distance(position_balle(state)) >= 34:
					vect = Vector2D(position_balle(state).x,0)-Vector2D(ma_position(state,id_team,id_player).x,0)
			if a==8:
				#shooter la balle dans une direction d
				d=Vector2D(choice(Tx),choice(Ty))
				shoot=d-ma_position(state,id_team,id_player)
		#else:
			
		#	a= argmax/L { R(s,a) + V(f) }
		#}
		#r(s,a)= R(s,a)
		#for ( state in espaceEtats){
		#	V(s) = max/L { r(s,a)+ alpha * V(f) }
		
		shoot=Vector2D()
		point=position_balle(state)
		
		return SoccerAction(aller(point),shoot)"""
