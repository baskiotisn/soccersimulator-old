# -*-coding: utf8 -*
import soccersimulator
from soccersimulator.settings import *
from soccersimulator import SoccerAction, SoccerState, Vector2D, Player
from math import pi
from random import *

#DEFINITION DES CONSTANTES

GOAL_SURFACE_WIDTH = GAME_WIDTH/9.
THIRD_WIDTH = GAME_WIDTH - 50
MEDIUM_WIDTH = GAME_WIDTH/2.
QUARTER_WIDTH = MEDIUM_WIDTH/2.
THREE_QUARTER_WIDTH = MEDIUM_WIDTH + QUARTER_WIDTH
MEDIUM_HEIGHT = GAME_HEIGHT/2.
QUARTER_HEIGHT = MEDIUM_HEIGHT/2.
THREE_QUARTER_HEIGHT = MEDIUM_HEIGHT + QUARTER_HEIGHT

######################################################################################################
#                     Mystate: mes petites strategies ;)
######################################################################################################

class Mystate:
    def __init__(self, state, id_team, id_player):
        self.state = state
        self.id_team = id_team
        self.id_player =id_player

    @property
    def do_nothing(self):
        """Ne fais rien ;)"""
        return SoccerAction()
   
    @property
    def position_ball(self):
        """Position de la balle"""
        return self.state.ball.position

    @property
    def vitesse_ball(self):
        """Vitesse de la balle"""
        return self.state.ball.vitesse

    @property
    def position_player(self):
        """Position du joueur"""
        return self.state.player_state(self.id_team, self.id_player).position
    
    @property
    def nbj_team4(self):
        """Nombres de joueurs de la team2"""
        return self.state.nb_players(4)

    @property
    def position_player_adv(self):
        """La position du joueur le plus proche"""
        if self.id_team == 1:
            return self.state.player_state(2, 0).position
        else:
            return self.state.player_state(1, 0).position

                                                                      ########################################
    @property
    def position_defenseur(self):
        """La position du defenseur dans le terrain"""
        return self.state.player_state(self.id_team, self.id_player == 0).position
    
    @property
    def position_attaquant_g(self):
        """La position de l'attaquant gauche sur le terrain"""
        return self.state.player_state(self.id_team, self.id_player == 1).position
    
    @property
    def position_gardien(self):
        """La position du gardien dans le terrain"""
        return self.state.player_state(self.id_team, self.id_player == 2).position
    
    @property
    def position_attaquant_d(self):
        """La position de l'attaquant droit sur le terrain"""
        return self.state.player_state(self.id_team, self.id_player == 3).position
                                                                    #########################################
    @property
    def goal_un(self):
        """Position du goal1, c'est à dire à gauche"""
        return Vector2D(x = 0, y = MEDIUM_HEIGHT)

    @property
    def goal_deux_coin_bas(self):
        """Position du coin bas du goal1"""
        return Vector2D(x = GAME_WIDTH, y = MEDIUM_HEIGHT + 3)

    @property
    def goal_deux_coin_haut(self):
        """Position du coin haut du goal1"""
        return Vector2D(x = GAME_WIDTH, y = MEDIUM_HEIGHT - 3)

    @property
    def goal_deux(self):
        """Position du goal2, c'est à dire à droite"""
        return Vector2D(x = GAME_WIDTH, y = MEDIUM_HEIGHT)
    
#######################
    @property
    def angle_0(self):
        """Complètement vers la droite"""
        return Vector2D(angle = 0, norm = 1)

    @property
    def angle_pi6(self):
        """Tourne d'un angle de pi/6"""
        return Vector2D(angle = pi/6, norm = 1)

    @property
    def angle_pi4(self):
        """D'un angle de pi/4"""
        return Vector2D(angle = pi/4, norm = 1)

    @property
    def angle_pi(self):
        """D'un angle de pi"""
        return Vector2D(angle = pi, norm = 1)
#######################

    @property
    def distance_player_ball(self):
        """Distance entre le joueur et la balle	"""
        return self.position_ball.distance(self.position_player)

    @property
    def distance_lalya1(self):
        """Distance entre le joueur de la team1 et celui de la team2 pour l'équipe lalya1"""
        return self.position_player.distance(self.position_player_adv)

    @property
    def distance_defenseur_ball(self):
        """Distance entre le joueur et la balle	"""
        return self.position_ball.distance(self.position_defenseur)

    @property
    def distance_gardien_ball(self):
        """Distance entre le joueur et la balle	"""
        return self.position_ball.distance(self.position_gardien)

    @property
    def rayon_player_ball(self):
        """Rayon du joueur plus rayon nde la balle"""
        return PLAYER_RADIUS + BALL_RADIUS

    @property
    def fonce_ball(self):
        """Fonce vers la balle"""
        #if self.id_team == 2:
        #    print self.id_team,self.id_player,self.position_ball,self.position_player,SoccerAction(self.position_ball-self.position_player)
        return SoccerAction(self.position_ball - self.position_player)

    @property
    def drible(self):
        """Drible le joueur en face to face"""
        if self.distance_player_ball < self.rayon_player_ball:
            if self.distance_lalya1 < 30 and self.position_player.x < self.position_player_adv.x:
                if self.position_ball.y > MEDIUM_HEIGHT:
                    return SoccerAction(Vector2D(), (Vector2D(x = self.position_player_adv.x + 5, y = self.position_player_adv.y + 20) - self.position_ball).norm_max(1))
                else:
                    return SoccerAction(Vector2D(), (Vector2D(x = self.position_player_adv.x + 5, y = self.position_player_adv.y - 20) - self.position_ball).norm_max(1))
            return SoccerAction((self.position_ball - self.position_player), (self.goal_deux - self.position_ball).norm_max(1))
        return self.shoot_ball
    
    @property
    def shoot_ball(self):
        """Shoot la balle"""
        if self.distance_player_ball < self.rayon_player_ball:
            if self.position_ball.x >= THREE_QUARTER_WIDTH:
                return SoccerAction(Vector2D(), (self.goal_deux - self.position_ball).norm_max(4))
            else:
                return SoccerAction(Vector2D(), (self.goal_deux - self.position_ball))
        return self.fonce_ball

    
    @property
    def passe_ball_pproche(self):
        """Passe la balle au joueur le plus proche"""
        if self.distance_player_ball < self.rayon_player_ball:
            return SoccerAction(Vector2D(), (self.position_player_adv - self.position_ball).norm_max(5))
        return self.fonce_ball

    @property
    def run_ball_avant_normalize(self):
        """Cours avec la ball vers le goal deux"""
        if self.distance_player_ball < self.rayon_player_ball:
            return SoccerAction(Vector2D(), (self.goal_deux - self.position_ball).normalize().scale(2))
        return self.fonce_ball

    @property
    def run_ball_arriere_normalize(self):
        """Cours avec la ball vers le goal un (son propre goal)"""
        if self.distance_player_ball < self.rayon_player_ball:
            return SoccerAction(Vector2D(), (self.goal_un - self.position_ball).normalize().scale(2))
        return self.fonce_ball

                                ############################
    @property
    def run_ball_angle_0(self):
        """Run with angle = 0"""
        return SoccerAction(Vector2D(), (self.angle_0 - self.position_ball).normalize().scale(2))

    @property
    def run_ball_angle_pi6(self):
        """Run with angle = pi/6"""
        return SoccerAction(self.position_ball - self.position_player, (self.angle_pi6 - self.position_ball).normalize().scale(2))

    @property
    def run_ball_angle_pi(self):
        """Run with a pi angle"""
        return SoccerAction(Vector2D(), (self.angle_pi - self.position_ball).normalize().scale(2))

    @property
    def pass_ball_plus_proche(self):
        """Passe la ball au joueur le plus proche"""
        return SoccerAction(Vector2D(), (self.position_j_plus_proche - self.position_ball))
                               #############################
                               
    @property
    def shoot_ball_coin_bas(self):
        """Shoot la balle au coin bas, c'est à dire au premier poto du goal_deux"""
        return SoccerAction(Vector2D(), (self.goal_deux_coin_bas - self.position_ball).norm_max(4))
    
    @property
    def shoot_ball_coin_haut(self):
        """Shoot la balle au coin haut, c'est à dire au deuxième poto du goal_deux"""
        return SoccerAction(Vector2D(), (self.goal_deux_coin_haut - self.position_ball).norm_max(4))
    
    @property
    def shoot_ball_smart(self):
        """Choisi quand shooter au premier ou au deuxième poto ou sur l'un des deux côtés s'il se trouve au beau milieu """
        if self.distance_player_ball < self.rayon_player_ball:
            if (self.position_ball.y <= GAME_HEIGHT - 46) and (self.position_ball.x >= MEDIUM_WIDTH - 5):
                return self.shoot_ball_coin_bas
            elif (self.position_ball.y >= GAME_HEIGHT - 44) and (self.position_ball.x >= MEDIUM_WIDTH - 5):
                return self.shoot_ball_coin_haut
            L = [self.shoot_ball_coin_bas, self.shoot_ball_coin_haut]
            return choice(L)
        return self.fonce_ball
    
    @property
    def passe_g(self):
        """Shoot la balle vers la gauche avec un angle de 45 dégré"""
        if self.distance_player_ball < self.rayon_player_ball:
            return SoccerAction(Vector2D(), (Vector2D(x = THREE_QUARTER_WIDTH, y = THREE_QUARTER_HEIGHT) - self.position_ball))
        return self.fonce_ball
    
    @property
    def passe_g_normalize(self):
        """Shoot la balle vers la gauche avec un angle de 45 dégré"""
        if self.distance_player_ball < self.rayon_player_ball:
            return SoccerAction(Vector2D(), (Vector2D(x = THREE_QUARTER_WIDTH - 5, y = THREE_QUARTER_HEIGHT - 5) - self.position_ball).normalize().scale(3))
        return self.fonce_ball

    @property 
    def passe_d(self):
        """Shoot la balle vers la droite avec un angle de 45 dégré"""
        if self.distance_player_ball < self.rayon_player_ball:
            return SoccerAction(Vector2D(), (Vector2D(x = THREE_QUARTER_WIDTH, y = QUARTER_HEIGHT) - self.position_ball))
        return self.fonce_ball

    @property 
    def passe_d_normalize(self):
        """Shoot la balle vers la droite avec un angle de 45 dégré"""
        if self.distance_player_ball < self.rayon_player_ball:
            return SoccerAction(Vector2D(), (Vector2D(x = THREE_QUARTER_WIDTH - 5, y = QUARTER_HEIGHT + 5) - self.position_ball).normalize().scale(3))
        return self.fonce_ball

    @property
    def defense_shoot_g(self):
        """Shoot la balle vers la gauche avec un x qui est le centre du terrain"""
        if self.distance_player_ball < self.rayon_player_ball:
            return SoccerAction(Vector2D(), Vector2D(x = MEDIUM_WIDTH + 30, y = GAME_HEIGHT - 20) - self.position_ball)
        return self.fonce_ball

    @property
    def defense_shoot_d(self):
        if self.distance_player_ball < self.rayon_player_ball:
            return SoccerAction(Vector2D(), Vector2D(x = MEDIUM_WIDTH + 30, y = 20) - self.position_ball)
        return self.fonce_ball

    @property
    def keeper_shoot_g(self):
        """Shoot vers la gauche du milieu du terrain"""
        if self.distance_player_ball < self.rayon_player_ball:
            return SoccerAction(Vector2D(), (Vector2D(x = MEDIUM_WIDTH, y = GAME_HEIGHT - 10) - self.position_ball).norm_max(6))
        return self.fonce_ball

    @property
    def keeper_shoot_d(self):
        """Shoot vers la droite du milieu du terrain"""
        if self.distance_player_ball < self.rayon_player_ball:
            return SoccerAction(Vector2D(), (Vector2D(x = MEDIUM_WIDTH, y = 10) - self.position_ball).norm_max(6))
        return self.fonce_ball    


######################################################################################################
#                                            TEAM ONE
######################################################################################################

    @property
    def player_team1(self):
        """Joueur de la team1"""
        if (self.position_ball.x == MEDIUM_WIDTH) and (self.position_ball.y == MEDIUM_HEIGHT):
            if self.distance_player_ball < self.rayon_player_ball:
                return SoccerAction(Vector2D(), (Vector2D(x = THREE_QUARTER_WIDTH, y = MEDIUM_HEIGHT + 4)).norm_max(4))
            return self.fonce_ball
        elif (self.position_ball.x > MEDIUM_WIDTH) and (self.position_ball.x < THREE_QUARTER_WIDTH):
            if self.distance_player_ball < self.rayon_player_ball:
                return SoccerAction(Vector2D(), (self.goal_deux - self.position_ball).norm_max(4))
            return self.fonce_ball
        elif (self.position_ball.x < MEDIUM_WIDTH) and (self.position_ball.x > QUARTER_WIDTH):
            if (self.position_ball.y > MEDIUM_HEIGHT):
                return self.passe_g
            elif (self.position_ball.y < MEDIUM_HEIGHT):
                return self.passe_d
            return self.shoot_ball_smart
        elif (self.position_ball.x < QUARTER_WIDTH):
            if (self.position_ball.y > MEDIUM_HEIGHT):
                return self.defense_shoot_d
            elif (self.position_ball.y < MEDIUM_HEIGHT):
                return self.defense_shoot_g
            return self.shoot_ball
        return SoccerAction((self.position_ball - self.position_player), (self.goal_deux - self.position_ball).norm_max(3))


######################################################################################################
#                                             TEAM TWO
######################################################################################################

    @property
    def player_team2(self):
        """Attaquant de la team2"""
        if (self.position_ball.x == MEDIUM_WIDTH) and (self.position_ball.y == MEDIUM_HEIGHT):
            if self.distance_player_ball < self.rayon_player_ball:
                return SoccerAction(Vector2D(), (Vector2D(x = THREE_QUARTER_WIDTH, y = MEDIUM_HEIGHT + 4)))
            return self.fonce_ball
        elif (self.position_ball.x > MEDIUM_WIDTH) and (self.position_ball.x < THREE_QUARTER_WIDTH):
            if self.distance_player_ball < self.rayon_player_ball:
                return SoccerAction(Vector2D(), (Vector2D(x = GAME_WIDTH, y = MEDIUM_HEIGHT) - self.position_ball).normalize().scale(2))
            return self.fonce_ball
        elif (self.position_ball.x < MEDIUM_WIDTH) and (self.position_ball.x > QUARTER_WIDTH):
            if (self.position_ball.y > MEDIUM_HEIGHT):
                return self.passe_g_normalize
            elif (self.position_ball.y < MEDIUM_HEIGHT):
                return self.passe_d_normalize
            return self.shoot_ball
        elif (self.distance_gardien_ball < QUARTER_WIDTH - 16 ):
            if (self.position_ball.y >= MEDIUM_HEIGHT + 1):
                return SoccerAction(Vector2D(x = MEDIUM_WIDTH - 8, y = 13) - self.position_player)
            elif (self.position_ball.y < MEDIUM_HEIGHT):
                return SoccerAction(Vector2D(x = MEDIUM_WIDTH - 8, y = GAME_HEIGHT - 13) - self.position_player)
            return self.shoot_ball
        return self.shoot_ball_smart


    @property
    def goalkeeper(self):
        """Gardien de la team2"""
        if (self.distance_player_ball <= QUARTER_WIDTH) and (self.position_ball.y < THREE_QUARTER_HEIGHT + 5) and (self.position_ball.y > QUARTER_HEIGHT - 5): 
            if (self.position_ball.y >= 46):
                return self.keeper_shoot_d
            elif (self.position_ball.y < 46):
                return self.keeper_shoot_g
        elif (self.distance_gardien_ball < self.distance_player_ball) and (self.position_ball.x < QUARTER_WIDTH):
            return self.shoot_ball
        elif (self.position_ball.x > MEDIUM_WIDTH) and (self.position_ball.y < THREE_QUARTER_HEIGHT and self.position_ball.y > QUARTER_HEIGHT):
            return SoccerAction(Vector2D(x = QUARTER_WIDTH - 10, y = self.position_ball.y) - self.position_player)
        elif (self.position_ball.x > MEDIUM_WIDTH - 10) and (self.position_ball.y > THREE_QUARTER_HEIGHT or self.position_ball.y < QUARTER_HEIGHT):
            return SoccerAction(Vector2D(x = QUARTER_WIDTH - 10, y = MEDIUM_HEIGHT) - self.position_player)
        elif (self.position_ball.x <= MEDIUM_WIDTH - 10) and (self.position_ball.x >= QUARTER_WIDTH + 10):
            return SoccerAction(Vector2D(x = QUARTER_WIDTH - 25, y = MEDIUM_HEIGHT) - self.position_player)
        else:
            return SoccerAction(Vector2D(x = 1, y = MEDIUM_HEIGHT) - self.position_player)

######################################################################################################
#                                             TEAM FOUR
######################################################################################################
    
    @property
    def goalkeeper_team4(self):
        """Gardien de la team4"""
        if (self.distance_player_ball <= QUARTER_WIDTH) and (self.position_ball.y < THREE_QUARTER_HEIGHT + 5) and (self.position_ball.y > QUARTER_HEIGHT - 5) and (self.position_ball.x < QUARTER_WIDTH + 5):
            if (self.position_ball.y >= 46):
                return self.keeper_shoot_d
            else:
                return self.keeper_shoot_g
        elif (self.distance_gardien_ball < self.distance_defenseur_ball) and (self.position_ball.x < QUARTER_WIDTH):
            return self.shoot_ball
        elif (self.position_ball.y <= GAME_HEIGHT - 49) and (self.position_ball.x > GAME_WIDTH/8.) and (self.position_ball.x < THIRD_WIDTH):
            return SoccerAction((self.goal_un - Vector2D(x = 0, y = 3)) - self.position_player) 
        elif (self.position_ball.y >= GAME_HEIGHT - 41) and (self.position_ball.x > GAME_WIDTH/8.) and (self.position_ball.x < THIRD_WIDTH):
            return SoccerAction((self.goal_un + Vector2D(x = 0, y = 3)) - self.position_player)
        elif (self.position_ball.x >= THIRD_WIDTH):
            return SoccerAction(Vector2D(x = GAME_WIDTH/11., y = MEDIUM_HEIGHT) - self.position_player)
        else:
            return SoccerAction(Vector2D(x = 1, y = MEDIUM_HEIGHT) - self.position_player)
    
    @property
    def defense(self):
        """Defenseur de la team4"""
        if (self.position_ball.x <= MEDIUM_WIDTH + 10) and (self.position_ball.x > QUARTER_WIDTH):
            if (self.position_ball.y > MEDIUM_HEIGHT):
                return self.passe_g
            elif (self.position_ball.y < MEDIUM_HEIGHT):
                return self.passe_d
            return self.shoot_ball_smart
        elif (self.position_ball.x <= QUARTER_WIDTH):
            if (self.position_ball.y > MEDIUM_HEIGHT):
                return self.defense_shoot_d
            elif (self.position_ball.y < MEDIUM_HEIGHT):
                return self.defense_shoot_g
            return self.shoot_ball_smart
        elif (self.position_ball.x - self.position_player.x >= 50) and (self.position_ball.x >= MEDIUM_WIDTH + 10):
            return SoccerAction(Vector2D(x = self.position_ball.x - 50, y = self.position_ball.y) - self.position_player)
        else:
            return SoccerAction(Vector2D(x = GAME_WIDTH/6., y = MEDIUM_HEIGHT) - self.position_player)

    @property
    def player_team41(self):
        """Attaquant elié gauche;) je pense"""
        if (self.position_ball.y > MEDIUM_HEIGHT):
            if (self.position_ball.x <= MEDIUM_WIDTH + 5):
                if (self.distance_defenseur_ball <= QUARTER_WIDTH - 25):
                    if (self.distance_player_ball < self.rayon_player_ball):
                        return self.passe_g_normalize
                    else:
                        return SoccerAction(Vector2D(x = THREE_QUARTER_WIDTH - 10, y = THREE_QUARTER_HEIGHT) - self.position_player)
                else:
                    if (self.distance_player_ball < self.rayon_player_ball):
                        return self.passe_g_normalize
                    return self.fonce_ball
            else:
                if (self.position_ball.x > THREE_QUARTER_WIDTH):
                    return self.shoot_ball_smart
                else:
                    return self.run_ball_avant_normalize
        return SoccerAction(Vector2D(x = self.position_ball.x, y = MEDIUM_HEIGHT + 10) - self.position_player)
        
        

    @property
    def player_team42(self):
        """Attaquant elié droit ;) encore je pense"""
        if (self.position_ball.y < MEDIUM_HEIGHT):
            if (self.position_ball.x <= MEDIUM_WIDTH + 10):
                if (self.distance_defenseur_ball <= QUARTER_WIDTH - 25):
                    if (self.distance_player_ball < self.rayon_player_ball):
                        return self.passe_d_normalize
                    else:
                        return SoccerAction(Vector2D(x = THREE_QUARTER_WIDTH - 10, y = QUARTER_HEIGHT) - self.position_player)
                else:
                    if (self.distance_player_ball < self.rayon_player_ball):
                        return self.passe_d_normalize
                    return self.fonce_ball
            else:
                if (self.position_ball.x > THREE_QUARTER_WIDTH):
                    return self.shoot_ball_smart
                else:
                    return self.run_ball_avant_normalize
        return SoccerAction(Vector2D(x = self.position_ball.x, y = MEDIUM_HEIGHT - 10) - self.position_player)

######################################################################################################
#                         Fin de mes petites strategies
######################################################################################################

def essai(mystate):
    return mystate.passe_ball_pproche

def rien(mystate):
    return mystate.do_nothing

def fonceur(mystate):
    return mystate.fonce_ball

def dribleur(mystate):
    return mystate.drible

def player_team1(mystate):
    return mystate.player_team1

def player_team2(mystate):
    return mystate.player_team2

def player_team41(mystate):
    return mystate.player_team41

def player_team42(mystate):
    return mystate.player_team42

def gardien(mystate):
    return mystate.goalkeeper

def gardien_team4(mystate):
    return mystate.goalkeeper_team4

def defenseur(mystate):
    return mystate.defense

######################################################################################################
#                          Strategies simples à utiliser avec KeyboardStrategy
######################################################################################################
def fonceur_shooteur(mystate):
    return mystate.shoot_ball

def shooteur_ball_smart(mystate):
    return mystate.shoot_ball_smart

def run_ball_avant_normalize(mystate):
    return mystate.run_ball_avant_normalize

def run_ball_arriere_normalize(mystate):
    return mystate.run_ball_arriere_normalize

######################################################################################################
#          Miroir: ps un gros problème
######################################################################################################

def miroir_p(p):
    return Vector2D(GAME_WIDTH - p.x, p.y)

def miroir_v(v):
    return Vector2D(-v.x, v.y)

def miroir_socac(action):
    return SoccerAction(miroir_v(action.acceleration), miroir_v(action.shoot))

def miroir_state(s):
    res = s.copy()
    res.ball.position = miroir_p(s.ball.position)
    res.ball.vitesse  = miroir_v(s.ball.vitesse)
    for (id_team, id_player) in s.players:
        res.player_state(id_team, id_player).position = miroir_p(s.player_state(id_team, id_player).position)
        res.player_state(id_team, id_player).vitesse = miroir_v(s.player_state(id_team, id_player).vitesse)
    return res

######################################################################################################
#          Fin de ce beau miroir
######################################################################################################
