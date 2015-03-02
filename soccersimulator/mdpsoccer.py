# -*- coding: utf-8 -*-<
from soccer_base import *
import soccerobj
import numpy as np
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
        return np.sqrt(self.width**2+self.height**2)
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
        return np.abs(y-(self.height/2))<GAME_GOAL_HEIGHT/2


    """ implementation """

    def apply_action(self,player,action):
        if not action:
            return
        player.dec_num_before_shoot()
        action_shoot=action.shoot.copy()
        action_acceleration=action.acceleration.copy()
        if (player.position.distance(self.ball.position)<(PLAYER_RADIUS+BALL_RADIUS)):
            if (player.get_num_before_shoot()>0):
                action_shoot=Vector2D()
            else:
                player.init_num_before_shoot()
            if action_shoot.norm>maxPlayerShoot:
                action_shoot.product(1.0/action_shoot.norm * maxPlayerShoot)
            if action_shoot.norm>0:
                player_speed=Vector2D.create_polar(player.angle,player.speed)
                dot_p=action_shoot.dot(player_speed)/(action_shoot.norm*player_speed.norm)
                if player_speed.norm==0:
                    fake_speed=Vector2D.create_polar(player.angle,1)
                    dot_p=action_shoot.dot(fake_speed)/(action_shoot.norm*fake_speed.norm)
                dot_p+=2
                dot_p/=3.
                if (dot_p<0.5):
                    dot_p=0.5
                action_shoot.product(dot_p)
                action_shoot+=player_speed
                norm=action_shoot.norm
                angle=np.arctan2(action_shoot.y,action_shoot.x)
                angle+=(np.random.rand()*2.-1)*shootRandomAngle/180.*np.pi
                action_shoot=Vector2D.create_polar(angle,norm)
                self.sum_of_shoots+=action_shoot

        norm = action_acceleration.norm
        if norm>maxPlayerAcceleration:
            action_acceleration.product(1./norm*maxPlayerAcceleration)
        frotte=Vector2D.create_polar(player.angle,-player.speed)
        frotte.product(playerBrackConstant)
        resultante=frotte
        resultante+=action_acceleration
        new_speed=Vector2D.create_polar(player.angle,player.speed)
        new_speed+=resultante
        new_player_speed=new_speed.norm
        if (new_player_speed>0):
            new_player_angle=np.arctan2(new_speed.y,new_speed.x)
            if new_player_speed>maxPlayerSpeed:
                new_player_speed=maxPlayerSpeed

            new_player_position=player.position.copy()
            new_player_position+=new_speed

            if new_player_position.x<0:
                new_player_position.x=0
                new_player_speed=0
            if new_player_position.y<0:
                new_player_position.y=0
                new_player_speed=0
            if new_player_position.x>self.width:
                new_player_position.x=self.width
                new_player_speed=0
            if new_player_position.y>self.height:
                new_player_position.y=self.height
                new_player_speed=0
            player.angle=new_player_angle
            player.speed=new_player_speed
            player.position=new_player_position

    def apply_actions(self):
        self.sum_of_shoots=Vector2D()
        for i,action in enumerate(self.actions_team1):
            self.apply_action(self.team1[i],action)
        for i,action in enumerate(self.actions_team2):
            self.apply_action(self.team2[i],action)

        frotte_ball_square=self.ball.speed.copy()
        coeff_frottement_square=ballBrakeSquare*(self.ball.speed.norm**2)
        frotte_ball_square.product(-coeff_frottement_square)
        frotte_ball_constant=self.ball.speed.copy()
        coeff_frottement_constant=ballBrakeConstant
        frotte_ball_constant.product(-coeff_frottement_constant)

        new_ball_speed=self.ball.speed
        no=self.sum_of_shoots.norm
        if no!=0:
            if (no>maxBallAcceleration):
                self.sum_of_shoots.product(1./no*maxBallAcceleration)
            new_ball_speed=self.sum_of_shoots.copy()
        new_ball_speed+=frotte_ball_square
        new_ball_speed+=frotte_ball_constant

        self.ball.speed=new_ball_speed
        new_ball_position=self.ball.position
        new_ball_position+=new_ball_speed
        self.ball.position=new_ball_position

        pos=self.ball.position
        speed=self.ball.speed
        if pos.x<0:
            if self.is_y_inside_goal(pos.y):
                self._winning_team=2
            else:
                self.ball.position=Vector2D(-pos.x,pos.y)
                self.ball.speed=Vector2D(-speed.x,speed.y)
        if pos.y<0:
            self.ball.position=Vector2D(pos.x,-pos.y)
            self.ball.speed=Vector2D(speed.x,-speed.y)
        if pos.x>self.width:
            if self.is_y_inside_goal(pos.y):
                self._winning_team=1
            else:
                self.ball.position=Vector2D(self.width-(pos.x-self.width),pos.y)
                self.ball.speed=Vector2D(-speed.x,speed.y)
        if pos.y>self.height:
            self.ball.position=Vector2D(pos.x,self.height-(pos.y-self.height))
            self.ball.speed=Vector2D(speed.x,-speed.y)
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

    def run_multiple_battles(self,battles_count=None,max_steps=None):
        self._is_ready=False
        self._ongoing=True
        if battles_count:
            self.battles_count=battles_count
        if max_steps:
            self.max_steps=max_steps
        self.begin_battles(self.battles_count,self.max_steps)
        self.next_battle()
        self._is_ready=True
        if not self._father:
            while self._ongoing:
                self.update()

    def start_by_thread(self,father,battles_count=None,max_steps=None):
        self._father=father
        self._is_ready=False
        self._ongoing=True
        self.run_multiple_battles(battles_count,max_steps)

    def update(self):
        if not self._is_ready or not self._ongoing:
            return
        self._is_ready=False
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
        for i,p in enumerate(st.team1.players):
            self.team1[i].strategy=p.strategy
        st=state.copy()
        self.team2.begin_battles(st,battles_count,max_steps)
        for i,p in enumerate(st.team2.players):
            self.team2[i].strategy=p.strategy

    def end_battles(self):
        self.team1.end_battles()
        self.team2.end_battles()
        self.listeners.end_battles()
        self._ongoing=False

    def start_battle(self):
        self.cur_step=0
        self.state=self.create_initial_state()
        self.state.cur_battle=self.cur_battle
        self.state.score_team1=self.score_team1
        self.state.score_team2=self.score_team2
        st1 = self.state.copy()
        st2 = self.state.copy()
        st1.team1.start_battle(st1)
        for i,p in enumerate(st1.team1.players):
            self.state.team1[i].strategy=p.strategy
        st = self.state.copy()
        st2.team2.start_battle(st2)
        for i,p in enumerate(st2.team2.players):
            self.state.team2[i].strategy=p.strategy
        st = self.state.copy()
        self.listeners.start_battle(st)

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

    def next_step(self):
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
        return False

    def create_initial_state(self):
        state=SoccerState(self.team1.copy(),self.team2.copy(),soccerobj.SoccerBall())
        quarters=[i*state.height/4 for i in range(1,4)]
        rows=[state.width*0.1,state.width*0.35,state.width*(1-0.35),state.width*(1-0.1)]
        if self.num_players!=1 and self.num_players!=2 and self.num_players !=4:
            raise Exception("create_initial_state : Nombre de joueurs incorrects %d" % self.num_players)
        if self.num_players==1:
            state.team1[0].set_position(rows[0],quarters[1],0)
            state.team2[0].set_position(rows[3],quarters[1],np.pi)
        if self.num_players==2:
            state.team1[0].set_position(rows[0],quarters[0],0)
            state.team1[1].set_position(rows[0],quarters[2],0)
            state.team2[0].set_position(rows[3],quarters[0],np.pi)
            state.team2[1].set_position(rows[3],quarters[2],np.pi)
        if self.num_players==4:
            state.team1[0].set_position(rows[0],quarters[0],0)
            state.team1[1].set_position(rows[0],quarters[2],0)
            state.team1[2].set_position(rows[1],quarters[0],0)
            state.team1[3].set_position(rows[1],quarters[2],0)
            state.team2[0].set_position(rows[3],quarters[0],np.pi)
            state.team2[1].set_position(rows[3],quarters[2],np.pi)
            state.team2[2].set_position(rows[2],quarters[0],np.pi)
            state.team2[3].set_position(rows[2],quarters[2],np.pi)
        state.ball.position.x=state.width/2
        state.ball.position.y=state.height/2
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
