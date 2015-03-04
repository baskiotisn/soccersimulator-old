
# -*- coding: utf-8 -*-<
from soccer_base import *
import soccerobj
import math
import time

from copy import deepcopy
import strategies

###############################################################################
# SoccerAction
###############################################################################

class SoccerAction(object):
    def __init__(self,acceleration=Vector2D(),shoot=Vector2D()):
        self.acceleration=acceleration
        self.shoot=shoot
    def copy(self):
        return SoccerAction(self.acceleration.copy(),self.shoot.copy())
    def __str__(self):
        return "%s %s" % (self.acceleration,self.shoot)
    def __eq__(self,other):
        return (other.acceleration==self.acceleration) and (other.shoot==self.shoot)
    def __add__(self,other):
        return SoccerAction(self.acceleration+other.acceleration,self.shoot+other.shoot)
    def __sub__(self,other):
        return Vector2D(self.acceleration-other.acceleration,self.shoot-other.shoot)
    def __iadd__(self,other):
       self.acceleration+=other.acceleration
       self.shoot+=other.shoot
       return self
    def __isub__(self,other):
        self.acceleration-=other.acceleration
        self.shoot-=other.shoot
        return self



###############################################################################
# SoccerState
#########################    e######################################################

class SoccerState:
    def __init__(self,team1,team2,ball):
        self.team1=team1
        self.team2=team2
        self._winning_team=0
        self.score_team1=0
        self.score_team2=0
        self.max_steps=0
        self.cur_step=0
        self.cur_battle=0
        self.battles_count=0
        self.ball=ball
        self._width=GAME_WIDTH
        self._height=GAME_HEIGHT
        self.actions_team1=None
        self.actions_team2=None
    def __eq__(self,other):
        return (self.team1 == other.team1) and (self.team2 == other.team2) and (self.ball == other.ball)
    def copy_safe(self):
        team1=self.team1.copy_safe()
        team2=self.team2.copy_safe()
        state=SoccerState(team1,team2,self.ball.copy())
        state._winning_team=self._winning_team
        state._width=self._width
        state._height=self._height
        state.actions_team1=self.actions_team1
        state.actions_team2=self.actions_team2
        state.score_team1=self.score_team1
        state.score_team2=self.score_team2
        state.max_steps=self.max_steps
        state.cur_battle=self.cur_battle
        state.cur_step=self.cur_step
        state.battles_count=self.battles_count
        return state
    def copy(self):
        team1=self.team1.copy()
        team2=self.team2.copy()
        state=SoccerState(team1,team2,self.ball.copy())
        state._winning_team=self._winning_team
        state._width=self._width
        state._height=self._height
        state.actions_team1=self.actions_team1
        state.actions_team2=self.actions_team2
        state.score_team1=self.score_team1
        state.score_team2=self.score_team2
        state.max_steps=self.max_steps
        state.cur_battle=self.cur_battle
        state.cur_step=self.cur_step
        state.battles_count=self.battles_count
        return state

    @property
    def winning_team(self):
        return self._winning_team
    @property
    def width(self):
        return self._width
    @property
    def height(self):
        return self._height
    @property
    def diagonal(self):
        return math.sqrt(self.width**2+self.height**2)
    def get_team(self,teamid):
        if teamid==1:
            return self.team1
        if teamid==2:
            return self.team2
        raise Exception("get_team : team demandé != 1 ou 2 : %s" % i)

    def get_player(self,num_team,player):
       return self.get_team(num_team).get_player(player)

    def get_goal_center(self,teamid):
        if (teamid==1):
            return Vector2D(0,self.height/2.)
        if (teamid==2):
            return Vector2D(self.width,self.height/2.)
        raise Exception("get_goal_center : team demandé != 1 ou 2 : %s" % i)

    def is_y_inside_goal(self,y):
        return abs(y-(self.height/2))<GAME_GOAL_HEIGHT/2


    """ implementation """

    def apply_action(self,player,action):
        if not action:
            return
        action_shoot=action.shoot.copy()
        action_acceleration=action.acceleration.copy()

        if action_shoot.norm>maxPlayerShoot:
            action_shoot.norm=maxPlayerShoot
        player.dec_num_before_shoot()
        if action_shoot.norm!=0:
            if (player.get_num_before_shoot()>0):
                action_shoot=Vector2D()
            else:
                player.init_num_before_shoot()

        dist_to_ball=player.position.distance(self.ball.position)

        if action_shoot.norm>0 and dist_to_ball<(PLAYER_RADIUS+BALL_RADIUS):
            angle_factor=1.-abs(math.cos(player.angle-action_shoot.angle))
            dist_factor=1.-dist_to_ball/(PLAYER_RADIUS+BALL_RADIUS)
            action_shoot.scale(1-angle_factor*0.25-dist_factor*0.25)
            action_shoot.angle=action_shoot.angle+(random.random()*(angle_factor+dist_factor)/2.)*shootRandomAngle*math.pi/2.
            self.sum_of_shoots+=action_shoot

        if action_acceleration.norm>maxPlayerAcceleration:
            action_acceleration.norm=maxPlayerAcceleration
        player.speed*=(1-playerBrackConstant)
        player.speed_v=player.speed_v+action_acceleration
        if player.speed>maxPlayerSpeed:
            player.speed=maxPlayerSpeed
        player.position=player.position+player.speed_v
        if player.position.x<0:
            player.position.x=0
            player.speed=0
        if player.position.y<0:
            player.position.y=0
            player.speed=0
        if player.position.x>self.width:
            player.position.x=self.width
            player.speed=0
        if player.position.y>self.height:
            player.position.y=self.height
            player.speed=0

    def apply_actions(self):
        self.sum_of_shoots=Vector2D()
        for i,action in enumerate(self.actions_team1):
            self.apply_action(self.team1[i],action)
        for i,action in enumerate(self.actions_team2):
            self.apply_action(self.team2[i],action)

        self.ball.speed.norm+=-ballBrakeSquare*self.ball.speed.norm**2-ballBrakeConstant*self.ball.speed.norm
        self.ball.speed+=self.sum_of_shoots
        if (self.ball.speed.norm>maxBallAcceleration):
            self.ball.speed.norm=maxBallAcceleration
        self.ball.position+=self.ball.speed

        if self.ball.position.x<0:
            if self.is_y_inside_goal(self.ball.position.y):
                self._winning_team=2
            else:
                self.ball.position.x=-self.ball.position.x
                self.ball.speed.x=-self.ball.speed.x
        if self.ball.position.y<0:
            self.ball.position.y=self.ball.position.y
            self.ball.speed.y=-self.ball.speed.y
        if self.ball.position.x>self.width:
            if self.is_y_inside_goal(self.ball.position.y):
                self._winning_team=1
            else:
                self.ball.position.x=2*self.width-self.ball.position.x
                self.ball.speed.x=-self.ball.speed.x
        if self.ball.position.y>self.height:
            self.ball.position.y=2*self.height-self.ball.position.y
            self.ball.speed.y=-self.ball.speed.y
    def __str__(self):
        return str(self.ball)+"\n"+ str(self.team1)+"\n"+str(self.team2)


###############################################################################
# SoccerBattle
###############################################################################

class SoccerBattle(object):
    def __init__(self,team1,team2,battles_count=1,max_steps=MAX_GAME_STEPS):
        if team1.num_players != team2.num_players:
            raise Exception("Les equipes n'ont pas le meme nombre de joueurs")
        self.team1=team1
        self.team2=team2
        self.score_team1=0
        self.score_team2=0
        self.score_draw=0
        self.listeners=SoccerEvents()
        self.battles_count=battles_count
        self.max_steps=max_steps
        self.state=None
        self.cur_step=0
        self.cur_battle=0
        self._is_ready=False
        self._ongoing=False
        self._father=None
        self.obs=None
        self._speed=False

    def copy_safe(self):
        battle=SoccerBattle(self.team1.copy_safe(),self.team2.copy_safe(),self.battles_count,self.max_steps)
        battle.score_team1=self.score_team1
        battle.score_team2=self.score_team2
        battle.score_draw=self.score_draw
        if self.state:
            battle.state=self.state.copy_safe()
        return battle
    def __str__(self):
        return "%s vs %s : %s-%s (%s)" %(str(self.team1), str(self.team2), str(self.score_team1),str(self.score_team2),str(self.score_draw))
    def init_score(self):
        self.score_team1=0
        self.score_team2=0
        self.score_draw=0
    @property
    def num_players(self):
        return self.team1.num_players

    def run_multiple_battles(self,battles_count=None,max_steps=None,father=None):
        self._is_ready=False
        self._ongoing=True
        self._father=father
        if battles_count:
            self.battles_count=battles_count
        if max_steps:
            self.max_steps=max_steps
        self.begin_battles(self.battles_count,self.max_steps)
        self.next_battle()
        self._is_ready=True
        if not self._father:
            self.run_until_end()

    def run_until_end(self):
        while 1:
            if not self._ongoing:
                break
            self.update()
            time.sleep(0.000001)
    def run_until_next(self):
        while 1:
            if not self.next_step():
                break
        self.next_battle()
        self._is_ready=True

    def update(self):
        if not self._is_ready or not self._ongoing:
            return
        self._is_ready=False
        if self._speed:
            self.run_until_next()
            self._is_ready=True
            return
        if not self.next_step():
            self.next_battle()
        self._is_ready=True

    def next_battle(self):
        if self.cur_battle<self.battles_count:
                self.cur_battle+=1
                self.start_battle()
        else:
            self.end_battles()

    def begin_battles(self,battles_count,max_steps):
        self.init_score()
        self.cur_battle=0
        state=self.create_initial_state()
        st=state.copy()
        self.listeners.begin_battles(st,battles_count,max_steps)
        st=state.copy()
        self.team1.begin_battles(st,battles_count,max_steps)
        st=state.copy()
        self.team2.begin_battles(st,battles_count,max_steps)
        if self.obs:
            self.obs.begin_battles(battles_count,max_steps)
    def end_battles(self):
        self.team1.end_battles()
        self.team2.end_battles()
        self.listeners.end_battles()
        self._ongoing=False
        if self.obs:
            self.obs.end_battles()
    def start_battle(self):
        self.cur_step=0
        self.state=self.create_initial_state()
        self.state.cur_battle=self.cur_battle
        self.state.score_team1=self.score_team1
        self.state.score_team2=self.score_team2
        st1 = self.state.copy()
        st2 = self.state.copy()
        st = self.state.copy()
        self.state.team1.start_battle(st1)
        self.state.team2.start_battle(st2)
        self.listeners.start_battle(st)
        if self.obs:
            self.obs.start_battle()
    def finish_battle(self):
        if self.state.winning_team==0:
            self.state.team1.finish_battle(0)
            self.state.team2.finish_battle(0)
        if self.state.winning_team==1:
            self.state.team1.finish_battle(1)
            self.state.team2.finish_battle(-1)
        if self.state.winning_team==2:
            self.state.team1.finish_battle(-1)
            self.state.team2.finish_battle(1)
        for i,p in enumerate(self.state.team1.players):
            self.team1[i].strategy=p.strategy
        for i,p in enumerate(self.state.team2.players):
            self.team2[i].strategy=p.strategy
        self.listeners.finish_battle(self.state.winning_team)
        if self.obs:
            self.obs.finish_battle(self.state.winning_team)
    def next_step(self):
        if self.state.winning_team!=0:
            return False
        if self.cur_step<self.max_steps:
            self.state.cur_step=self.cur_step
            st1=self.state.copy()
            st2=self.state.copy()
            self.state.actions_team1=st1.team1.compute_strategies(st1,1)
            for j,p in enumerate(st1.team1.players):
                self.state.team1[j].strategy=p.strategy
            self.state.actions_team2=st2.team2.compute_strategies(st2,2)
            self.state.team1._exceptions=st1.team1._exceptions
            for j,p in enumerate(st2.team2.players):
                self.state.team2[j].strategy=p.strategy
            self.state.apply_actions()
            self.state.team2._exceptions=st2.team2._exceptions
            st = self.state.copy()
            self.listeners.update_battle(st,self.cur_step)
            self.cur_step+=1
            if len(st1.team1.exceptions)>NB_MAX_EXCEPTIONS:
                self.state.winning_team=2
                print "\033[91m Too much exceptions for \033[92m %s \033[0m, last one :\n" % (st1.team1.name,)
                print st1.team1.exceptions[-1][1]
            if len(st2.team2.exceptions)>NB_MAX_EXCEPTIONS:
                self.state.winning_team=1
                print "\033[91m Too much exceptions for \033[92m %s \033[0m, last one : \n" % (st2.team2.name,)
                print st2.team2.exceptions[-1][1]

            if self.state.winning_team==0:
                return True
        if self.state.winning_team==1:
            self.score_team1+=1
        if self.state.winning_team==2:
            self.score_team2+=1
        if self.state.winning_team==0:
            self.score_draw+=1
        self.finish_battle()
        return True

    def create_initial_state(self):
        state=SoccerState(self.team1.copy(),self.team2.copy(),soccerobj.SoccerBall())
        quarters=[i*state.height/4 for i in range(1,4)]
        rows=[state.width*0.1,state.width*0.35,state.width*(1-0.35),state.width*(1-0.1)]
        if self.num_players!=1 and self.num_players!=2 and self.num_players !=4:
            raise Exception("create_initial_state : Nombre de joueurs incorrects %d" % self.num_players)
        if self.num_players==1:
            state.team1[0].set_position(rows[0],quarters[1],0)
            state.team2[0].set_position(rows[3],quarters[1],math.pi)
        if self.num_players==2:
            state.team1[0].set_position(rows[0],quarters[0],0)
            state.team1[1].set_position(rows[0],quarters[2],0)
            state.team2[0].set_position(rows[3],quarters[0],math.pi)
            state.team2[1].set_position(rows[3],quarters[2],math.pi)
        if self.num_players==4:
            state.team1[0].set_position(rows[0],quarters[0],0)
            state.team1[1].set_position(rows[0],quarters[2],0)
            state.team1[2].set_position(rows[1],quarters[0],0)
            state.team1[3].set_position(rows[1],quarters[2],0)
            state.team2[0].set_position(rows[3],quarters[0],math.pi)
            state.team2[1].set_position(rows[3],quarters[2],math.pi)
            state.team2[2].set_position(rows[2],quarters[0],math.pi)
            state.team2[3].set_position(rows[2],quarters[2],math.pi)
        state.ball.position.x=state.width/2
        state.ball.position.y=state.height/2
        state.ball.speed=Vector2D()
        state.max_steps=self.max_steps
        state.battles_count=self.battles_count
        state.cur_battle=self.cur_battle
        return state

    def send_to_strat(self,*args,**kwargs):
        if self.state:
            for p in self.state.team1.players:
                if hasattr(p.strategy,"send_to_strat"):
                        p.strategy.send_to_strat(1,p,*args,**kwargs)
            for p in self.state.team2.players:
                if hasattr(p.strategy,"send_to_strat"):
                        p.strategy.send_to_strat(2,p,*args,**kwargs)


class Events(object):
    def __init__(self):
       for e in self.__events__:
           self.__getattr__(e)
    def __getattr__(self, name):
      if hasattr(self.__class__, '__events__'):
         assert name in self.__class__.__events__, \
                "Event '%s' is not declared" % name
      self.__dict__[name] = ev = _EventSlot(name)
      return ev
    def __str__(self): return 'Events :' + str(list(self))
    __repr__ = __str__
    def __len__(self):
       if len(self.__dict__)!=0:
           return len(self.__dict__.values()[0])

       return 0

    def __iter__(self):
      def gen(dictitems=self.__dict__.items()):
         for attr, val in dictitems:
            if isinstance(val, _EventSlot):
               yield val
      return gen()
    def __getstate__(self):
        return dict()
    def __setstate__(self,d):
        pass


class _EventSlot(object):
   def __init__(self, name):
      self.targets = []
      self.__name__ = name
   def __repr__(self):
      return self.__name__
   def __call__(self, *a, **kw):
      return [ f(*a, **kw) for f in self.targets]
   def __iadd__(self, f):
      self.targets.append(f)
      return self
   def __isub__(self, f):
      while f in self.targets: self.targets.remove(f)
      return self
   def __len__(self):
       return len(self.targets)

class SoccerEvents(Events):
    __events__=('begin_battles','start_battle','update_battle','finish_battle','end_battles','is_ready')
    def __iadd__(self,f):
        for e in self:
            try:
                e+=getattr(f,str(e))
            except:
                    print "no %s supported by this interface" %e
        return self
    def __isub__(self, f):
        for e in self:
            while getattr(f,e) in e.targets: e.targets.remove(getattr(f,e))
        return self
