# -*- coding: utf-8 -*-
from soccer_base import *
import strategies
import mdpsoccer

###############################################################################
# SoccerPlayer
###############################################################################

class SoccerBall(object):
    def __init__(self,position=Vector2D(),speed=Vector2D()):
        self.position=position
        self.speed=speed
    @property
    def angle(self):
        return self.speed.angle
    def copy(self):
        return SoccerBall(self.position.copy(),self.speed.copy())
    def __str__(self):
        return "Ball : %s %s"% (self.position,self.speed)


###############################################################################
# SoccerPlayer
###############################################################################


class SoccerPlayer(object):        
    def __init__(self,name,strat=None):
        self._name=name
        self.position=Vector2D()
        self.angle=0.
        self.speed=0.
        self._num_before_shoot=0
        self._strategy=None
        if strat:
            if not isinstance(strat,strategies.SoccerStrategy):
                raise PlayerException("La stratégie n'herite pas de la classe SoccerStrategy")
            self._strategy=strat.copy()        
    @property      
    def name(self):
        return self._name
    def set_position(self,x,y,angle):
        self.position=Vector2D(x,y)
        self.angle=float(angle)
    def dec_num_before_shoot(self):
        if self._num_before_shoot>0:        
            self._num_before_shoot-=1
    def init_num_before_shoot(self):
        self._num_before_shoot=nbWithoutShoot
    def get_num_before_shoot(self):
        return self._num_before_shoot
    def __str__(self):
        return "%s : (%s, %f, %f)" % (self._name,self.position,self.speed,self.angle)
    @property
    def normed_position(self):
        return Vector2D(self.position.x/SoccerState.GAME_WIDTH, self_position.y/SoccerState.GAME_HEIGHT)
    def copy(self):
        res=SoccerPlayer(self._name,self._strategy)
        res.position=self.position.copy()
        res.angle=self.angle
        res.speed=self.speed
        res._num_before_shoot=self._num_before_shoot
        return res
    def can_shoot(self):
        return self.get_num_before_shoot()<1
    @property
    def strategy(self):
        return self._strategy
    @strategy.setter
    def strategy(self,strat):
        self._strategy=strat.copy()
    def compute_strategy(self,state,teamid):
        if self._strategy:
            return self.strategy.compute_strategy(state,self,teamid)
        raise PlayerException('Pas de strategie définie pour le joueur %s' %self.get_name())
        
###############################################################################
# SoccerTeam
###############################################################################
        
class SoccerTeam:
    def __init__(self,name,soccer_club=None):
        self._name=name
        self._exceptions=[]
        self._players=dict()
        
    def copy(self):
        team=SoccerTeam(self._name)
        team._exceptions=list(team._exceptions)
        for name,p in self._players.items():
            team.add_player(p.copy())
        return team
    def add_name(self,name):
        self._name+="."+name
    def add_player(self,player):
        if player.name in self.players:
            raise IncorrectTeamException('Nom de joueur dupliqué : '%player.name)
        self._players[player.name]=player
    @property
    def name(self):
        return self._name
    @property
    def num_players(self):
        return len(self._players)
    @property
    def num_exceptions(self):
        return len(self._exceptions)
    def get_player(self,player):
        name=player
        if isinstance(player,SoccerPlayer):
            name=player.name
        if name not in self._players.keys():
            return None
        return self._players[player]
    @property        
    def players(self):
        return self._players.values()
    @property
    def dic_players(self):
        return self._players
    def compute_strategies(self,state,teamid):
        res=dict()
        for p in self.players:
            action=p.compute_strategy(state,teamid)
            if not isinstance(action,mdpsoccer.SoccerAction):
                raise StrategyException("Le resultat n'est pas une action : player %s, strategie %s " % (p.name,p.get_strategy().name))
            res[p.name]=action
        return res
    def start_battle(self,state):
        for p in self.players:
            p.strategy.start_battle(state)
    def finish_battle(self,won):
        for p in self.players:
            p.strategy.finish_battle(won)
    def __getitem__(self,index):
        if isinstance(index,int):
            return self.players[index]
        return self._players[index]
    def __str__(self):
        return " Team "+self.name+": " +" | ".join(map(str,self.players)) 

