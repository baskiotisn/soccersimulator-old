import soccersimulator
from soccersimulator import BaseStrategy, Vector2D, SoccerAction, settings
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Player, SoccerTournament

# Si le joueur est dans le rayon de la balle, il tire
def peutShooter(vjoueur,vballe):
	return (vballe.distance(vjoueur)) < (settings.PLAYER_RADIUS + settings.BALL_RADIUS) 

def passeOuShoot(vjoueur, vballe, id_team):
	if(id_team == 1): 
		if(vballe.x > settings.GAME_WIDTH - 5): #Si on est loin des buts, on fait des petites passes
			return SoccerAction(vballe - vjoueur, (Vector2D(settings.GAME_WIDTH, settings.GAME_HEIGHT / 2) - vjoueur) * 0.03)
		else: #Sinon, on tire
                	return SoccerAction(vballe - vjoueur, Vector2D(settings.GAME_WIDTH, settings.GAME_HEIGHT / 2) - vjoueur)
	else:
		if(vballe.x < 5): #Si on est loin des buts, on fait des petites passes
			return SoccerAction(vballe - vjoueur, (Vector2D(0, settings.GAME_HEIGHT / 2) - vjoueur) * 0.03)
		else: #Sinon, on tire
                	return SoccerAction(vballe - vjoueur, Vector2D(0, settings.GAME_HEIGHT / 2) - vjoueur)

 #Si on peut ni tirer ni passer, on court vers la balle
def courirVersBalle(vjoueur,vballe):
	return SoccerAction(vballe - vjoueur, Vector2D(0,0))

#Si le joueur est dans sa zone defensive, il shoote
def peutShooterDefensegauche(vballe,vjoueur,id_team):
	if(id_team == 1):
		return vballe.x < 35
	else:
		return vballe.x > 115

def peutShooterDefensedroit(vballe,vjoueur,id_team):
	if(id_team == 1):
		return vballe.x < 50
	else:
		return vballe.x > 100

def peutShooterDefense(vballe,vjoueur,id_team):
	if(id_team == 1):
		return vballe.x < 35
	else:
		return vballe.x > 115



#Si le milieu peut shooter, il shoote
def peutShooterMilieu(vballe,vjoueur,id_team):
	if(id_team == 1):
		return (vballe.x > 35) 
	else:
		return (vballe.x < settings.GAME_WIDTH - 35) 


#Si la balle est dans la zone du defenseur, il shoote
def shootDefense(vjoueur,vballe,id_team):
	if(id_team == 1):
            	if (peutShooter(vjoueur,vballe)):
			return SoccerAction(vballe - vjoueur, Vector2D(settings.GAME_WIDTH, settings.GAME_HEIGHT / 2) - vjoueur)
		else: 
			return SoccerAction(vballe - vjoueur, Vector2D(0,0))
	else:
	
		if(peutShooter(vjoueur,vballe)):
                	return SoccerAction(vballe - vjoueur, Vector2D(0, settings.GAME_HEIGHT / 2) - vjoueur)
            	else:
                	return SoccerAction(vballe - vjoueur, Vector2D(0,0)) 



def replacementDefense(vjoueur,vballe,id_team):
	if (id_team == 1):
		return SoccerAction(Vector2D(10, settings.GAME_HEIGHT / 2) - vjoueur, Vector2D(0,0))
	else:
		return SoccerAction(Vector2D(settings.GAME_WIDTH - 10, settings.GAME_HEIGHT / 2) - vjoueur, Vector2D(0,0)) #le defenseur se replace en defense si la balle sort de sa zone defensive

def replacementDefenseurGauche(vjoueur,vballe,id_team):
	if (id_team == 1):
		return SoccerAction(Vector2D(10, settings.GAME_HEIGHT/2 + 5) - vjoueur, Vector2D(0,0))
	else:
		return SoccerAction(Vector2D(settings.GAME_WIDTH - 10, settings.GAME_HEIGHT/2 + 5) - vjoueur, Vector2D(0,0)) #le defenseur gauche se replace a sa position

def replacementDefenseurDroit(vjoueur,vballe,id_team):
	if (id_team == 1):
		return SoccerAction(Vector2D(10, settings.GAME_HEIGHT/2 - 5) - vjoueur, Vector2D(0,0))
	else:
		return SoccerAction(Vector2D(settings.GAME_WIDTH - 10, settings.GAME_HEIGHT/2 - 5) - vjoueur, Vector2D(0,0)) #le defenseur droit se replace a sa position


def replacementMilieu(vjoueur,vballe,id_team):
	if (id_team == 1):
		return SoccerAction(Vector2D(50, settings.GAME_HEIGHT/2) - vjoueur, Vector2D(0,0))
	else:
		return SoccerAction(Vector2D(settings.GAME_WIDTH - 50, settings.GAME_HEIGHT/2) - vjoueur, Vector2D(0,0)) #Prend sa position de contre attaquant

		


class attaquantcentral(BaseStrategy):
	def __init__(self):
        	BaseStrategy.__init__(self, "Aleatoire")
        
    
	def compute_strategy(self, state, id_team, id_p1ayer):
        	p = state.player_state(id_team, id_p1ayer)
        	vballe = state.ball.position
        	vjoueur = p.position
            
		if(peutShooter(vjoueur, vballe)):
			return passeOuShoot(vjoueur, vballe, id_team)	
 		else:
             		return courirVersBalle(vjoueur, vballe) #Classe du fonceur



class defenseurcentral(BaseStrategy): #Strategie du defenseur central
	def __init__(self):
        	BaseStrategy.__init__(self, "Aleatoire")
	    
    	def compute_strategy(self, state, id_team, id_p1ayer):
        	p = state.player_state(id_team, id_p1ayer)
        	vballe = state.ball.position
        	vjoueur = p.position
        
		if(peutShooterDefense(vballe,vjoueur,id_team)):
			return shootDefense(vjoueur,vballe,id_team)
		return replacementDefense(vjoueur,vballe,id_team)




class defenseurgauche(BaseStrategy): #Strategie du defenseur gauche
	def __init__(self):
        	BaseStrategy.__init__(self, "Aleatoire")
	    
    	def compute_strategy(self, state, id_team, id_p1ayer):
        	p = state.player_state(id_team, id_p1ayer)
        	vballe = state.ball.position
        	vjoueur = p.position
        
		if(peutShooterDefense(vballe,vjoueur,id_team)):
			return shootDefense(vjoueur,vballe,id_team)
		return replacementDefenseurGauche(vjoueur,vballe,id_team)


class defenseurdroit6(BaseStrategy): #Strategie du defenseur droit
	def __init__(self):
        	BaseStrategy.__init__(self, "Aleatoire")
	    
    	def compute_strategy(self, state, id_team, id_p1ayer):
        	p = state.player_state(id_team, id_p1ayer)
        	vballe = state.ball.position
        	vjoueur = p.position
        
		if(peutShooterDefensedroit(vballe,vjoueur,id_team)):
			return shootDefense(vjoueur,vballe,id_team)
		return replacementDefenseurDroit(vjoueur,vballe,id_team)

class defenseurdroit(BaseStrategy): #Strategie du defenseur droit
	def __init__(self):
        	BaseStrategy.__init__(self, "Aleatoire")
	    
    	def compute_strategy(self, state, id_team, id_p1ayer):
        	p = state.player_state(id_team, id_p1ayer)
        	vballe = state.ball.position
        	vjoueur = p.position
        
		if(peutShooterDefense(vballe,vjoueur,id_team)):
			return shootDefense(vjoueur,vballe,id_team)
		return replacementDefenseurDroit(vjoueur,vballe,id_team) 

class Milieu(BaseStrategy): #Strategie de contre attaque
	def __init__(self):
        	BaseStrategy.__init__(self, "Aleatoire")
	    
    	def compute_strategy(self, state, id_team, id_p1ayer):
        	p = state.player_state(id_team, id_p1ayer)
        	vballe = state.ball.position
        	vjoueur = p.position
        
		if(peutShooterMilieu(vballe,vjoueur,id_team)):
			return shootDefense(vjoueur,vballe,id_team)
		return replacementMilieu(vjoueur,vballe,id_team)









       

               


