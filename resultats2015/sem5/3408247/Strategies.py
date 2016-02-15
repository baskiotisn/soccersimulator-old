# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 16:45:44 2016

@author: 3408247
"""
import math
import soccersimulator
from soccersimulator.settings import  *
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament

from Outils import *
SEUIL_BALL_FAR = 40
SEUIL_BALL_CLOSE = 30
SEUIL_BALL_TOO_CLOSE = 10


class SousStrat(BaseStrategy):
    def __init__(self,sous_strat):
        BaseStrategy.__init__(self,sous_strat.__name__)
        self.strat=sous_strat 
    def compute_strategy(self,state,idteam,idplayer): #ou faire miroir ici 
        return self.strat(MyState(state,idteam,idplayer))   
    

### ATTAQUANT ###


def fonceur(me): #"me->objet state" #faire me bouger et shooter vers but de l'opposant
	return me.aller(me.ball_position)+me.shoot(me.but_position_adv)

def fonceur_alea(me):
	return me.aller_vers_ball + me.shoot_alea

### DEFENSEUR ###

#def def_mouvement_et_shoot_alea(me):
#	if (me.ball_position.x<GAME_WIDTH):
#		if me.test_peut_shooter:
#			return me.shoot_intercepter_contrecarE + me.shoot_alea
#			
#		else:
#			return me.aller_vers_ball + me.shoot_intercepter_contrecarE + me.shoot_alea
#	else:
#		def_position_defaut(me)

def def_mouvement_et_shoot(me):
	action = Vector2D()
	if (me.ball_position.x<GAME_WIDTH/2):
		#print "motier inf"

		if me.test_peut_shooter:
			#print "peut shooter"
				
			return me.shoot_vers_but_adv
		else:
			#print "peut pas shooter"
			
				
			return me.aller_vers_ball + me.shoot_intercepter_contrecarE + me.shoot_vers_but_adv

	else:	
		#print "motier sup pos defaut"
		return me.def_positionnement_defaut



#def def_mouvement_et_shoot_centre(me):



### GARDIEN ###

def revenir_au_but(me): #faire me revenir a la position milieu but 

		if(me.key[0]==1):
   			return me.aller(me.but_position)
		if(me.key[0]==2):
			return me.aller(me.but_position)	

		return SoccerAction()

	
def gardien_mouvement(me):

	
	if (dist(me.but_position,me.ball_position)<SEUIL_BALL_CLOSE):
		#print "a"
	 	if (dist(me.but_position,me.ball_position)<SEUIL_BALL_TOO_CLOSE):
			#print "b"
			return me.aller_vers_ball
		else:
			#print "c"
			return me.alligne_sur_demi_cercle
	#print "d"
	return revenir_au_but(me)

def gardien_shoot_alea(me):
	
	if me.test_peut_shooter:
		return me.shoot_intercepter_contrecarE + me.shoot_alea

	else:
		return SoccerAction()

def gardien_shoot_vers_but(me):
	if me.test_peut_shooter:
		return me.shoot_intercepter_contrecarE + me.shoot_vers_but_adv

	else:
		return SoccerAction()
		
def gardien_complexe_1(me):
	return gardien_mouvement(me) + gardien_shoot_alea(me)	

def gardien_complexe_2(me):
	return gardien_mouvement(me) + gardien_shoot_vers_but(me)


def gardien_2(me):

	
	if (me.dist(me.but_position,me.ball_position)<SEUIL_BALL_CLOSE):
	 	if (me.dist(me.but_position,me.ball_position)<SEUIL_BALL_TOO_CLOSE):
			return revenir_au_but(me)
		else:
			return me.alligne_sur_demi_cercle
	else:
		if me.test_peut_shooter:
			return me.shoot_intercepter_contrecarE

		else:
			return me.aller_vers_ball + me.shoot_alea
	
	

FonceurStrat = SousStrat(fonceur)
GkStrat = SousStrat(gardien_complexe_2)
AllignerStrat = SousStrat(gardien_complexe_2)
DefStrat = SousStrat(def_mouvement_et_shoot)



class RandomStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self,"Random")
    def compute_strategy(self,state,id_team,id_player):
        
        if id_team==1:
            position_milieu_but=Vector2D(x=150.,y=45.)
            
        if id_team==2:
            position_milieu_but=Vector2D(x=0.,y=45.)
            
        vector_acc=state.ball.position-state.player_state(id_team,id_player).position
        
        if (state.ball.position.distance(state.player_state(id_team,id_player).position)<BALL_RADIUS+PLAYER_RADIUS):
            vector_shoot=position_milieu_but-state.ball.position
        else:
            vector_shoot=Vector2D()
        
        return SoccerAction(vector_acc,vector_shoot)
    

"""FonceurStrat =  SousStrat(fonceur ) ---> FonceurStrat.strat == fonceur,
 FonceurStrat.compute_strategy(state,idtema,idplayer) <--> fonceur(MyState(state,id_team,idplayer))

class Strat(BaseStrategy):
	def __init__(self,decideur):
		BaseStrategy.__init__(self,decideur.__name__)
		self.decideur = decideur
	def compute_strategy():
		return self.decideur(MyState(state,id_team,idplayer)


Fonceur = Strat(defenseur)

def defenseur(me):
		return SoccerAction().....

def startComplexce(me):
	if me...:
		return goal(me)
	if me....:
		return defenseur(me)+degager(me)

FonceurStrat = SousStrat(fonceur)

MaStratComplexe = """
