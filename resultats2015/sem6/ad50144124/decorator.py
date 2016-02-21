# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
"""
=========================player==================================
"""
class SoccerStateDecorator:
    def __init__(self, state, id_team, id_player, info):
        self.state=state
        self.id_team=id_team
        self.id_player=id_player
        self.info = info
        
    @property
    def pos(self):#position (vecteur)
        return self.state.player_state(self.id_team,self.id_player).position

    @property
    def d(self):#distance entre player et ball (float)
        return self.state.ball.position.distance(self.pos)
    
    @property
    def goal(self):#goal selon la team (vecteur)
        return Vector2D(150-(self.id_team-1)*150,45)

    @property   
    def d_vec(self):#distance (vecteur)
        return self.state.ball.position-self.state.player(self.id_team,self.id_player).position
        
        
        
    
"""
========================strategy===================================
"""
def random(mystate):
    return SoccerAction(Vector2D.create_random()-0.5,
                        Vector2D.create_random())

def fonceur(mystate):
    return SoccerAction((mystate.state.ball.position-mystate.state.player(mystate.id_team,mystate.id_player).position),
                            Vector2D(150,45)-mystate.state.ball.position)
                            
def QuickCatch(mystate):
    d=mystate.state.ball.position-mystate.state.player(mystate.id_team,mystate.id_player).position
    #print state.ball.position-state.player(2,0).position
    if mystate.state.ball.vitesse._x==0 and d.norm<2:
        d.scale(0.009)
    return SoccerAction(d,
                        Vector2D(0,45)-mystate.state.ball.position)
                        
def QuickCatch2v2(mystate):                  
    d=mystate.state.ball.position-mystate.state.player(mystate.id_team,mystate.id_player).position
    #print state.ball.position-state.player(2,0).position
    if mystate.state.ball.vitesse._x<0.1 and d.norm<0:
        d.scale(0.09)
    #print state.ball.vitesse
    return SoccerAction(d,
                        Vector2D(0,45)-mystate.state.ball.position)
                        
def QuickFollow(mystate):
    d=mystate.state.ball.position-mystate.state.player(mystate.id_team,mystate.id_player).position
    #print state.ball.position-state.player(2,0).position
    if d.norm>5 and mystate.state.ball.vitesse._x<0.001:
        d+=Vector2D(-50,20)
    elif mystate.state.ball.vitesse._x!=0 or mystate.state.ball.vitesse._y!=0 :
        v=mystate.state.ball.vitesse.norm
        p=0
        while(v>=0.00001):
            p+=v
            v-=v*0.06-(v**2)*0.01
            #print v
        v=mystate.state.ball.vitesse.norm
        vb=mystate.state.ball.vitesse 
        vb.scale(p/v)
        d+=vb
    elif d.norm<1:
        d.scale(0.09)
    return SoccerAction(d,
                        Vector2D(0,45)-mystate.state.ball.position)
                        
def Smart1v1(mystate):
    e_t = 3 - mystate.id_team
    #enemy team (int)
        
    b_p = mystate.state.ball.position
    #ball position (vector)
    b_v =mystate.state.ball.vitesse
    #ball vitesse (vector) 
    
    p = mystate.pos
    #position player (vector)
    d = mystate.d
    #distance player to ball (float)  
    d_vec = mystate.d_vec
    #distance player to ball (vector)
    goal = mystate.goal
    #position goal (vector)
    
    e_p = mystate.state.player(e_t,mystate.id_player).position
    #position enemie (vector)
    e_d = (b_p-e_p).norm
    #distance enemie player to ball (float)
    e_d_vec = b_p-e_p
    #distance enemie player to ball (vector)
    e_goal = Vector2D(150-(e_t-1)*150,45)
    #goal enemie (vector)
    if (d <= e_d) and (d>5 or b_v.norm>2) and b_v.norm>0.01:
        v=b_v.norm
        #vitesse ball norme
        p_fin=0
        #condition initiale position en norme
    
        while(v>=0.01):
            p_fin+=v
            v-= (v*0.06 + (v**2)*0.01)
        #calcule d'intégrale
        v=b_v.norm
        #réinitialisation
        vb=b_v
        #norme de vitesse
        vb.scale(p_fin/v*0.9)
        #rendre unitaire et scalaire norme de position, position relative à la fin par rapport à position actuelle (0.4 est la constant de correction)
        vb+=b_p
        #position absolue
        if vb.x<0:
            vb._x=-vb._x
        if vb.y<0:
            vb._y=-vb._y
        if vb.x>150:
            vb._x=300-vb._x
        if vb.y>90:
            vb._y=180-vb._y
        #reflextion
        return SoccerAction(vb-p, Vector2D(0,0))
    #si je suis plus proche et ball a une vitesse éleve ,calculer la position à la fin est chercher la ball 
        
    if (d <= e_d) and (d>2 and b_v.norm<=2):
        return SoccerAction(d_vec, Vector2D(0,0))
    #si je suis plus proche et ball est imoblile, chercher la ball
        

    if (d > e_d) and (d > 2):
        b_to_goal = e_goal-b_p
        #distance ball to e_goal (vector)
        b_to_goal_u = b_to_goal/b_to_goal.norm
        #rendre vector unitaire
        b_to_goal_u.scale(min(10,b_to_goal.norm-2))
        #se mettre à distance 10 par rapport à ball dans la direction de e_goal et éviter d'être trop proche de e_goal (en esperant enemie shoote ver e_goal)
        return SoccerAction(d_vec,Vector2D(0,0))
    # si j'ai moins de chance de ratrapper la ball plus rapide que l'autre, se mettre entre la ball et goal

    if goal-b_p < 12:

        return SoccerAction(d_vec, goal-b_p)
        #fonceur strategie
    #si je peux shooter et je suis plus proche de goal que enemie,foncer 
    
    if (d < 2) and ((goal-p).norm > (goal-e_p).norm) and (goal-p).norm>15:
        if b_p.y>45:
            s=90
        else:
            s=0  
        if (e_p-p).norm<10:
            s=Vector2D(p.x+10-(mystate.id_team-1)*20,s)-b_p
        else:
            s=goal-b_p
            s.scale(1.0/(goal-b_p).norm)
        return SoccerAction(d_vec,s)    
    #si j'ai la ball mais enemie est en face, essayer de faire une réflexion
    s=goal-b_p
    s.scale(1.0/(goal-b_p).norm)
    return SoccerAction(d_vec,s)
    #fonceur
   
    
    
def Smart2v2(mystate):

    e_t = 3 - mystate.id_team
    #enemy team (int)
        
    b_p = mystate.state.ball.position
    #ball position (vector)
    b_v =mystate.state.ball.vitesse
    #ball vitesse (vector) 
    
    
    p = mystate.pos
    #position player (vector)
    d = mystate.d
    #distance player to ball (float)  
    d_vec = mystate.d_vec
    #distance player to ball (vector)
    goal = mystate.goal
    #position goal (vector)
    
    e_p = mystate.state.player(e_t,mystate.id_player).position
    #position enemie (vector)
    e_d = (b_p-e_p).norm
    #distance enemie player to ball (float)
    e_d_vec = b_p-e_p
    #distance enemie player to ball (vector)
    e_goal = Vector2D(150-(e_t-1)*150,45)
    #goal enemie (vector)
    
    a_p = mystate.state.player(mystate.id_team,1-mystate.id_player).position
    #position allie (vector)
    a_d = (b_p-a_p).norm
    #distance allie (float)
    a_d_vec = b_p-a_p
    #distance allie (vector)
    
    ea_p = mystate.state.player(e_t,1-mystate.id_player).position
    #position enemie allie (vector)
    ea_d = (b_p-ea_p).norm
    #distance enemie allie (float)
    ea_d_vec = b_p-ea_p
    #distance enemie allie (vector)
    
    
    if a_d<e_d-0.2 and a_d<ea_d-0.2 and a_d<d-0.2 and ((e_goal-a_p).norm<(e_goal-e_p).norm or (e_goal-a_p).norm<(e_goal-ea_p).norm) and ((e_p-a_p).norm<5 or (ea_p-a_p).norm<5):
        if p.y>45:
            s=-20
        else:
            s=20
        return SoccerAction(d_vec+Vector2D(20-(mystate.id_team-1)*40,s),goal-b_p)
    #allie est le plus proche à ball, préparer à récupérer la passage
    
    if d<2 and d<e_d-0.2 and d<ea_d-0.2 and d<a_d-0.2 and ((e_goal-p).norm<(e_goal-e_p).norm or (e_goal-p).norm<(e_goal-ea_p).norm) and ((e_p-p).norm<5 or (ea_p-p).norm<5):
        s=a_p-b_p+Vector2D(10-(mystate.id_team-1)*20)
        s.scale(0.1)        
        return SoccerAction(d_vec,s)
    #passage
    
    return Smart1v1(mystate)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    