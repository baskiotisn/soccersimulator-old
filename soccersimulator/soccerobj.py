# -*- coding: utf-8 -*-
from soccer_base import *
import strategies
import mdpsoccer
from operator import itemgetter
from copy import deepcopy

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
            self._strategy=deepcopy(strat)
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
        return self._name
    @property
    def normed_position(self):
        return Vector2D(self.position.x/SoccerState.GAME_WIDTH, self.position.y/SoccerState.GAME_HEIGHT)
    def can_shoot(self):
        return self.get_num_before_shoot()<1
    @property
    def strategy(self):
        return self._strategy
    @strategy.setter
    def strategy(self,strat):
        self._strategy=strat
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
        self._club=None

    @property
    def club(self):
        return self._club
    @club.setter
    def club(self,club):
        self._club = club
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
        return self.name+"("+ str(self.club)+")"


class SoccerClub:
    def __init__(self,login=None):
        self.name=login
        self.teams=dict()
        self.login=login
        self._exceptions=[]

    def get_num_teams(self):
        return sum([ len(team) for team in self.teams.values()])

    def get_all_teams(self):
        return [x for i in self.teams.keys() for x in self.get_teams(i) ]
    def get_teams(self,i):
        if i in self.teams:
            return self.teams[i].values()
        return []
    def add_team(self,team):
        nbp = team.num_players
        if nbp not in self.teams:
            self.teams[nbp]=dict()
        if team.name not in self.teams[nbp]:
            self.teams[nbp][team.name]=team
            team.club=self

    def add_teams(self,teams):
        for team in teams:
            self.add_team(team)

    def __str__(self):
        return self.name



class SoccerTournament:
    def __init__(self,name,list_games=[1,2,4],same_club=False):
        self.clubs=[]
        self.name=name
        self.list_games=list_games
        self.battles=dict()
        self.battles_by_club=dict()
        self.teams_score=dict()
        self.same_club=same_club
    def add_club(self,club):
        self.clubs.append(club)

    def init_battles(self):
        self.battles=dict()
        self.battles_by_club=dict()
        self.teams_score=dict()
        for nbp in self.list_games:
            self.battles[nbp]=list()
            self.battles_by_club[nbp]=dict()
            self.teams_score[nbp]=dict()
            for club in self.clubs:
                self.battles_by_club[nbp][club.login]=list()
                self.teams_score[nbp][club]=dict()
        for club1 in range(len(self.clubs)):
            for club2 in range(club1+1 if not self.same_club else club1,len(self.clubs)):
                for nbp in self.list_games:
                    for team1 in self.clubs[club1].get_teams(nbp):
                        for team2 in self.clubs[club2].get_teams(nbp):
                            b = mdpsoccer.SoccerBattle(team1,team2)
                            self.battles[nbp].append(b)
                            self.battles_by_club[nbp][self.clubs[club1].login].append(b)
                            self.battles_by_club[nbp][self.clubs[club2].login].append(b)
                            self.teams_score[nbp][self.clubs[club1]][team1]=0
                            self.teams_score[nbp][self.clubs[club2]][team2]=0
    def do_battles(self):
        for nbp in self.list_games:
            print "Tournoi %d joueurs" % (nbp,)
            for i,b in enumerate(self.battles[nbp]):
                b.run_multiple_battles(5,5000)
                print "Game ended %d/%d: %s" % (i,len(self.battles[nbp]),b)
                if b.score_team1 > b.score_team2:
                    self.teams_score[nbp][b.team1.club][b.team1]+=3
                if b.score_team2 > b.score_team1:
                    self.teams_score[nbp][b.team2.club][b.team2]+=3
                if b.score_team2 == b.score_team1:
                    self.teams_score[nbp][b.team1.club][b.team1]+=1
                    self.teams_score[nbp][b.team2.club][b.team2]+=1


    def get_best_team_by_club(self):
        res=dict()
        for nbp in self.list_games:
            res[nbp]=dict()
            for c in self.clubs:
                res[nbp][c]=sorted(self.teams_score[nbp][c].items(),key=itemgetter(1),reverse=True)[0]
        return res
