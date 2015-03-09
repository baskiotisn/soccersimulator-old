
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
    to_save=["_winning_team","score_team1","score_team2","max_steps","cur_step",\
            "cur_battle","battles_count"]
    def __init__(self,team1,team2,ball,cst=dict()):
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
        self.actions_team1=None
        self.actions_team2=None

        self.cst={"GAME_WIDTH":GAME_WIDTH,"GAME_HEIGHT":GAME_HEIGHT,
                "GAME_GOAL_HEIGHT":GAME_GOAL_HEIGHT,"PLAYER_RADIUS":PLAYER_RADIUS,
                "BALL_RADIUS":BALL_RADIUS,"maxPlayerSpeed":maxPlayerSpeed,
                "maxPlayerAcceleration":maxPlayerAcceleration,"playerBrackConstant":playerBrackConstant,
                "nbWithoutShoot":nbWithoutShoot,"maxPlayerShoot":maxPlayerShoot,
                "maxBallAcceleration":maxBallAcceleration,"shootRandomAngle":shootRandomAngle,
                "ballBrakeSquare":ballBrakeSquare,"ballBrakeConstant":ballBrakeConstant}
        self.cst.update(cst)
    def __eq__(self,other):
        return (self.team1 == other.team1) and (self.team2 == other.team2) and (self.ball == other.ball)
    def copy(self,safe=False):
        team1=self.team1.copy(safe)
        team2=self.team2.copy(safe)
        state=SoccerState(team1,team2,self.ball.copy(),self.cst)
        for k in self.to_save:
            state.__dict__[k]=self.__dict__[k]
        if self.actions_team1:
            state.actions_team1=[a.copy() for a in self.actions_team1]
        if self.actions_team2:
            state.actions_team2=[a.copy() for a in self.actions_team2]
        return state

    @property
    def winning_team(self):
        return self._winning_team
    @property
    def width(self):
        return self.cst["GAME_WIDTH"]
    @property
    def height(self):
        return self.cst["GAME_HEIGHT"]
    @height.setter
    def height(self,v):
        self.cst["GAME_HEIGHT"]=v
    @width.setter
    def width(self,v):
        self.cst["GAME_WIDTH"]=v
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
        return abs(y-(self.height/2))<self.cst["GAME_GOAL_HEIGHT"]/2


    """ implementation """

    def apply_action(self,player,action):
        if not action:
            return
        action_shoot=action.shoot.copy()
        action_acceleration=action.acceleration.copy()

        if action_shoot.norm>self.cst["maxPlayerShoot"]:
            action_shoot.norm=self.cst["maxPlayerShoot"]
        player.dec_num_before_shoot()
        if action_shoot.norm!=0:
            if (player.get_num_before_shoot()>0):
                action_shoot=Vector2D()
            else:
                player.init_num_before_shoot(self.cst["nbWithoutShoot"])

        dist_to_ball=player.position.distance(self.ball.position)

        if action_shoot.norm>0 and dist_to_ball<(self.cst["PLAYER_RADIUS"]+self.cst["BALL_RADIUS"]):
            angle_factor=1.-abs(math.cos((player.angle-action_shoot.angle)/2.))
            dist_factor=1.-dist_to_ball/(self.cst["PLAYER_RADIUS"]+self.cst["BALL_RADIUS"])
            action_shoot.scale(1-angle_factor*0.25-dist_factor*0.25)
            action_shoot.angle=action_shoot.angle+((2*random.random()-1.)*(angle_factor+dist_factor)/2.)*self.cst["shootRandomAngle"]*math.pi/2.
            self.sum_of_shoots+=action_shoot

        if action_acceleration.norm>self.cst["maxPlayerAcceleration"]:
            action_acceleration.norm=self.cst["maxPlayerAcceleration"]
        player.speed*=(1-self.cst["playerBrackConstant"])
        player.speed_v=player.speed_v+action_acceleration
        if player.speed>self.cst["maxPlayerSpeed"]:
            player.speed=self.cst["maxPlayerSpeed"]
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

        self.ball.speed.norm+=-self.cst["ballBrakeSquare"]*self.ball.speed.norm**2-self.cst["ballBrakeConstant"]*self.ball.speed.norm
        ## decomposition selon le vecteur unitaire de ball.speed
        snorm=self.sum_of_shoots.norm
        if snorm>0:
            u_s=self.sum_of_shoots.copy()
            u_s.normalize()
            u_t=Vector2D(-u_s.y,u_s.x)
            speed_abs=abs(self.ball.speed.scalar(u_s))
            speed_ortho=self.ball.speed.scalar(u_t)
            speed=Vector2D(speed_abs*u_s.x-speed_ortho*u_s.y,speed_abs*u_s.y+speed_ortho*u_s.x)
            speed+=self.sum_of_shoots
            self.ball.speed=speed

        if (self.ball.speed.norm>self.cst["maxBallAcceleration"]):
            self.ball.speed.norm=self.cst["maxBallAcceleration"]
        self.ball.position+=self.ball.speed

        if self.ball.position.x<0:
            if self.is_y_inside_goal(self.ball.position.y):
                self._winning_team=2
            else:
                self.ball.position.x=-self.ball.position.x
                self.ball.speed.x=-self.ball.speed.x
        if self.ball.position.y<0:
            self.ball.position.y=-self.ball.position.y
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

    def to_dic(self):
        res=dict()
        for k in self.to_save:
            res[k]=self.__dict__[k]
        res["team1.name"]=self.team1.name
        res["team2.name"]=self.team2.name
        #res["team1.club"]=self.team1.club.name
        #res["team2.club"]=self.team2.club.name
        res["team1"]=[ (p.name,p.strategy.name,p.position.x,p.position.y,p.angle,p.speed,p._num_before_shoot) for p in self.team1]
        res["team2"]=[ (p.name,p.strategy.name,p.position.x,p.position.y,p.angle,p.speed,p._num_before_shoot) for p in self.team2]
        res["ball"]=(self.ball.position.x,self.ball.position.y,self.ball.speed.x,self.ball.speed.y)
        res["actions_team1"]=None
        res["actions_team2"]=None
        if self.actions_team1:
            res["actions_team1"]=[(a.acceleration.x,a.acceleration.y,a.shoot.x,a.shoot.y) for a in self.actions_team1]
        if self.actions_team2:
            res["actions_team2"]=[(a.acceleration.x,a.acceleration.y,a.shoot.x,a.shoot.y) for a in self.actions_team2]
        return res
    @staticmethod
    def create_from_dic(dic,team1=None,team2=None):
        if not team1:
            team1=SoccerTeam(dic["team1.name"])
            for t in dic["team1"]:
                p=SoccerPlayer(t[0])
                team1.add_player(p)
        if not team2:
            team2=SoccerTeam(dic["team2.name"])
            for t in dic["team2"]:
                p=SoccerPlayer(t[0])
                team2.add_player(p)
        state=SoccerState(team1,team2,soccerobj.SoccerBall())
        state.from_dic(dic)
        return state
    def from_dic(self,dic):
        for i,t in enumerate(dic["team1"]):
            p=self.team1.players[i]
            p.strategy=strategies.SoccerStrategy(t[1])
            p.position.x,p.position.y,p.angle,p.speed,p._num_before_shoot=t[2:]
        for i,t in enumerate(dic["team2"]):
            p=self.team2.players[i]
            p.strategy=strategies.SoccerStrategy(t[1])
            p.position.x,p.position.y,p.angle,p.speed,p._num_before_shoot=t[2:]
        self.ball.position.x,self.ball.position.y,self.ball.speed.x,self.ball.speed.y=dic['ball']
        for k in self.to_save:
            self.__dict__[k]=dic[k]
        if dic["actions_team1"]:
            self.actions_team1=[SoccerAction(Vector2D(t[0],t[1]),Vector2D(t[2],t[3])) for t in dic["actions_team1"]]
        if dic["actions_team2"]:
            self.actions_team2=[SoccerAction(Vector2D(t[0],t[1]),Vector2D(t[2],t[3])) for t in dic["actions_team2"]]

    def to_blockfile(self):
#    to_save=["_winning_team","score_team1","score_team2","max_steps","cur_step",\"cur_battle","battles_count","_width","_height"]
        nbp=len(self.team1.players)
        res="|".join(str(x) for x in [nbp,self.team1.name,self.team2.name,\
                self._winning_team,self.score_team1,self.score_team2,self.max_steps,self.cur_step,\
                self.cur_battle,self.battles_count,self.width,self.height])
        res+="\n"
        res+="|".join("%.3f"  % (x,) for x in [self.ball.position.x,self.ball.position.y,self.ball.speed.x,self.ball.speed.y])
        res+="\n"
        for p in self.team1:
            res+="|".join(str(x) for x in [p.name.replace("|",""),p.strategy.name.replace("|",""),\
                "%.3f" %(p.position.x,),"%.3f" %(p.position.y,),"%.3f" %(p.angle,),"%.3f" %( p.speed,),\
                "%.3f" %(p._num_before_shoot,)])
            res+="\n"
        for p in self.team2:
            res+="|".join(str(x) for x in [p.name.replace("|",""),p.strategy.name.replace("|",""),\
                "%.3f" %(p.position.x,),"%.3f" %(p.position.y,),"%.3f" %(p.angle,),"%.3f" %( p.speed,),\
                "%.3f" %(p._num_before_shoot,)])
            res+="\n"
        if self.actions_team2 and self.actions_team1:
            for a in self.actions_team1:
                res+="|".join("%.3f" % (x,) for x in [a.acceleration.x,a.acceleration.y,a.shoot.x,a.shoot.y])
                res+="\n"
            for a in self.actions_team2:
                res+="|".join("%.3f" % (x,) for x in [a.acceleration.x,a.acceleration.y,a.shoot.x,a.shoot.y])
                res+="\n"
        return res
    @staticmethod
    def from_blockfile(block,team1=None,team2=None):
        lines=[l.split("|") for l in  block]
        #"import pdb
        #pdb.set_trace()
        info=lines.pop(0)
        nbp=int(info[0])
        ball_line=lines.pop(0)
        ball=soccerobj.SoccerBall(Vector2D(float(ball_line[0]),float(ball_line[1])),\
                Vector2D(float(ball_line[2]),float(ball_line[3])))
        t1_list=lines[0:nbp]
        t2_list=lines[nbp:2*nbp]
        a1_list=lines[2*nbp:3*nbp]
        a2_list=lines[3*nbp:4*nbp]
        if not team1:
            team1=soccerobj.SoccerTeam(info[1])
            for p in t1_list:
                team1.add_player(soccerobj.SoccerPlayer(p[0]))
        if not team2:
            team2=soccerobj.SoccerTeam(info[2])
            for p in t2_list:
                team2.add_player(soccerobj.SoccerPlayer(p[0]))
        state=SoccerState(team1,team2,ball)
        for l,p in zip(t1_list+t2_list,state.team1.players+state.team2.players):
            p.strategy=strategies.SoccerStrategy(l[1])
            p.position.x=float(l[2])
            p.position.y=float(l[3])
            p.angle=float(l[4])
            p.speed=float(l[5])

        state.actions_team1=[SoccerAction(Vector2D(float(a[0]),float(a[1])),\
                    Vector2D(float(a[2]),float(a[3]))) for a in a1_list]
        state.actions_team2=[SoccerAction(Vector2D(float(a[0]),float(a[1])),\
                    Vector2D(float(a[2]),float(a[3]))) for a in a2_list]
        state._winning_team,state.score_team1,state.score_team2,state.max_steps,\
            state.cur_step,state.cur_battle,state.battles_count,state.width,state.height=[int(x) for x in info[3:]]
        return state



###############################################################################
# SoccerBattle
###############################################################################

class SoccerBattle(object):
    def __init__(self,team1,team2,battles_count=1,max_steps=2000,cst=dict()):
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
        self.cst=dict(cst)

    @staticmethod
    def from_save(dic):
        res=dic["soccer_battle"]
        res.battles=[ [SoccerState.create_from_dic(s,res.team1,res.team2) for s in battle] for battle in dic["battles"] ]
        return res
    def copy(self,safe=False):
        battle=SoccerBattle(self.team1.copy(safe),self.team2.copy(safe),self.battles_count,self.max_steps)
        battle.score_team1=self.score_team1
        battle.score_team2=self.score_team2
        battle.score_draw=self.score_draw
        if self.state:
            battle.state=self.state.copy(safe)
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
        if self.state.winning_team!=0 or self.cur_step>=self.max_steps:
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
        state=SoccerState(self.team1.copy(),self.team2.copy(),soccerobj.SoccerBall(),self.cst)
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
