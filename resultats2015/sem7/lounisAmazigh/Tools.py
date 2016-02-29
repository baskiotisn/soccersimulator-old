#import soccersimulator
import math
import random
from  soccersimulator import settings
from soccersimulator import SoccerAction 
from soccersimulator import Vector2D

        
        ################ MIROIR    #####################

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
                    
class PlayerStateDecorator : 
    def __init__(self , state , id_team , id_player):
        self.state = state
        self.id_team = id_team
        self.id_player = id_player 
       

            
        ################ POSITION  #####################
   
    def position_bal(self) : 
        return self.state.ball.position
        
    def position_player(self):
        return self.state.player_state(self.id_team, self.id_player).position  
        
    def distance_of_bal(self):
        return self.state.player_state(self.id_team, self.id_player).position.distance(self.state.ball.position)     
    
    def distance_of_cage(self):
        return self.state.player_state(self.id_team, self.id_player).position.distance(Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2.))     
     
    def distance_player(self,idt,idp):
        return self.position_player().distance(self.state.player_state(idt,idp).position)
        
    def distance_players_t2(self):
        #list_dist = []
         #list_dist.add(self.distance_player(idt,idp),idt,idp)
        j = 0
        for (idt, idp) in self.state.players :
            if idt != self.id_team and self.distance_player(idt,idp) < 30 and (self.state.player_state(idt, idp).position.x >= self.position_player().x):
                j=j+1
        if j != 0:
            return True
        else :
            return False
            
    def position_attaquant(self):
        for (idt, idp) in self.state.players :
            if idt == self.id_team and idp== 0:
                print("La")
                return self.state.player_state(idt, idp).position
            else :
                continue
    def pos_ball_attaque(self):
        if(self.position_bal().x >= (settings.GAME_WIDTH*3)/4 ) :
            return True
        else :
            return False
            
    def pos_ball_milieu(self):
        if(self.position_bal().x <= (settings.GAME_WIDTH*1.08)/2) and (self.position_bal().x >= (settings.GAME_WIDTH*1.2)/4):
            return True
        else : 
            return False
            
    def pos_ball_defense(self):
        if(self.position_bal().x <= (settings.GAME_WIDTH/4)) and (self.position_bal().x >= (settings.GAME_WIDTH/16)):
            return True
        else : 
            return False
            
    def pos_ball_goal(self):
        if(self.position_bal().x <= (settings.GAME_WIDTH/10)) and (self.position_bal().y <= (settings.GAME_HEIGHT*3/4)) and (self.position_bal().y >= (settings.GAME_HEIGHT/4)) :
            return True
        else : 
            return False
    def pos_ball_AD(self):
        if(self.position_bal().x >= settings.GAME_WIDTH/2) and (self.position_bal().y <= settings.GAME_HEIGHT/2) :
            return True
        else : 
            return False
            
    def pos_ball_AG(self):
        if(self.position_bal().x >= settings.GAME_WIDTH/2) and (self.position_bal().y >= settings.GAME_HEIGHT/2) :
            return True
        else : 
            return False
            
    def pos_ball_DD(self):
        if(self.position_bal().x <= settings.GAME_WIDTH/2) and (self.position_bal().y <= settings.GAME_HEIGHT/2) :
            return True
        else : 
            return False
        
    def pos_ball_DG(self):
        if(self.position_bal().x <= settings.GAME_WIDTH/2) and (self.position_bal().y >= settings.GAME_HEIGHT/2) :
            return True
        else : 
            return False
            
    def ball_est_proche(self):
        if self.distance_of_bal() < 20: 
            return True
        else: 
            return False
            
    def ball_is_goal_t2(self):
        if self.position_bal().x >=  (settings.GAME_WIDTH*7)/8 :
            return True 
        else : 
            return False
       ############## DEPLACEMENT ########################
       
    def stop(self):
        return SoccerAction()
       
    def retour_position(self, v):
         return SoccerAction(v - self.position_player(),Vector2D())
        
    def suivre_bal(self) : 
        return SoccerAction(self.position_bal()-self.position_player() , self.no_shoot())
        
    def suivre_bal_en_y(self) :
        return SoccerAction(Vector2D(0,(self.position_bal().y - self.position_player().y)),Vector2D())
        
    def suivre_bal_en_x(self) : 
        return SoccerAction(Vector2D((self.position_bal().x - self.position_player().x),0),Vector2D())  
    
    def go_to_the_middle(self):
        v = Vector2D(settings.GAME_WIDTH/2,settings.GAME_HEIGHT/2.)
        return self.retour_position(v)
            
    def go_to_attack(self):
        v = Vector2D(settings.GAME_WIDTH*3/4,settings.GAME_HEIGHT/2.)
        return self.retour_position(v)
        
            
    
    def go_to_defence(self):
        v= Vector2D(settings.GAME_WIDTH*0.5/4,settings.GAME_HEIGHT/2.)
        return self.retour_position(v)
   

    def go_to_goal(self):
        v= Vector2D(0,settings.GAME_HEIGHT/2.)
        if(self.id_team == 1):
            return self.retour_position(v)
        else :
            return self.retour_position(v)
            
    def go_to_left(self):
        v= Vector2D(self.position_player().x,settings.GAME_HEIGHT*3/4.)
        return self.retour_position(v)
            
            ###### deplacement avec la balle #######
            
    def go_to_cage_with_ball(self):
       # a = random.uniform(0,1) - 0.2
        v = Vector2D(angle =0 ,norm = 2)
        if(self.position_bal().y > settings.GAME_HEIGHT/2) : 
             v = Vector2D(angle =-0.5 ,norm = 1.5)
        else :
            v = Vector2D(angle =0.5 ,norm = 1.5)
        if(self.can_shoot()==True):
            return self.shoot_to_polar(v)
        else:
            return self.suivre_bal()
            
    def foncer_vers_les_but(self):
        if self.can_shoot() == True:
            v = Vector2D(settings.GAME_WIDTH - self.position_player().x , (settings.GAME_HEIGHT)/2 - self.position_player().y ).normalize().scale(2)
            return SoccerAction( Vector2D() , v )
        else :
            return self.suivre_bal()
            
    def foncer_tout_droit(self):
         if self.can_shoot() == True:
            v = Vector2D(settings.GAME_WIDTH - self.position_player().x,0 ).normalize().scale(2)
            return SoccerAction( Vector2D() , v )
         else :
            return self.suivre_bal()

    ############## SHOOT ###########################
        
    def no_shoot(self):
        return Vector2D(x=0,y=0)
        
    def can_shoot(self):
        if(self.distance_of_bal() < settings.PLAYER_RADIUS + settings.BALL_RADIUS):
            return True
        else :
            return False
            
    def shoot_to(self, v):
        v1 = (v - self.position_player())
        return SoccerAction( self.position_bal()-self.position_player() ,  v1)
        
    def shoot_to_polar(self, v):
         return SoccerAction( self.position_bal()-self.position_player() ,  v)
         
 
    def shoot_to_cage_t1(self):
        if self.can_shoot() == True:
            return SoccerAction( self.position_bal()-self.position_player() , Vector2D(settings.GAME_WIDTH , (settings.GAME_HEIGHT)/2) - self.position_player())
        else :
            return SoccerAction(self.position_bal()-self.position_player(),self.no_shoot())
            
    def shoot_rand(self) :
        a = random.uniform(0,1) - 0.5
        u = (self.position_player().x*self.position_player().x) + (settings.GAME_HEIGHT/2 - self.position_player().y)*(settings.GAME_HEIGHT/2 - self.position_player().y) 
        d = math.sqrt(u)
        v = Vector2D(angle = a , norm = d ) 
        if self.can_shoot() == True:
            return SoccerAction(self.position_bal()-self.position_player(), v)
        else :
            return SoccerAction(self.position_bal()-self.position_player(),self.no_shoot())
        
    def shoot_bal( self):
        if(self.can_shoot() == True):
            return self.shoot_to_cage_t1()
        else :
            return self.stop()
            
    def small_shoot(self):
        if(self.can_shoot() == True):
            return SoccerAction( self.position_bal()-self.position_player() , Vector2D(settings.GAME_WIDTH , (settings.GAME_HEIGHT)/6) - self.position_player())
        else:
            return self.stop()
    
    def shoot_bal_def(self) : 
        if(self.can_shoot() == True):
            return self.shoot_rand() 
        else :
            return self.stop()
            
    ############# PASS #####################
            
    def pass_to_attaquant(self):
        if(self.position_attaquant() == Vector2D()):
            return self.foncer_tout_droit()
        else :
            v = Vector2D(self.position_attaquant().x - self.position_player().x , self.position_attaquant().y - self.position_player().y).normalize().scale(4)
            if(self.can_shoot() == True):
                return SoccerAction(Vector2D() , v)
            else : 
                return SoccerAction(self.position_bal()-self.position_player(),self.no_shoot())
        
        
   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
