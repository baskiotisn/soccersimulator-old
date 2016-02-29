import soccersimulator, soccersimulator.settings
from soccersimulator import BaseStrategy, Vector2D, SoccerAction, settings

class App(object):
    def __init__(self,state,idteam,idplayer):
        self.state=state
        self.key=(idteam,idplayer)

    def __getattr__(self,name):
        return getattr(self.state,name)
        
    @property
    def my_position(self):
        return self.state.player_state(self.key[0],self.key[1]).position  # player_state(*self.key)
    @property
    def ball_position(self):
        return self.state.ball.position
        
    def shoot(self,force):
        return SoccerAction(Vector2D(),force-self.my_position)
    @property
    def ball_vitesse(self):
        return self.state.ball.vitesse

    def can_shoot(self):
        if self.my_position.distance(self.ball_position) <= (settings.BALL_RADIUS+settings.PLAYER_RADIUS):
            return 0
        return 1
    
    def vers_ball(self): #go vers balle sans frapper
        return SoccerAction(self.ball_position-self.my_position,Vector2D())
    
    def go_goal(self): #sans ballon
        return SoccerAction(Vector2D(settings.GAME_GOAL_HEIGHT/1.1,settings.GAME_HEIGHT/2)-self.my_position,Vector2D())
        #    return SoccerAction(Vector2D(settings.GAME_WIDTH-(settings.GAME_GOAL_HEIGHT/1.5),settings.GAME_HEIGHT/2)-self.my_position,Vector2D())
        
    def conduire_ball(self):
        return SoccerAction(self.state.ball.position-self.my_position,Vector2D(1.2,0))

    
    def is_ball_near_goal(self, pourcentage): #test si la balle est a WIDTH/pourcentage des cages
        if self.key[0] == 1:
            if self.ball_position.x > (settings.GAME_WIDTH)-(settings.GAME_WIDTH/pourcentage): #and self.ball_position.y < (settings.GAME_WIDTH)-settings.GAME_WIDTH/4 and self.ball_position.y > settings.GAME_WIDTH/4:
                return 0
            return 1
        
        if self.ball_position.x > -(settings.GAME_WIDTH/pourcentage-(settings.GAME_WIDTH)): #and self.ball_position.y < (settings.GAME_WIDTH)-settings.GAME_WIDTH/4 and self.ball_position.y > settings.GAME_WIDTH/4:
            return 0
        return 1

    
    def near_ball(self, pourcentage):
       if self.my_position.distance(self.ball_position) <= (settings.BALL_RADIUS+settings.PLAYER_RADIUS)+pourcentage*2.7:
           return 0
       return 1

    
    def is_in_goal(self): # test si le gardien est dans les cages 
        if self.my_position.distance(Vector2D(settings.GAME_GOAL_HEIGHT/1.1,settings.GAME_HEIGHT/2)) > settings.PLAYER_RADIUS:
            return 0
        
        if self.my_position.distance(Vector2D(settings.GAME_WIDTH-settings.GAME_GOAL_HEIGHT/1.1,settings.GAME_HEIGHT/2)) > settings.PLAYER_RADIUS: #Miror
            return 0
        return 1

    def is_out_goal(self): # test si gardien sort de sa zone et qu'il ne peut pas shooter
    
        if self.my_position.y >= (settings.GAME_HEIGHT/1.1)+settings.GAME_GOAL_HEIGHT/2 or self.my_position.x >= settings.GAME_GOAL_HEIGHT*1.5:
            return 0
        return 1
     #   if self.my_position.y >= (settings.GAME_HEIGHT/1.1)+settings.GAME_GOAL_HEIGHT/2 or self.my_position.x >= (settings.GAME_GOAL_HEIGHT*1.5): #miror
     #       return 0
     #   return 1
    
    def is_ball_in_my_camp(self):
        if self.key[0] == 1:
            if self.ball_position.x<(settings.GAME_WIDTH/2):
                return 0
        else:
            if self.ball_position.x>(settings.GAME_WIDTH/2):  #la balle a traverse la moitie de terrain
                return 0
        return 1

    
  
#func
#ball dans quel moitie de terrain
#

