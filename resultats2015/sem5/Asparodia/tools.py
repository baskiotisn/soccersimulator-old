import random
import math
import soccersimulator
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Player, SoccerTournament
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator.settings import *

class PlayerStateDeco:
	def __init__(self,state, id_team, id_player):
		self.state=state
		self.id_team=id_team
		self.id_player=id_player
	@property
	def ball_pos(self):
		return self.state.ball.position
	
	def pos(self):
		return self.state.player_state(self.id_team,self.id_player).position
	
	def pos_player(self,idteam,idplayer):
		return self.state.player_state(idteam,idplayer).position
	@property
	def cible(self):
		if(self.id_team==1):
			
            		return Vector2D(GAME_WIDTH, GAME_HEIGHT/2.)-self.pos()
        	else:
        		
            		return self.pos()-Vector2D(GAME_WIDTH, GAME_HEIGHT/2.)
	

	def dist_ball(self):
		return self.ball_pos.distance(self.pos())
	

	def suivre_balle(self):
    		return SoccerAction(self.ball_pos-self.pos(), Vector2D(0,0))
    	
    	def campeur(self):
    		if(self.id_team==1):
    			camping=Vector2D(105,self.pos().y)
    			return SoccerAction(camping-self.pos(),Vector2D(0,0))
    		else:
    			camping=Vector2D(GAME_WIDTH-105,self.pos().y)
    			return SoccerAction(camping-self.pos(),Vector2D(0,0))
    	
	def shoot(self):
		if(self.dist_ball()<(PLAYER_RADIUS + BALL_RADIUS)):
        		return SoccerAction(0, self.cible)
    		else:
    			return SoccerAction()
	def shoot_def(self):
		if(self.dist_ball()<(PLAYER_RADIUS + BALL_RADIUS)):
			
			cible_def=self.cible
		
			cible_def.angle = random.randint(-1,1)*185
			if(cible_def.angle==0):
				cible_def.angle=185
			
			
        		return SoccerAction(0,cible_def)
    		else:
    			return SoccerAction()
    			
	
            		
            		
    	def get_adv_proche(self):
        	return sorted([ (self.pos().distance(self.pos_player(id_team,id_player)),id_team,id_player) for (id_team, id_player) in self.state.players if id_team !=self.id_team])
        
    	def get_copain_proche(self):
        	return sorted([ (self.pos().distance(self.pos_player(id_team,id_player)),id_team,id_player) for (id_team, id_player) in self.state.players if id_team ==self.id_team])
        	
    	def distance_adv_proche(self):
        	
        	liste_adv=self.get_adv_proche()
        	
        	(dist,idteam,idplayer)=liste_adv[0]
        	return dist
        def distance_copain_proche(self):
        	
        	liste_copain=self.get_copain_proche()
        	
        	(dist,idteam,idplayer)=liste_copain[1]
        	return dist
        	
    	def passe(self):
        	liste_copain=self.get_copain_proche()
        	(a,it,ip)=liste_copain[1]
		if(self.dist_ball()<(PLAYER_RADIUS + BALL_RADIUS)):
			passe=self.state.player_state(it,ip).position-self.pos()
			passe.norm=1
	        	return SoccerAction(0, passe)
	    	else:
	    		return SoccerAction()

	def defense(self):
		if(self.id_team==1):
			back=Vector2D(20, GAME_HEIGHT/2.)-self.pos()
			if(self.ball_pos.x < GAME_WIDTH/2):
				return self.suivre_balle()+ self.shoot_def()
			else:
				return SoccerAction(back, Vector2D())
		
		else:
			back=Vector2D(GAME_WIDTH-20, GAME_HEIGHT/2.)-self.pos()
			
			if(self.ball_pos.x > GAME_WIDTH/2):
				return self.suivre_balle()+ self.shoot_def()
			else:
				return SoccerAction(back, Vector2D())
		
        def utilitaire(self):
      
        	if((self.distance_adv_proche())<10 and (self.distance_copain_proche())<15):
        		return self.defense()
        	
        	return self.suivre_balle()+self.passe()
        			
        def campe(self):
        	if(self.id_team==1):
        		if(self.ball_pos.x > 3*GAME_WIDTH/4 or self.dist_ball()<(PLAYER_RADIUS + BALL_RADIUS)*15 ):
        			return self.suivre_balle()+self.shoot()
        		else:
        			return self.campeur()+self.shoot()
	 	else:
	 		if(self.ball_pos.x < GAME_WIDTH/4 or self.dist_ball()<(PLAYER_RADIUS + BALL_RADIUS)*15 ):
	 			return self.suivre_balle()+self.shoot()
	 		else:
	 			
				return self.campeur()+self.shoot()
		

#def suivre(state, id_team, id_player):
#   bal=state.ball
#    p=state.player_state(id_team,id_player)
#    return SoccerAction(bal.position-p.position, Vector2D(0,0))

    
#def shoot(state, id_team, id_player,cible):
#    bal=state.ball
#    p=state.player_state(id_team,id_player)
    
#    if(p.position.distance(bal.position)<(PLAYER_RADIUS + BALL_RADIUS)):
#        return SoccerAction(0, cible)
#    return SoccerAction()

#def retour_goal(state, id_team,id_player):
#    bal=state.ball
#    p=state.player_state(id_team,id_player)
#    if(id_team==1):
#        point_de_retour= Vector2D(10,GAME_HEIGHT/2.)
#    else:
#        point_de_retour= Vector2D(GAME_WIDTH-10,GAME_HEIGHT/2.)

#    return SoccerAction(point_de_retour-p.position,Vector2D(0.,0.))

#def defense( state,id_team,id_player,cible):
#        bal=state.ball
#        p=state.player_state(id_team,id_player)
#        cible_local=cible
        
#        cible_local.angle=random.random()*math.pi
       
#        if(id_team==1):
#            if(bal.position.x<GAME_WIDTH/2):
#                return suivre(state, id_team,id_player) + shoot(state,id_team,id_player,cible_local)
#            else:
#                return retour_goal(state, id_team,id_player)
#        else:
#            if(bal.position.x>GAME_WIDTH/2):
#                return suivre(state, id_team,id_player) + shoot(state,id_team,id_player,cible_local)
#            else:
#                return retour_goal(state, id_team,id_player)
                
