# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 16:45:44 2016

@author: 3408247
"""
import math
import soccersimulator
from soccersimulator.settings import  *
from soccersimulator import BaseStrategy, SoccerAction, KeyboardStrategy
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
	self.state = state
     
        action=self.strat(MyState(self.state,idteam,idplayer))
	#print action
        if(idteam!=1):
	   action= miroir_action(action)

        #print action
        return action
    



### ATTAQUANT ###


def fonceur(me): #"me->objet state" #faire me bouger et shooter vers but de l'opposant
	#print("Fonceur", me.shoot_vers_but_adv, me.state._configs[(me.key[0],me.key[1])]._last_shoot)
	if me.test_peut_shooter:
	   return me.shoot(me.but_position_adv)
	else:
	   return me.aller(me.ball_position)

def fonceur_bis(me):
    if me.test_peut_shooter:
	return me.shoot_avec_angle_puissance(me.angle_player_but,10.)

    else:
	return me.courir_vers_ball


	


def fonceur_alea(me):
	return me.aller_vers_ball + me.shoot_alea

def fonceur_pass(me):
	#print(me.aller(me.ball_position))
	#print(me.shoot_vers_equipier_proche())

        if me.test_peut_shooter:
 	   return me.shoot_vers_equipier_proche

	else:
	   return me.aller(me.ball_position)


#Attaquant 1_VS_1 ou 2_VS_2
def shooteur_malin(me):
    if me.test_peut_shooter:

	if (me.dist_but_adv_ball>30):  #JE SUIS PRES DES BUTS ADV

		if dist(me.my_position,me.pos_adv)<25:   # SI ADV EST PROCHE/S'APPROCHE  DE MOI
			return me.shoot_malin  #SHOOT 
		else:
			return me.shoot_dribble  # CONTINUE A S'APPROCHER DES BUTS

	else: # JE SUIS LOIN DES BUTS
	 	return me.shoot_dribble  

    else: # PEUT PAS SHOOTER
	return me.courir_vers_ball 


### DEFENSEUR ###

# 1_VS_1 #

	
    
 

def def_mouvement_et_shoot(me):
	#print me.state._configs[(me.key[0],me.key[1])]._last_shoot

	if (me.ball_position.x<GAME_WIDTH/2):
	

		if me.test_peut_shooter:
		
			
			return me.shoot_vers_but_adv
		else:
									
			return me.aller_vers_ball 

	else:	
		
		return me.def_positionnement_defaut



#def def_mouvement_et_shoot_centre(me):



### GARDIEN ###

def revenir_au_but(me): #faire me revenir a la position milieu but 

		#if(me.key[0]==1):
   			return me.aller(me.but_position)
		#if(me.key[0]==2):
			#return me.aller(me.but_position)	

		#return SoccerAction()

	
def gardien_mouvement(me):

	
	if (dist(me.but_position,me.ball_position)<SEUIL_BALL_CLOSE):
		
	 	if (dist(me.but_position,me.ball_position)<SEUIL_BALL_TOO_CLOSE):
			
			return me.aller_vers_ball
		else:
			
			return me.alligne_sur_demi_cercle

	return revenir_au_but(me)

def gardien_shoot_alea(me):
	
	if me.test_peut_shooter:
		return  me.shoot_alea

	else:
		return gardien_mouvement(me)

def gardien_shoot_vers_but(me):
	if me.test_peut_shooter:
		return me.shoot_vers_but_adv

	else:
		return gardien_mouvement(me)
		


def gardien_2(me):

	
	if (dist(me.but_position,me.ball_position)<SEUIL_BALL_CLOSE):
	 	if (dist(me.but_position,me.ball_position)<SEUIL_BALL_TOO_CLOSE):
			return revenir_au_but(me)
		else:
			return me.alligne_sur_demi_cercle
	else:
		if me.test_peut_shooter:
			return me.shoot_intercepter_contrecarE

		else:
			return me.aller_vers_ball + me.shoot_alea


## SPECIALISATION DES JOUEURS POUR LES TOURNOIS ##	

def j_1vs1(me):
	
	if (me.ball_position.x<GAME_WIDTH/2): #SI DANS MA MOITIER DE TERRAIN

		if me.a_la_balle==2:  # SI ADV A LA BALLE
			if me.test_peut_shooter:
				return me.shoot_degager 
			else:
				return me.courir_vers_ball
		else:
			return shooteur_malin(me)  

	else: # DANS MOITIER ADV
		return shooteur_malin(me)

def j_2vs2(me):
	flag = me.key[0]==1 
	print me.state.step,me.key[1]
	if(me.ball_position.x<GAME_WIDTH/2): # DANS MA MOITIER
		print "la1"
		if me.a_la_balle==2:  # SI ADV A LA BALLE

			if me.test_peut_shooter:
				return me.shoot_vers_but_adv 

			else:
				print "la", me.courir_vers_ball
				return me.courir_vers_ball

		if me.a_la_balle==1: #JAI LA BALLE

			print "labis"
			if dist(me.my_position,me.pos_adv_plus_proche)<7:  #ADV FONCE SUR MOI
				return me.shoot_vers_equipier_proche # FAIRE PASSE
			else:
				return shooteur_malin(me) # CONTINUER NORMAL 

		else: #PERSONNE N'A LA BALLE 

			return shooteur_malin(me)
	else:
		print "later",me.my_position,me.pos_adv_plus_proche
		if dist(me.my_position,me.pos_adv_plus_proche)<7: #ADV FONCE SUR MOI
			return me.shoot_vers_equipier_proche # FAIRE PASSE
		else:
			print "ici",shooteur_malin(me)
			return shooteur_malin(me) # CONTINUER NORMAL 
def test(me):
	if me.test_peut_shooter:
		return me.shoot_vers_but_adv
	else:
		return me.courir_vers_ball

	
J_1vs1_Strat = SousStrat(j_1vs1)
Test_Strat = SousStrat(test)

J_2vs2_Strat = SousStrat(j_2vs2)
J_2vs2_Strat_bis= SousStrat(j_2vs2)
Hello = SousStrat(j_2vs2)
Hey = SousStrat(j_2vs2)

FonceurStrat = SousStrat(fonceur)
Gard_shoot_but = SousStrat(gardien_shoot_vers_but)
Gard_shoot_alea = SousStrat(gardien_shoot_alea)
DefStrat = SousStrat(def_mouvement_et_shoot)

keystrat1 = KeyboardStrategy()
keystrat1.add("a", Gard_shoot_alea)
keystrat1.add("b", Gard_shoot_but)

keystrat2= KeyboardStrategy()
keystrat2.add("c", FonceurStrat)
keystrat2.add("d", DefStrat)

milieustrat = KeyboardStrategy()
milieustrat.add("x", FonceurStrat)
milieustrat.add("w", DefStrat)





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
