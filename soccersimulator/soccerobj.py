# -*- coding: utf-8 -*-
from soccer_base import *
import mdpsoccer
from functools import total_ordering
from copy import deepcopy
import strategies
import string
import traceback
import interfaces
valid_chars=frozenset("%s%s%s" % (string.ascii_letters, string.digits,"_-.()[]"))
def clean_fn(fn):
    return ''.join(c if c in valid_chars else '' for c in fn)

###############################################################################
# SoccerPlayer
###############################################################################

class SoccerBall(object):
    def __init__(self,position=Vector2D(),speed=Vector2D()):
        self.position=position
        self.speed=speed
    def copy(self):
        return SoccerBall(self.position.copy(),self.speed.copy())
    @property
    def angle(self):
        return self.speed.angle
    def __str__(self):
        return "Ball : %s %s"% (self.position,self.speed)
    def __eq__(self,other):
        return (self.position == other.position)  and (self.speed == other.speed)

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
        self.id =-1
        if strat:
            self._strategy=deepcopy(strat)
        #self._strategy=strat
    def __eq__(self,other):
        return self.id == other.id and (self.position == other.position) and (self.angle == other.angle) and (self.speed == other.speed)\
                and (self._num_before_shoot == other._num_before_shoot)
    def copy_safe(self):
        #player=deepcopy(self)
        player=SoccerPlayer(self.name,self._strategy)
        player.position=self.position
        player.angle=self.angle
        player.speed=self.speed
        player._num_before_shoot=self._num_before_shoot
        player.id=self.id
        player._strategy=strategies.SoccerStrategy(self.strategy.name)
        return player
    def copy(self):
        player=self.copy_safe()
        player._strategy=deepcopy(self._strategy)
        return player
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
        try:
            return self.strategy.compute_strategy(state,self,teamid)
        except Exception as e:
        #    print "*********\n erreur pour joueur %s : %s \n *********" % (self,e,)
        #    traceback.print_exc()
            raise e


###############################################################################
# SoccerTeam
###############################################################################

class SoccerTeam:
    def __init__(self,name,soccer_club=None):
        self._name=name
        self._exceptions=[]
        self._players=[]
        self._club=None

    def __eq__(self,other):
        other_players = list(other.players)
        for p in self._players:
            try:
                other_players.remove(p)
            except ValueError:
                return False
        return True
    def copy_safe(self):
        team = SoccerTeam(self.name)
        for p in self:
            team.add_player(p.copy_safe())
        return team
    def copy(self):
        team = SoccerTeam(self.name)
        for p in self:
            team.add_player(p.copy())
        team._exceptions=list(self._exceptions)
        team._club=self._club
        return team
    @property
    def club(self):
        return self._club
    @club.setter
    def club(self,club):
        self._club = club
    def add_name(self,name):
        self._name+="."+name
    def add_player(self,player):
        if player.name in [p.name for p in self.players]:
            self.add_exception('Nom de joueur dupliqué : %s ' %(player.name,) )
            raise Exception('Nom de joueur dupliqué : %s ' % (player.name,))
        player.id=len(self._players)
        self._players.append(player)
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
        if isinstance(player,int):
            return self._players[player]
        name=player
        if isinstance(player,SoccerPlayer):
            name=player.name
        for p in self._players:
            if p.name==name:
                return p
        return None
    def add_exception(self,e):
        self._exceptions.append(e)
    @property
    def exceptions(self):
        return self._exceptions
    @property
    def players(self):
        return self._players
    def compute_strategies(self,state,teamid):
        res=[]
        for p in self.players:
            action=mdpsoccer.SoccerAction()
            try:
                action=p.compute_strategy(state,teamid)
                if not isinstance(action,mdpsoccer.SoccerAction):
                    raise Exception("Le resultat n'est pas une action : player %s, strategie %s " % (p.name,p.strategy.name))
            except Exception as e:
                self.add_exception([e,traceback.format_exc()])
            res.append(action)
        return res

    def begin_battles(self,state,battles_count,max_step):
        for p in self.players:
            p.strategy.begin_battles(state,battles_count,max_step)
    def start_battle(self,state):
        self._exceptions=[]
        for p in self.players:
            p.strategy.start_battle(state)
    def finish_battle(self,won):
        for p in self.players:
            p.strategy.finish_battle(won)
    def end_battles(self):
        for p in self.players:
            p.strategy.end_battles()

    def __getitem__(self,index):
        if isinstance(index,int):
            return self.players[index]
        return self.get_player(index)
    def __str__(self):
        return self.name+"("+ str(self.club)+")"
    def __iter__(self):
        return self._players.__iter__()

class SoccerClub:
    def __init__(self,login=None):
        self.name=login
        self.teams=dict()
        self.login=login
        self._exceptions=[]
    def get_num_teams(self,nbp=None):
        if not nbp:
            return sum([ len(team) for team in self.teams.values()])
        return len(self.teams[nbp])
    def add_team(self,team):
        nbp = team.num_players
        if nbp not in self.teams:
            self.teams[nbp]=[]
        if team.name not in [t.name for t in self.teams[nbp]]:
            self.teams[nbp].append(team)
            team.club=self

    def add_teams(self,teams):
        for team in teams:
            self.add_team(team)

    def __str__(self):
        return self.name

@total_ordering
class Score:
    def __init__(self,team=None):
        self.win=0
        self.loose=0
        self.draw=0
        self.gf=0
        self.ga=0
        self._list_battles=[]
        if team:
            self._team=team.name
            self._login=team.club.login
            self._club=team.club.name
        else:
            self._team=""
            self._login=""
            self._club=""
    def add_score(self,gf,ga,team=None):
        if team:
            self._list_battles.append(((team.club.login,team.club.name,team.name),gf,ga))
        self.gf+=gf
        self.ga+=ga
        if gf>ga:
            self.win+=1
        if gf<ga:
            self.loose+=1
        if gf==ga:
            self.draw+=1
    @property
    def battles(self):
        return list(self._list_battles)
    @property
    def team(self):
        return self._team
    @property
    def club(self):
        return self._club
    @property
    def login(self):
        return self._login
    @property
    def score(self):
        return 3*self.win+self.draw
    @property
    def nb_battles(self):
        return self.win+self.loose+self.draw
    def __lt__(self,other):
        return (self.score,self.gf,-self.ga) < (other.score,other.gf,-other.ga)
    def __eq__(self,other):
        return (self.score,self.gf,self.ga) == (other.score,other.gf,other.ga)
    def reset(self):
        self.win=0
        self.loose=0
        self.draw=0
        self.gf=0
        self.ga=0
        self._list_battles=[]
    def __str__(self):
        return "%d (%d,%d,%d) - (%d,%d)" % (self.score,self.win,self.loose,self.draw,self.gf,self.ga)

class SoccerTournament:
    def __init__(self,name,list_games=[1,2,4],max_teams=3,same_club=False,save_fn=None):
        self.clubs=[]
        self.name=name
        self.list_games=list_games
        self.battles=dict()
        self.same_club=same_club
        self.max_teams=max_teams
        self._save_fn=save_fn

    def add_club(self,club):
        myclub = deepcopy(club)
        for nbp in self.list_games:
            if nbp not in myclub.teams:
                continue
            last_team=club.teams[nbp][-1]
            for i in range(club.get_num_teams(nbp),self.max_teams):
                tmp = deepcopy(last_team)
                tmp.name+="_%d" %i
                myclub.add_team(tmp)
            if len(myclub.teams[nbp])>self.max_teams:
                myclub.teams[nbp]=myclub.teams[nbp][:self.max_teams]
        self.clubs.append(myclub)

    def get_battles(self,nbp=None,login=None,club=None,team=None,only=False):
        res =[]
        if nbp:
            if type(nbp) !=list:
                nbp=[nbp]
            for i in nbp:
                res+=self.battles[i]
        else:
            for p in self.battles.values():
                res+=p
        if club:
            if type(club) != list:
                club = [club]
            if only:
                res=[x for x in res if x.team1.club.name in club and x.team2.club.name in club]
            else:
                res=[x for x in res if x.team1.club.name in club or x.team2.club.name in club]
        if login:
            if type(login) != list:
                login=[login]
            if only:
                res=[x for x in res if x.team1.club.login in login and x.team2.club.login in login]
            else:
                res=[x for x in res if x.team1.club.login in login or x.team2.club.login in login]
        if team:
            if type(team) != list:
                team=[team]
            if only:
                res=[x for x in res if x.team1.name in team and x.team2.name in team]
            else:
                res=[x for x in res if x.team1.name in team or x.team2.name in team]
        return res

    def init_battles(self):
        self.battles=dict()
        for nbp in self.list_games:
            self.battles[nbp]=list()

        for club1 in range(len(self.clubs)):
            for club2 in range(club1+1 if not self.same_club else club1,len(self.clubs)):
                for nbp in self.list_games:
                    if nbp in self.clubs[club1].teams and nbp in self.clubs[club2].teams:
                        for team1 in self.clubs[club1].teams[nbp]:
                            for team2 in self.clubs[club2].teams[nbp]:
                                b_aller = mdpsoccer.SoccerBattle(team1,team2)
                                b_retour= mdpsoccer.SoccerBattle(team2,team1)
                                self.battles[nbp].append(b_aller)
                                self.battles[nbp].append(b_retour)
    def do_battles(self,nbgoals=10,max_time=5000):
        self.scores=dict()
        for nbp in self.list_games:
            print "Tournoi %d joueurs\n" % (nbp,)
            for i,b in enumerate(self.battles[nbp]):
                try:
                    if self.save_fn:
                        fn=self.save_fn
                        log=interfaces.LogObserver(fn,True)
                        log.set_soccer_battle(b)
                    b.run_multiple_battles(nbgoals,max_time)
                except Exception as e:
                    print "****** %s" % (e,)
                    traceback.print_exc()
                print "Game ended %d/%d: %s\n" % (i,len(self.battles[nbp])-1,b)
            self.scores[nbp]=self.build_scores(self.battles[nbp])
        return self.battles

    def do_some_battles(self,only=False,nbp=None,login=None,club=None,team=None,nbgoals=10,max_time=5000):
        res = self.get_battles(nbp,login,club,team,only)
        for i,b in enumerate(res):
            try:
                if self.save_fn:
                    fn="%s_%s(%s)_%s(%s).pkl" % (self.save_fn,clean_fn(b.team1.name),clean_fn(b.team1.club.name),\
                                                    clean_fn(b.team2.name),clean_fn(b.team2.club.name))
                    log=interfaces.LogObserver(fn)
                    log.set_soccer_battle(b)
                b.run_multiple_battles(nbgoals,max_time)
            except Exception as e:
                print "*******  %s" % (e,)
                traceback.print_exc()
            print "Game ended %d/%d : %s" % (i,len(res)-1,b)
        return res

    @staticmethod
    def build_scores(battles_list):
        res=dict()
        for b in battles_list:
            tup1 = (b.team1.club.login,b.team1.club.name,b.team1.name)
            tup2 = (b.team2.club.login,b.team2.club.name,b.team2.name)
            if tup1 not in res:
                res[tup1]=Score(b.team1)
            if tup2 not in res:
                res[tup2]=Score(b.team2)
            res[tup1].add_score(b.score_team1,b.score_team2,b.team2)
            res[tup2].add_score(b.score_team2,b.score_team1,b.team1)
        return res
