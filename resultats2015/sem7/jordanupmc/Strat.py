import soccersimulator, soccersimulator.settings, cPickle

from soccersimulator import BaseStrategy, Vector2D, SoccerAction, settings

from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Player, SoccerTournament,KeyboardStrategy
from tools import *


class RandomStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "Random")

    def compute_strategy(self, state,id_team, id_player):
        return SoccerAction(Vector2D.create_random(-1,1),Vector2D.create_random(-1,1))

 
class FonceurStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "Fonceur")

    def compute_strategy(self, state,id_team, id_player):
        a=App(state,id_team,id_player)
        if a.key[0]==2:
            a=App(miroir(state),id_team,id_player)
            return miroir_action(fonceur(a))
        return fonceur(a)
 
 
class GardienStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "Gardien")

    def compute_strategy(self, state,id_team, id_player):
        a=App(state,id_team,id_player)
            
        if a.key[0]==2:
            a=App(miroir(state),id_team,id_player)

        
        if a.near_ball(20) == 1 or a.is_out_goal()==0:
            if a.key[0] ==2:
               return miroir_action(gardien(a))
            return gardien(a)
        
        if a.key[0] ==2:
           return miroir_action(go_vers_ball(a))+miroir_action(degager(a))
        
        return go_vers_ball(a)+degage_cote(a)


class DTreeStrategy(BaseStrategy):
    def __init__(self,tree,dic,gen_feat):
        BaseStrategy.__init__(self,"Tree Strategy")
        self.dic = dic
        self.tree = tree
        self.gen_feat= gen_feat
    def compute_strategy(self, state, id_team, id_player):
        label = self.tree.predict(self.gen_feat(state,id_team,id_player))[0]
        if label not in self.dic:
            print("Erreur : strategie %s non trouve" %(label,))
            return SoccerAction()
        return self.dic[label].compute_strategy(state,id_team,id_player)


#################

def go_vers_ball(app):
    return app.vers_ball()

def degager(app):
    if app.can_shoot() == 0:
        return SoccerAction(Vector2D(),Vector2D(5,0)) 
    return SoccerAction(Vector2D(),Vector2D())

def conduite_ball(app):
    if app.can_shoot() == 0:
        return app.conduire_ball()
    return SoccerAction(Vector2D(),Vector2D())


def fonceur(a):
    if a.is_ball_near_goal(3.8) == 0:#3.8
        return go_vers_ball(a)+degager(a)
    return go_vers_ball(a)+conduite_ball(a)


def gardien(a):
    if a.is_out_goal() == 0:  #Si il etait dans les cages et qu'il en est sortit
        return a.go_goal()+degage_cote(a)
    if a.is_ball_in_my_camp() == 0: #balle dans ma moitie de terain
        return degage_cote(a)
    if a.is_in_goal() == 0: #initialisation 
        return a.go_goal()
    return SoccerAction()
    

def degage_cote(a):
    dep=a.ball_position-a.my_position            #--> bloquer le passage de la balle 
    dep.x=0
    if a.can_shoot() == 0:  # Shoot ou pas
        
        if a.ball_position.y >= settings.GAME_HEIGHT/2: 
            return SoccerAction(dep,Vector2D((3.14),5)) # angle a modifie
        else:
            return SoccerAction(dep,Vector2D(-(3.14),5))
    return SoccerAction(dep,Vector2D())

###Tree#########

def gen_feat(state, player, idteam):
    a=App(state,id_team,player)
    
    bpos = state.ball.position
    mpos = state.player_state(id_team,id_player).position
    myg = Vector2D((id_team-1)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)
    hisg = Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)

    return [bpos.distance(mpos),bpos.distance(myg),bpos.distance(hisg)]


def build_apprentissage(fn,generator):
    ex_raw = KeyboardStrategy.read(fn)
    exemples = []
    labels = []
    for x in ex_raw:
        exemples.append(generator(x[1],x[0][0],x[0][1]))
        labels.append(x[0][2])
    return exemples,labels

def apprendre_arbre(train,labels,depth=5):
    tree= DecisionTreeClassifier()
    tree.fit(train,labels)
    return tree

    

  #MIROR#########################

def miroir_point(p):
    return Vector2D(settings.GAME_WIDTH-p.x,p.y)
    
def miroir_v(v):
    return Vector2D(-v.x,v.y)

def miroir_action(action):
    action.acceleration=miroir_v(action.acceleration)
    action.shoot=miroir_v(action.shoot)
    return action

def miroir(state):
    state.ball.position=miroir_point(state.ball.position)
    state.ball.vitesse=miroir_v(state.ball.vitesse)
    for(idteam,idplayer) in state.players:
        state.player_state(idteam,idplayer).position=miroir_point(state.player_state(idteam,idplayer).position)
        state.player_state(idteam,idplayer).vitesse=miroir_v(state.player_state(idteam,idplayer).vitesse)        
    return state


    ###########################################
