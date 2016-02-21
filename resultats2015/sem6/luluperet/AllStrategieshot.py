import soccersimulator, soccersimulator.settings,math
from soccersimulator.settings import *
from soccersimulator import SoccerTeam as STe,SoccerMatch as SM, Player, SoccerTournament as ST, BaseStrategy as AS, SoccerAction as SA, Vector2D as V2D,SoccerState as SS, MobileMixin as MM
from soccersimulator.mdpsoccer import Ball
from random import randint,uniform

settings=soccersimulator.settings

T1_BUT=GAME_WIDTH
T2_BUT=0
T1_SENS=1
T2_SENS=-1
COEFF_FORCEUR=5
GOAL1=V2D(T2_BUT,GAME_HEIGHT/2)
GOAL2=V2D(T1_BUT,GAME_HEIGHT/2)
ZONE_GOAL=0
ANGLE1=0
ANGLE2=math.pi
GOAL_ATTACK=20
GOAL_ALERT=60
INCER=10
BALLE_MIN_VITESSE=0.5578
BALLE_MAX_NORM=1
RAYON_BALL_PLAYER=PLAYER_RADIUS + BALL_RADIUS
NORM_DVT=0.5
MODULO_GOAL=2
GOAL_ATTACK2=20
GAMMA=1.5

TO_GOAL=2
TO_ATTACK=3
TO_FORCEUR=1


class clever(object):
        def __init__(self):
                self.auto1_attack=1
                self.auto1_goal=1
                self.auto_goal_inside=1
                self.auto1_round=0
                self.onetoone_begin_round=1
                self.auto1_all=1
                self.one_to_one_goal_auto1=1
                self.two_to_two_goal_attack=0
                self.one_to_one_goal_attack=0
                self.one_to_one_goal_max=0
                self.master=0
                self.history_me={}
                self.tech=[1,2,3]
                self.one_to_one_goal_attack_master=0
                self.two_to_two_goal_attack_master=0
                self.one_to_one_attack_goal_master=0
                self.two_to_two_attack_goal_master=0
                self.one_to_one_goal_forceur_master=0
                self.two_to_two_goal_forceur_master=0
                self.one_to_one_forceur_goal_master=0
                self.two_to_two_forceur_goal_master=0
                self.one_to_one_forceur_attack_master=0
                self.two_to_two_forceur_attack_master=0
                self.one_to_one_attack_forceur_master=0
                self.two_to_two_attack_forceur_master=0
                self.count=0
        
        def ajoute(self,nom,val):
                self.nom=val
        
        def begin_round(self):
                self.onetoone_begin_round=1
                self.one_to_one_goal_auto1=1
                self.one_to_one_goal_max=0
                self.two_to_two_goal_attack=0
                self.one_to_one_goal_attack=0
        
        def auto_master(self,num,bibli):
            nb_p=bibli.nb_p()
            self.clean_master()
            if nb_p==2:
                if num==1:
                    self.master=1
                    if self.master==2:
                        self.one_to_one_goal_forceur_master=1
                        return
                    elif self.master==3:
                        self.one_to_one_attack_forceur_master=1
                        return
                elif num==2:
                    self.master=2
                    if self.master==1:
                        self.one_to_one_forceur_goal_master=1
                        return
                    elif self.master==3:
                        self.one_to_one_attack_goal_master=1
                        return
                elif num==3:
                    self.master=3
                    if self.master==1:
                        self.one_to_one_forceur_attack_master=1
                        return
                    elif self.master==2:
                        self.one_to_one_goal_attack_master=1
                        return

            elif nb_p==4:
                if num==1:
                    self.master=1
                    if self.master==2:
                        self.two_to_two_goal_forceur_master=1
                        return
                    elif self.master==3:
                        self.two_to_two_attack_forceur_master=1
                        return
                elif num==2:
                    self.master=2
                    if self.master==1:
                        self.two_to_two_forceur_goal_master=1
                        return
                    elif self.master==3:
                        self.two_to_two_attack_goal_master=1
                        return
                elif num==3:
                    self.master=3
                    if self.master==1:
                        self.two_to_two_forceur_attack_master=1
                        return
                    elif self.master==2:
                        self.two_to_two_goal_attack_master=1
                        return

        
        
        def check(self,bibli):
            print("check")
            y = self.tech[:]
            for key, value in self.history_me.iteritems():
                if value != bibli.id_team:
                    y.remove(key)
            if len(y) > 0:
                print("auto-mzsret",y[0])
                self.auto_master(y[0],bibli)
            else:
                print("PLUS DE STRATEGIES")
                self.count+=1
                if self.count==3:
                    self.count=0
                    self.history_me.clear()
                    self.check(bibli)
                
            
            return
    
        def end_round(self,state,bibli):
            self.history_me[self.master]=state._winning_team
            if state._winning_team != bibli.id_team:
                self.check(bibli)
            return

        def clean_master(self):
            self.one_to_one_goal_attack_master=0
            self.two_to_two_goal_attack_master=0
            self.one_to_one_attack_goal_master=0
            self.two_to_two_attack_goal_master=0
            self.one_to_one_goal_forceur_master=0
            self.two_to_two_goal_forceur_master=0
            self.one_to_one_forceur_goal_master=0
            self.two_to_two_forceur_goal_master=0
            self.one_to_one_forceur_attack_master=0
            self.two_to_two_forceur_attack_master=0
            self.one_to_one_attack_forceur_master=0
            self.two_to_two_attack_forceur_master=0

class StatePlayer:
    def __init__(self,state,id_team,id_player):
        self.state=state
        self.id_team=id_team
        self.id_player=id_player
        if id_team==1:
            self._autre=2
        elif id_team==2:
            self._autre=1
        self.moi=self.config=state.player(id_team,id_player)
        self.ma_position=self.moi.position
        self.ma_vitesse=self.moi.vitesse

    @property
    def ma_position_m(self):
        return usefull().mirror(self.ma_position,self.id_team)
    
    def __getattr__(self,name):
        return getattr(self.state,name)

class StateTerrain:
    def __init__(self,state,id_team,id_player):
        self.state=state
        self._state=state
        self.id_team=id_team
        self.id_player=id_player
        if id_team==1:
            self.mes_goal=self.goal=GOAL1
            self.autre_goal=self.goal2=GOAL2
            self.mon_sens=self.sens=T1_SENS
        elif id_team==2:
            self.mes_goal=self.goal=GOAL2
            self.autre_goal=self.goal2=GOAL1
            self.mon_sens=self.sens=T2_SENS
    
    def __getattr__(self,name):
        return getattr(self.state,name)

class StateBall:
    def __init__(self,state,id_team,id_player):
        self.state=state
        self.id_team=id_team
        self.id_player=id_player
        self.ball=self.state.ball
        self.ball_position=self.ball.position
        self.ball_vitesse=self.ball.position

    def __getattr__(self,name):
        return getattr(self.state,name)

class AllState:
    def __init__(self,state,id_team,id_player):
        self.state=StatePlayer(StateBall(StateTerrain(state,id_team,id_player),id_team,id_player),id_team,id_player)
        self.id_team=id_team
        self.id_player=id_player
    
    def __getattr__(self,name):
        return getattr(self.state,name)
class usefull:
    def __init__(self):
        self.name="d"
    
    def get_attr(self,a,b,c):
        try:
            return getattr(a, c)
        except:
            return getattr(b,c)
    def simulate(self,config,state):
        i=0
        a=state.ball
        print("ball-dvt while")
        while self.balle_dvt(config,state.id_team,a) and i<=10:
            print("a",a)
            print("ball dvt if")
            if self.balle_dvt(config,state.id_team,self.next_position_ball(a)):
                a=self.next_position_ball(a)
                print("a")
            else:
                return a
            i+=1
        i=0
        return a
    def next_position_player(self,dis,config):
        config_state_vitesse = config._state.vitesse * (1 - settings.playerBrackConstant) #frottemnt
        config_state_vitesse = (config_state_vitesse+dis.norm_max(settings.maxPlayerAcceleration)).norm_max(settings.maxPlayerSpeed)
        config_state_position = config._state.position+ config_state_vitesse.norm_max(settings.maxPlayerSpeed)
        return config_state_position
    
    def balle_dvt(self,config,id_team,ball):
        print("ball-dvt",ball,config)
        if id_team==1:
            return ball.position.x > config.position.x
        else:
            return ball.position.x<config.position.x
            
    def has_ball(self,ball,position,m=0):
        try:
            return ball.position.distance(position) <= RAYON_BALL_PLAYER + m
        except:
            return ball.ball.position.distance(position) <= RAYON_BALL_PLAYER + m

    def has_ball_merge(self,ball,position,m):
        return self.has_ball(ball,position,m)
    
    def has_ball_next(self,state,id_team,id_player):
        dis=state.ball.position - state.player_state(id_team, id_player).position
        config=state.player(id_team,id_player)
        f=self.next_position_player(dis,config)
        return self.has_ball(state,f)
    
    def _near_of_me(self,config1,id_team,state):
        po=0
        g=ma_position.distance(state.player(id_team,po).position)
        pp=1
        i=config1.position.distance(state.player(id_team,pp).position)
        if g<i:
            j=state.player(id_team,po)
        else:
            j=state.player(id_team,pp)
        return j

    def next_position_ball(self,ball):
        try:
            ball=Ball(ball.position,ball.vitesse)
            ball.next(V2D())
        except:
            ball=Ball(ball.ball.position,ball.ball.vitesse)
            ball.next(V2D())
        return ball

    def projector_ball_x(self,ball,position_x):
        if ball.vitesse.x != 0:
            lamda=(position_x-ball.position.x)/ball.vitesse.x
            return ball.vitesse.y*lamda + ball.position.y
        else:
            return ball.position.y

    def mirror(self,position,id_team):
        if id_team==2:
            return V2D(GAME_WIDTH-position.x,GAME_HEIGHT-position.y)
        return position

    def Min(self,n,min):
        return n<=min

    def Max(self,n,max):
        return n>=max

    def In(self,b,min,max):
        return self.Min(b,max) and self.Max(b,min)

    def In_m(self,position,but,marge):
        return self.In(position, but-marge,but+marge)

class Bibli_Player:
        def __init__(self,state,bibli):
            self.state=state
            self.bibli=bibli
            self.autre_player=self.autre
        
        def nb_p(self):
            return len([x for x in self._configs.keys()])
        
        @property
        def autre(self):
            return self.near_of_me()
        @property
        def autre_position(self):
            return self.autre.position
        @property
        def autre_vitesse(self):
            return self.autre.vitesse
        
        def have_ball(self):
            return self.has_ball(self.ball,self.ma_position)
        
        def dvt_lui(self,him):
            me=self.ma_position
            if self.id_team==1:
                return me.x >him.x
            else:
                return me.x <him.x

        def has_ball_dvt(self):
            him=self.near_of_me()
            return self.have_ball() and not self.dvt_lui(him.position)


        def has_ball_dvt2(self):
            him=self.near_of_me()
            return self.dvt_lui(him.position)

        def autre_ball(self):
            nb=self.nb_p()/2
            print("an",nb)
            for i in range (0,nb):
                print("i",i,"hs",self.has_ball(self.ball,self.state.player(self._autre,i).position))
                if self.has_ball(self.ball,self.state.player(self._autre,i).position):
                    return 1
            return 0
        def near_of_me(self):
            config1,id_team,state = self.moi,self._autre,self.bibli
            if self.nb_p()==2:
                return state.player(id_team,0)
            po=0
            g=self.ma_position.distance(state.player(id_team,po).position)
            pp=1
            i=self.ma_position.distance(state.player(id_team,pp).position)
            if g<i:
                j=state.player(id_team,po)
            else:
                j=state.player(id_team,pp)
            return j

        def player_in_but(self,but,marge_x,marge_y):
            but=GOAL1
            return self.In_m(self.ma_position_m.x,but.x,marge_x) and self.In_m(self.ma_position.y,but.y,marge_y)
    
        def __getattr__(self,name):
            return self.bibli.get_attr(self.bibli,self.state,name)


class all(AS):
        def __init__(self,num=0):
            self.clever=clever()
            self.clever.master=num
            self.num=num
            self.name="ALL"
        
        
            
        def compute_strategy(self,state1,id_team,id_player):
            self.state1=AllState(state1,id_team,id_player)
            self.state=Bibli(self.state1,self.clever)
            nb_pers=self.state.nb_p()
            if nb_pers==2:
                if self.num==0:
                    return ia().compute_strategy(self.state,self.id_team,self.id_player)
                else:
                    return illumination_one_to_one(self.clever.master).compute_strategy(self.state)
            elif nb_pers==4:
                return illumination_two_to_two(self.clever.master).compute_strategy(self.state)


        def begin_round(self, team1, team2, state):
            return self.clever.begin_round()
        
        
        def end_round(self, team1, team2, state):
            return self.clever.end_round(state,self.state)


        def __getattr__(self,name):
            return getattr(self.state,name)

class all2(AS):
    def __init__(self,num=0):
        self.clever=clever()
        self.clever.master=num
        self.num=num
        self.name="ALL"

    def compute_strategy(self,state1,id_team,id_player):
        self.state1=AllState(state1,id_team,id_player)
        self.state=Bibli(self.state1,self.clever)
        nb_pers=self.state.nb_p()
        if nb_pers==2:
            if self.num==0:
                return ia().compute_strategy(self.state,self.id_team,self.id_player)
            else:
                return illumination_one_to_one(self.clever.master).compute_strategy(self.state)
        elif nb_pers==4:
            return illumination_two_to_two(self.clever.master).compute_strategy(self.state)


    def begin_round(self, team1, team2, state):
        return self.clever.begin_round()
    
    
    def __getattr__(self,name):
        return getattr(self.state,name)
class illumination_one_to_one(AS):
    def __init__(self,id=0):
        AS.__init__(self,"illumination")
        self.id=id
    
    def compute_strategy(self,state):
        self.state=state
        if self.state.clever.one_to_one_goal_attack:
			return attack_one_to_one(state).compute_strategy()
        if self.id==1:
			return forceur(state).compute_strategy()
        elif self.id==2:
			return goal_one_to_one(Bibli_Goal(state)).compute_strategy()
        elif self.id==3:
			return attack_one_to_one(state).compute_strategy()
                
    def __getattr__(self,name):
        return getattr(self.state,name)

class illumination_two_to_two(AS):
    def __init__(self,id=0):
        AS.__init__(self,"illumijnation")
        self.id=id
        
    def compute_strategy(self,state):
        self.state=state
        if self.state.clever.two_to_two_goal_attack:
            return attack_one_to_one(state).compute_strategy()
        if self.id==1:
            return forceur(state).compute_strategy()
        elif self.id==2:
            return goal_two_to_two(Bibli_Goal(state)).compute_strategy()
        elif self.id==3:
            return attack_one_to_one(state).compute_strategy()

class Bibli_Goal:
    def __init__(self,state):
        self.bibli=self.state=state
    
    def revien_goal(self):
        s=self.state
        return SA(s.goal - s.ma_position,V2D())
    
    def check_no_goal(self):
        return self.ball.position.distance(self.ma_position) < self.ball.position.distance(self.autre.position) or self.ball.position.distance(self.ma_position) < 10
    def check_goal(self):
        
        return (self.check_goal_m(0) and not self.ball_in_zone(10))
    
    def check_goal_m(self,m=0):
        s=self.state
        b=self.bibli
        return b.player_in_but(s.mes_goal,ZONE_GOAL + m,MODULO_GOAL)
                                     
    def check_ball(self):
        return self.has_ball_dvt()
    
    def projector_ball_goal(self):
        ball=self.ball
        return self.projector_ball_x(ball,self.ma_position.x)
                                     
    def projector_ball_goal_x(self,ball):
        return self.projector_ball_x(ball,self.ma_position.x)

    def check_goal_dvt(self):
        angle=self.moi.position.angle
        if self.check_goal():
            if self.id_team==1:
                return angle != ANGLE1
            else:
                return angle != ANGLE2
        else:
            return False

    def alert(self):
        yy=self.projector_ball_goal()

        if self.In(yy,40,50):
            return SA(V2D(0,yy-self.moi.position.y),V2D(0,0))
        else:
            return SA()

    def check_shoot(self):
        return self.have_ball()
                                     
    def dvt(self):
        if self.id_team==1:
            return SA(V2D(angle=ANGLE1,norm=NORM_DVT),V2D(4,4))
        else:
            return SA(V2D(angle=ANGLE2,norm=NORM_DVT),V2D(4,4))

    def __getattr__(self,name):
        return self.bibli.get_attr(self.bibli,self.state,name)

class Bibli_Ball:
    def __init__(self,state,d):
        self.state=state
        self.d=d
    
    
    def next_position_ball_state(self):
        return self.next_position_ball(self.state)
                                     
    def ball_in_zone(self,zone):
        return self.ball.position.distance(self.mes_goal) <= zone

    def __getattr__(self,name):
        return  self.d.get_attr(self.state,self.d,name)

class Bibli:
    def __init__(self,state,clever=0):
        self.state=state
        self.clever=clever
        self.bibli=Bibli_Player(state,Bibli_Ball(state,usefull()))
    def to_change(self,num):
        return all(num).compute_strategy(self.state._state,self.id_team,self.id_player)
        
    def __getattr__(self,name):
        return self.bibli.get_attr(self.bibli,self.state,name)

class goal_one_to_one(AS):
    def __init__(self,state):
        AS.__init__(self,"goal_one_to_one")
        self.state=state
    
    # A REVOIR
    def check_attack(self):
        yh=self.ball_in_zone(GOAL_ATTACK)
        return ((abs(self.ball.vitesse.x) <= BALLE_MIN_VITESSE and abs(self.ball.vitesse.y) <= BALLE_MIN_VITESSE and yh and self.ma_position.y >= self.goal.y - 2 -GOAL_ATTACK and self.ball.position.y <= self.goal.y + 2 + GOAL_ATTACK and self.ball.vitesse.norm <=BALLE_MAX_NORM )or( yh and self.ball.position.y >= self.goal.y - 2 -GOAL_ATTACK and self.ball.position.y <= self.goal.y + 2 + GOAL_ATTACK))
    #A REVOIR
    def attack(self):
        yy=self.projector_ball_goal()
        if self.config.position.y >=yy+1 or self.config.position.y <=yy-1:
            return SA(V2D(0,yy -self.config.position.y),V2D())
        return SA(self.ball.position-self.config.position,V2D())

    
    def shoot(self):
        yy=(GAME_HEIGHT-self.autre_player.position.y )*1.5
        while self.Min(abs(yy-self.autre_player.position.y),5):
            yy=yy*1.5
        y=V2D(75 ,yy)-self.state.ball.position
        return SA(V2D(),y)

    def check_stop_alert(self):
            ty=self.projector_ball_goal()
            return (ty <= self.goal.y-7 or self.goal.y + 7 <=ty )and not self.check_goal_m(15)

    def stop_alert(self):
            self.clever.one_to_one_goal_auto1=1
            return self.revien_goal

    def check_alert(self):
        yh=self.ball_in_zone(GOAL_ALERT)
        return yh and not self.check_ball() and abs(self.state.ball.vitesse.x) >=0

    def check_angle(self):
        return self.config.position.y -self.autre_player.position.y >= 10

    def compute_strategy(self):
        print("goal oooooooooooooooooooooooooooooooooooooooooo",self.id_team,self.id_player)
        if self.check_goal_dvt():
            print("dvt")
            self.clever.one_to_one_goal_auto1=0
            return self.dvt()
        if not self.check_goal() and self.clever.one_to_one_goal_auto1:
            print("goal")
            return self.revien_goal()
        if self.check_shoot():
            print("shoot")
            self.clever.one_to_one_goal_auto1=1
            self.clever.one_to_one_goal_attack=1
            return self.to_change(TO_ATTACK)
        if self.check_attack():
            print("attackg")
            return self.attack()
        if self.check_stop_alert():
            print("stop alert")
            return self.stop_alert()
        if self.check_alert():
            print("alert")
            return self.alert()
        return SA()

    def __getattr__(self,name):
        return getattr(self.state,name)

class goal_two_to_two(AS):
    def __init__(self,state):
        AS.__init__(self,"goal_one_to_one")
        self.state=state
                                     
    def attack(self):
        yi=usefull().simulate(self.moi,self.state)
        print("karim",yi)
        return SA((yi.position-self.config.position).norm_max(1),V2D())

    def check_attack(self):
        yh=self.ball_in_zone(GOAL_ATTACK)
        yp=self.near_of_me()
        jd=self.next_position_ball_state()
        return self.config.position.distance(self.state.ball.position)<self.autre_player.position.distance(self.state.ball.position)  or jd.position.distance(self.ma_position) < jd.position.distance(yp.position)
                                
    def shoot(self):
        yp=self.near_of_me()
        yy=(GAME_HEIGHT-yp.position.y )
        print(yy)
        if yp.position.y >= GAME_HEIGHT/2:
            fk=-1
        else:
            fk=1
        while abs(yy-yp.position.y) <=6:
            yy=yy*1.5*fk
        y=V2D(75 ,yy)-self.state.ball.position
        return SA(V2D(),y)
                                     
    def bb(self):
        return not self.check_goal_m(20) and self.config.vitesse.norm < 0.2 and (self.state.ball.position.distance(self.ma_position) > self.state.ball.position.distance(self.autre_position))
                                     
    def check_stop_alert(self):
        ty=self.projector_ball_goal
        return (ty <= self.goal.y-7 or self.goal.y + 7 <=ty )and not self.check_goal_m(15)
                                     
    def stop_alert(self):
        self.clever.one_to_one_goal_auto1=1
        return self.revien_goal()
                                     
    def check_alert(self):
        if self.id_team==1:
            yh=self.state.ball.position.x <= GOAL_ALERT
            d=self.state.ball.vitesse.x<=0
        else:
            yh=self.state.ball.position.x >= GAME_WIDTH-GOAL_ALERT
            d=self.state.ball.vitesse.x>=0
        return yh and not self.check_ball() and abs(self.state.ball.vitesse.x) >=0 and d
                                     
    def check_angle(self):
        return self.config.position.y -self.autre_player.position.y >= 10
                                     
    def compute_strategy(self):
        print("goal toooooooooooooooooooooooooooooooooooooooooo",self.id_team,self.id_player)
        if self.check_no_goal():
            self.clever.one_to_one_goal_auto1=0
        if self.check_goal_dvt():
            print("dvt")
            self.clever.one_to_one_goal_auto1=0
            return self.dvt()
        if (not self.check_goal() and self.clever.one_to_one_goal_auto1) or self.bb():
            print("goal")
	    self.clever.one_to_one_goal_auto1=1
            return self.revien_goal()
        if self.check_shoot():
            print("shoot")
            self.clever.one_to_one_goal_auto1=1
            self.clever.two_to_two_goal_attack=1
            return self.to_change(TO_ATTACK)
        if self.check_attack():
            print("attackg")
            return self.attack()
        if self.check_stop_alert():
            print("stop alert")
            return self.stop_alert()
        if self.check_alert():
            print("alert")
            return self.alert()
        return SA()
    def __getattr__(self,name):
        return getattr(self.state,name)

class attack_two_to_two(AS):
    def __init__(self,state):
        AS.__init__(self,"goal_one_to_one")
        self.state=state
                                     
    def compute_strategy(self):
        print("attack t oooooooooooooooooooooooo",self.id_team,self.id_player)

        if (self.state.ball.position.distance(self.config.position) <= (PLAYER_RADIUS + BALL_RADIUS) ) :
            if abs(self.goal2.x - (self.config.position.x)) <=40:
                y=(self.goal2+ V2D(0,-3)-self.state.ball.position).norm_max(3)
                return SA(V2D(),y)
            else:
                dis = self.ball.position - self.autre_player.position
                self.yp=self.autre_player
                moi = self.config.position
                s = usefull().next_position_player(dis, self.autre_player)
                jj=usefull().has_ball_merge(self.state,s,10)
                if jj:
                    if abs(self.goal2.x- (self.config.position.x)) <=40:
                        y=self.goal2 + V2D(0,3)-self.state.ball.position
                        return SA(V2D(0,0),y)
                    else:
                        yy=GAME_HEIGHT-self.yp.position.y 
                        while abs(yy-self.yp.position.y) <=15:
                            yy=yy*1.5
                        y=V2D(self.ball.position.x+70*self.sens ,yy)-self.state.ball.position
                        y=(y).norm_max(2)
                        return SA(V2D(0,0),y)
                else:
                    return SA(V2D(0,0),(self.goal2-self.state.ball.position).norm_max(0.4))

        else:
            ballpro=self.next_position_ball_state()
            return SA(ballpro.position-self.config.position,V2D(0,0))
   
    def __getattr__(self,name):
        return getattr(self.state,name)

                                     
class attack_one_to_one(AS):
    def __init__(self,state):
        self.state=state
    
    def trouve(self):
        a=self.autre_position.y
    
    def attack_o(self):
        print("attack oooooooooooooooooooooooo",self.id_team,self.id_player)
        if (self.state.ball.position.distance(self.config.position) <= (PLAYER_RADIUS + BALL_RADIUS) ) :
            print("A LA BALLE")
            e=self.has_ball_dvt2()
            print("DERIERE")
            dis = self.ball.position - self.autre_player.position
            moi = self.config.position
            s = usefull().next_position_player(dis, self.autre_player)
            if e:
                print("e")
                if abs(self.goal2.x- (self.config.position.x)) <=35:
                    print("25")
#                    self.trouve()
                    y=self.goal2 + V2D(0,-3)-self.state.ball.position
                    return SA(V2D(0,0),y)
                else:
                    print("-25")
                    y=self.goal2-self.state.ball.position +V2D(uniform(-100,100),uniform(-14,14))
                    return SA(V2D(0,0),(y).norm_max(1.5))
            else:
                print("not e")
                jj=usefull().has_ball_merge(self.state,s,15)
                if jj:
                    print("jj",jj)
                    if abs(self.goal2.x- (self.config.position.x)) <=35:
                        print("25")
                        y=self.goal2 + V2D(0,3)-self.state.ball.position
                        return SA(V2D(0,0),y)
                    else:
                        print("-25")
                        yy=GAME_HEIGHT-self.autre.position.y
                        while abs(yy-self.autre.position.y) <=25:
                            yy=yy*1.13
                        y=V2D(self.ball.position.x+40*self.sens ,yy*self.sens)-self.state.ball.position
                        y=(y).norm_max(2)
                        return SA(V2D(0,0),y)
                else:
                    print("not jj")
                    return SA(V2D(0,0),(self.goal2-self.state.ball.position).norm_max(0.6))
        
        else:
            print("not ball")
            return SA(self.state.ball.position-self.config.position,V2D(0,0))

    def compute_strategy(self):
        print(self.clever.two_to_two_goal_attack_master)
        if self.clever.two_to_two_goal_attack==1 and self.autre_ball():
            print("autre basse")
            self.clever.two_to_two_goal_attack=0
            return self.to_change(TO_GOAL)
        
        return self.attack_o()
                                     
    def __getattr__(self,name):
       return getattr(self.state,name)

                                     
        
class ia(AS):
    def __init__(self):
        AS.__init__(self,"ia") 
        
    def compute_strategy(self,state,id_team,id_player):
        return

class forceur(AS):
    def __init__(self,state):
        AS.__init__(self,"forceur_one_to_one")
        self.state=state
        
    def compute_strategy(self):
        print("forceur oooooooooooooooooooooooooooooooooooooooooo",self.id_team,self.id_player)
        id_team=self.id_team
        id_player=self.id_player
        state=self.state
        vod=0
        if id_team==1:
            vod=T1_SENS*COEFF_FORCEUR
            vo=T1_BUT
        elif id_team==2:
            vod=T2_SENS*COEFF_FORCEUR
            vo=T2_BUT
        position=self.ma_position
        ball_to_player=self.state.ball.position.distance(self.state.player(self.id_team,self.id_player).position)
        goal_to_player=self.state.player(self.id_team,self.id_player).position.distance(V2D(vo,GAME_HEIGHT/2))
        goal_to_ball= self.goal2-self.ma_position
        ball= PLAYER_RADIUS + BALL_RADIUS
        if self.have_ball():
            return SA(V2D(0,0),goal_to_ball+V2D(uniform(-100,100),uniform(-100,100)).norm_max(uniform(4,40)))
        else:
            return SA(self.ball.position - self.ma_position)

    def __getattr__(self,name):
        return getattr(self.state,name)

