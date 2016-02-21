# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 16:38:24 2016

@author: 3408247
"""
import math
import soccersimulator
from soccersimulator.settings import  *
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from random import uniform

DCERCLE_RAYON = 10

def miroir_pos(p):
    return Vector2D(GAME_WIDTH-p.x,p.y)

def miroir_vect(v):
    return Vector2D(-v.x,v.y)

def miroir_action(act):
    return SoccerAction(miroir_vect(act.acceleration),miroir_vect(act.shoot))

def miroir_state(etat):
    etatcpy=etat.copy()

    etatcpy.ball.position=miroir_pos(etat.ball.position)
    etatcpy.ball.vitesse=miroir_vect(etat.ball.vitesse)

    for(idt,idp) in etat.players:
	etatcpy.player(idt,idp).position=miroir_pos(etat.player(idt,idp).position)
	etatcpy.player(idt,idp).vitesse=miroir_vect(etat.player(idt,idp).vitesse)
    
    return etatcpy

def dist(u,v): #"u->Vector2D, v->Vector2D" #retourne float->la distance entre u et v
	return u.distance(v)

class MyState(object):
    def __init__(self,state,idteam,idplayer):
        self.state = state    #ajouter le miroir ici option 1
        self.key = (idteam,idplayer)
 
        if (idteam!=1):
	    self.state=miroir_state(self.state)


### POSITIONS ###

    @property
    def my_position(self): #retourne Vector2D->la position de self (ici joueur)
        return self.state.player_state(self.key[0],self.key[1]).position
        #equivalent a self.state.player_state(self.key[0],self.key[1])
    
    @property    
    def ball_position(self): #retoune Vector2D->la position de self (ici ball)
        return self.state.ball.position

    @property
    def but_position(self): #retourne Vector2D->la position_milieu du but 
	
		return Vector2D(x=3,y=GAME_HEIGHT/2)


    @property   
    def but_position_adv(self): #retourne Vector2D->la position_milieu du but de l'adversaire

		return Vector2D(x=GAME_WIDTH-3,y=GAME_HEIGHT/2)


### DISTANCES ###

  
    
    @property
    def dist_player_ball(self): #distance entre player et ball
	return dist(self.my_position,self.ball_position)

    @property
    def dist_but_ball(self): #distance entre but et ball
	return dist(self.but_position,ball_position)

    @property
    def dist_but_adv_ball(self): #distance entre but_adv et ball
	return dist(self.but_position_adv,ball_position)


    def dist_player_equipier(self,num):
	return dist(self.my_position,self.state.player(1,num).position)

	

### ANGLES ###

    @property
    def angle_ball_but(self):

	vecteur=self.ball_position-(self.but_position)

	return vecteur.angle

    @property
    def angle_player_but(self):

	vecteur=self.my_position-(self.but_position)

	return vecteur.angle
        

### MOUVEMENTS ###

    def aller(self,p): #"self->vector2D, p->vector2D" #retourne SoccerAction->faire bouger self jusqu'a p ; pas de shoot
        return SoccerAction(p-self.my_position,Vector2D())

    @property
    def aller_vers_but_adv(self):
	return self.aller(self.but_position_adv)

    @property
    def aller_vers_ball(self):
        return self.aller(self.ball_position)
            
    def aller_avec_angle_norme(self,theta,norme):
	dep=Vector2D(angle=theta,norm=norme)
	return SoccerAction(dep,Vector2D())

    @property
    def alligne_sur_demi_cercle(self):
	ux=(math.cos(self.angle_ball_but))*(DCERCLE_RAYON)
	uy=(math.sin(self.angle_ball_but))*(DCERCLE_RAYON)
	
	pos_x=self.but_position.x+ux
	pos_y=self.but_position.y+uy
	return self.aller(Vector2D(pos_x,pos_y))


    def placer_entre_ball_but(self,x_):
	vecteur_but_ball=self.ball_position-self.but_position
	y_=(((vecteur_but_ball.y)/(vecteur_but_ball.x))*(x_-self.ball_position.x))+self.ball_position.y	
	vect=Vector2D(x=x_,y=y_)
   
        return self.aller(vect)

    @property 
    def def_positionnement_defaut(self):
	return self.placer_entre_ball_but(GAME_WIDTH/4)
	
    
  #  @property 
   # def def_defaut_pos(self):   #placer defenseur entre ball et but sur x_fixe GAME_WIDTH/4
#	x_=GAME_WIDTH/4
#	vecteur_but_ball=self.ball_position-self.but_position
#	y_=(((vecteur_but_ball.y)/(vecteur_but_ball.x))*(x_-self.ball_position.x))+self.ball_position.y	
#
#	return Vector2D(x=x_,y=y_)

#    @property
  #  def def_positionnement_defaut(self):
#	return self.aller(self.def_defaut_pos)
	
    #@property
    #def alligner_entre_ball_but(self):
	

### RADAR ###

    @property
    def pos_equipier_plus_proche(self):
	d_min=999
	vecteur=Vector2D(0,0)
	liste_equipiers=[(it, ip) for (it, ip) in self.state.players if (it ==self.key[0] and ip!=self.key[1])] 
	for p in liste_equipiers:
		d=self.dist_player_equipier(p[1])
		if d<d_min:
	           d_min=d
                   vecteur=self.state.player(it,p[1]).position 
	
	return vecteur


    @property
    def pos_adv_plus_proche(self):
	d_min=999
	vecteur=Vector2D(0,0)
	liste_equipiers=[(it, ip) for (it, ip) in self.state.players if (it!=self.key[0])] 
	for p in liste_equipiers:
		d=self.dist_player_equipier(p[1])
		if d<d_min:
	           d_min=d
                   vecteur=self.state.player(it,p[1]).position 
	
	return vecteur
	

### SHOOTS ###

    @property 
    def test_peut_shooter(self):
	return ((self.dist_player_ball)<BALL_RADIUS+PLAYER_RADIUS)

    #def test_peut_shooter_tours(self):
        
    def shoot(self,p): #pas de mouvement; faire shooter dans la direction p - self
        return SoccerAction(Vector2D(),p-self.my_position)
    
    @property
    def shoot_alea(self):
	angleu=uniform(-3.14/2,3.14/2)
	normeu=uniform(1.,maxBallAcceleration)
        return SoccerAction(Vector2D(),Vector2D(angle=angleu,norm=normeu))

    #comment shooter tres fort aleatoirement ? Decorateur thingy ? Specialisation ?
  
    @property
    def shoot_vers_but_adv(self):
         return self.shoot(self.but_position_adv)

    def shoot_avec_angle_puissance(self,theta,puissance):
	shot=Vector2D(angle=theta,norm=puissance)
	return SoccerAction(Vector2D(),shot)

    @property
    def shoot_intercepter_contrecarE(self):
	vect_input=self.state.ball.vitesse
	vect_output_x=-vect_input.x
	vect_output_y=-vect_input.y
	vect_output=Vector2D(vect_output_x,vect_output_y)

	return SoccerAction(Vector2D(),vect_output)

    @property 
    def shoot_vers_equipier_proche(self):
	return self.shoot(self.pos_equipier_plus_proche)
    
