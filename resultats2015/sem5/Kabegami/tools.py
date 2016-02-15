import soccersimulator,soccersimulator.settings
from soccersimulator import BaseStrategy, SoccerAction
from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Vector2D, Player, SoccerTournament
from soccersimulator import settings
from zone import *
from PlayerDecorator import *

def fonceur(etat):
    return etat.shoot_but + etat.go_ball

def goal(etat):
    if (etat.distance_ball) < 20:
        return etat.go_ball + etat.degage(etat.my_zone)
    else:
        return etat.go(etat.my_but) + etat.shoot_but

def milieu(etat):
    if not(etat.adv_dans_zone(m)):
        return fonceur(etat)
    if (etat.j_dans_zone(m)):
        if(etat.key[0] == 1):   
            return etat.go_ball + etat.degage(m.division_verticale[1])
        else:
            return etat.go_ball + etat.degage(m.division_verticale[0])
    else:
        if(etat.dans_zone(etat.adv_zone,etat.my_position)):
            return fonceur(etat)
        else:
            if (etat.key[0] == 1):
                if etat.adv_dans_zone(etat.my_zone.division_verticale[0]):
                    return goal(etat)
                else:
                    return fonceur(etat)
            else:
                if etat.adv_dans_zone(etat.my_zone.division_verticale[1]):
                    return goal(etat)
                else:
                    return fonceur(etat)
            
