from zone import *

def MiroirState(state):
    miroir = state.copy()
    miroir.ball.position = terrain.miroir_point(state.ball.position)
    miroir.ball.vitesse = terrain.miroir_vecteur(state.ball.vitesse)
    for (it,ip) in miroir.players:
        miroir.player_state(it,ip).position = terrain.miroir_point(miroir.player_state(it,ip).position)
    return miroir

def MiroirSoccerAction(action):
    return SoccerAction(terrain.miroir_vecteur(action.acceleration),terrain.miroir_vecteur(action.shoot))
        
