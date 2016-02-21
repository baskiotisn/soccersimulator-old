from  soccersimulator import settings
from soccersimulator import  SoccerAction 
from Tools import *

# ATTAQUE BASIC T1
def attaquant1(Mystate):
    return Mystate.shoot_to_cage_t1() + Mystate.suivre_bal()                
       
# ATTAQUE BASIC T2 
def player_go(Mystate):
    
     if  Mystate.position_bal().x ==  (settings.GAME_WIDTH)/2  :
         return attaquant1(Mystate)
    
     elif(Mystate.pos_ball_attaque() == True) :
        return Mystate.go_to_the_middle()
        
     elif (Mystate.pos_ball_milieu() == True) :
        v = Vector2D(settings.GAME_WIDTH*3/4,settings.GAME_HEIGHT/2.)
        if Mystate.position_bal().x >  (settings.GAME_WIDTH*1.2)/2 :
            return Mystate.suivre_bal() + Mystate.shoot_to_cage_t1() 
        else :
            return Mystate.suivre_bal() + Mystate.shoot_to(v)
            
     else :
         return Mystate.shoot_bal_def() + Mystate.suivre_bal()
     
       
# ATTAQUE EN POINTE 
       
def attaque_pointe(Mystate):
    
    if Mystate.pos_ball_attaque() == True :
        return Mystate.shoot_to_cage_t1() + Mystate.suivre_bal()
        
    elif (Mystate.pos_ball_milieu() == True) :
        return Mystate.go_to_attack()

    else:
        return Mystate.suivre_bal_en_y()
        
# MILIEU DE TERRAIN
def milieu_centre(Mystate):
    
    if(Mystate.pos_ball_attaque() == True) :
        return Mystate.suivre_bal_en_y()
        
    elif (Mystate.pos_ball_milieu() == True) :
        v = Vector2D(settings.GAME_WIDTH*3/4,settings.GAME_HEIGHT/2.)
        if Mystate.position_bal().x >  (settings.GAME_WIDTH*1.2)/2 :
            return Mystate.suivre_bal() + Mystate.shoot_to_cage_t1() 
        else :
            return Mystate.suivre_bal() + Mystate.shoot_to(v)
            
    elif Mystate.pos_ball_goal() == True :
        return Mystate.go_to_the_middle()
        
    else:
        return Mystate.suivre_bal_en_y()
        
# DEFENSE BASIC T1
def defenseur1(Mystate):
    
    if( Mystate.pos_ball_defense() == True) :
        return Mystate.shoot_bal_def() + Mystate.suivre_bal()  
            
    elif(Mystate.pos_ball_attaque() == True) :
       return Mystate.go_to_defence()
  
    else : 
        return Mystate.suivre_bal_en_y()
        
# GOAL
def goal(Mystate):  
  
     if( Mystate.pos_ball_goal() == True) :
        return Mystate.shoot_bal_def() + Mystate.suivre_bal()
        
     else :
        return Mystate.go_to_goal()
    
    

# MIL ATT
def milieu_att(Mystate):

     if( Mystate.position_bal().x >=  (settings.GAME_WIDTH*2.5)/4  ):
        return attaque_pointe(Mystate)
        
     else :
        return milieu_centre(Mystate)
        
def test1(Mystate):   
    
    #if(Mystate.distance_of_cage() < 50 ):
    if Mystate.distance_players_t2():
        print("ok" )
        return Mystate.shoot_to_cage_t1()
    else:
        return Mystate.go_to_cage_with_ball()     
 
         
 #  """    a = random.uniform(0,30)
  #      if a > 2.5:
   # #        return Mystate.suivre_bal_en_y()
      #  else:
       #     return Mystate.shoot_to_cage_t1() + Mystate.suivre_bal()"""
        
        
        
        
        
        
        
        
        
        
        
