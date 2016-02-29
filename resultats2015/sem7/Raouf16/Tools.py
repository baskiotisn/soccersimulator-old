#import soccersimulator
import math
import random
from soccersimulator import settings
from soccersimulator import SoccerAction 
from soccersimulator import Vector2D


##############################################################################
#         				 Miroir				     #
##############################################################################

def miroir_p(p):       # miroir position
    return Vector2D( settings.GAME_WIDTH - p.x,p.y)

        # miroir vecteur
def miroir_v(v):
    return Vector2D(-1*v.x , v.y)  
    
def miroir_sa(action):
    return SoccerAction(miroir_v(action.acceleration),miroir_v(action.shoot))
    
def miroir_st(state):
    res = state.copy()
    res.ball.position = miroir_p(state.ball.position)
    res.ball.vitesse = miroir_v(state.ball.vitesse)
    for (id_team, id_player) in state.players :
        (res.player_state(id_team,id_player)).position = miroir_p(state.player_state(id_team,id_player).position)
        (res.player_state(id_team,id_player)).vitesse = miroir_v(state.player_state(id_team,id_player).vitesse)
    return res    

##########################################################################################
#			Utilisation de Design Pattern Decorator				 #
#				A partir du 22/02/2016					 #
##########################################################################################

class PlayerStateDecorator : 
	def __init__(self , state , id_team , id_player):
	
		self.state = state
		self.id_team = id_team
		self.id_player = id_player 

	##################################################################
	#			POSITIONS				 #
	##################################################################
	@property
	def rienFaire(self):
		return SoccerAction()

	@property
	def position_balle(self):
		#Retourne la position de la balle
		return self.state.ball.position

	@property
	def vitesse_balle(self):
	 	#Retourne la vitesse de la balle
		return self.state.ball.vitesse

	@property
	def position_joueur(self):
		#Retourne la position du joueur
		return self.state.player_state(self.id_team, self.id_player).position

	@property
    	def position_defense(self):
        	return self.state.player_state(self.id_team, self.id_player == 0).position
    
   	@property
    	def position_milieu(self):
       		return self.state.player_state(self.id_team, self.id_player == 1).position
    
   	@property
   	def position_milieuDefense(self):
        	return self.state.player_state(self.id_team, self.id_player == 2).position

	@property
   	def position_attaquant(self):
       		return self.state.player_state(self.id_team, self.id_player == 3).position


	##################################################################
	#			Fonctions				 #
	##################################################################

	@property
	def peutShooter(self):
		return (self.position_balle.distance(self.position_joueur)) < (settings.PLAYER_RADIUS + settings.BALL_RADIUS) 

	@property
	def passeOuShoot(self):
		return SoccerAction(self.position_balle - self.position_joueur, Vector2D(settings.GAME_WIDTH, settings.GAME_HEIGHT / 2) - self.position_joueur)
	
	@property
	def passeVersAttaque(self):
		return SoccerAction(self.position_balle - self.position_joueur, self.position_attaquant - self.position_joueur)
	@property
	def courirVersBalle(self):
		return SoccerAction(self.position_balle - self.position_joueur, Vector2D(0,0))

	@property
	def peutShooterDefensegauche(self):
		return self.position_balle.x < 35

	@property
	def peutShooterDefensedroit(self):
		return self.position_balle.x < 50

	@property
	def peutShooterAttaque(self):
		return self.position_balle.x > 110

	@property
	def peutShooterDefense(self):
		return self.position_balle.x < 35

	@property
	def peutShooterMilieu(self):
		return (self.position_balle.x > 35) 

	@property
	def peutShooterMilieuDefensif(self):
		return (self.position_balle.x < settings.GAME_WIDTH/2+10) 


	@property
	def shootDefense(self):
	    	if (self.peutShooter):
			return SoccerAction(self.position_balle - self.position_joueur, Vector2D(settings.GAME_WIDTH, settings.GAME_HEIGHT / 2) - self.position_joueur)
		else: 
			return SoccerAction(self.position_balle - self.position_joueur, Vector2D(0,0))

	@property
	def replacementDefense(self):
		return SoccerAction(Vector2D(10, settings.GAME_HEIGHT / 2) - self.position_joueur, Vector2D(0,0))
		 #le defenseur se replace en defense si la balle sort de sa zone defensive

	@property
	def replacementDefenseurGauche(self):
		return SoccerAction(Vector2D(10, settings.GAME_HEIGHT/2 + 5) - self.position_joueur, Vector2D(0,0))
		#le defenseur gauche se replace a sa position

	@property
	def replacementDefenseurDroit(self):
		return SoccerAction(Vector2D(10, settings.GAME_HEIGHT/2 - 5) - self.position_joueur, Vector2D(0,0))
	 	#le defenseur droit se replace a sa position

	@property
	def replacementMilieu(self):
		return SoccerAction(Vector2D(50, settings.GAME_HEIGHT/2) - self.position_joueur, Vector2D(0,0))

	@property
	def replacementMilieuDefensif(self):
		#Le milieu se place en position de contre attaque
		return SoccerAction(Vector2D(settings.GAME_WIDTH/2+10, self.position_balle.y) - self.position_joueur, Vector2D(0,0))

	@property
	def replacementAttaque(self):
		#L'attaquant se place devant les cages
		return SoccerAction(Vector2D(settings.GAME_WIDTH-30, self.position_balle.y) - self.position_joueur, Vector2D(0,0))
	
##################################################################
#			Joueurs 				 #
##################################################################

def attaquant_fonceur(Mystate):
	if(Mystate.peutShooter):
		return Mystate.passeOuShoot	
 	else:
             	return Mystate.courirVersBalle

def attaquant_pointe(Mystate):
	if(Mystate.peutShooterAttaque):
		if(Mystate.peutShooter):
			return Mystate.passeOuShoot
		else:
			return Mystate.courirVersBalle
	else:
		return Mystate.replacementAttaque

def defenseur_central(Mystate):
	if(Mystate.peutShooterDefense):
		if(Mystate.peutShooter):
			return Mystate.shootDefense
		else:
			return Mystate.courirVersBalle
	return Mystate.replacementDefense

def defenseur_gauche(Mystate):
	if(Mystate.peutShooterDefense):
		if(Mystate.peutShooter):
			return Mystate.shootDefense
		else:
			return Mystate.courirVersBalle
	return Mystate.replacementDefenseurGauche

def defenseur_droit(Mystate):
	if(Mystate.peutShooterDefense):
		if(Mystate.peutShooter):
			return Mystate.shootDefense
		else:
			return Mystate.courirVersBalle
	return Mystate.replacementDefenseurDroit

def milieu(Mystate):
	if(Mystate.peutShooterMilieu):
		if(Mystate.peutShooter):
			return Mystate.passeOuShoot
		else:
			return Mystate.courirVersBalle
	return Mystate.replacementMilieu

def milieu_defensif(Mystate):
	if(Mystate.peutShooterMilieuDefensif):
		if(Mystate.peutShooter):
			return Mystate.passeOuShoot
		else:
			return Mystate.courirVersBalle
	return Mystate.replacementMilieuDefensif


