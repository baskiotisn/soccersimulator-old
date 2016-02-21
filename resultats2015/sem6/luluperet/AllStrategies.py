import soccersimulator, soccersimulator.settings,math
from soccersimulator.settings import *
from soccersimulator import SoccerTeam as STe,SoccerMatch as SM, Player, SoccerTournament as ST, BaseStrategy as AS, SoccerAction as SA, Vector2D as V2D,SoccerState as SS, MobileMixin


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
GOAL_ATTACK=40
GOAL_ALERT=50
INCER=10
BALLE_MIN_VITESSE=0.5
BALLE_MAX_NORM=1
NORM_DVT=0.5
MODULO_GOAL=2
GOAL_ATTACK2=20
GAMMA=1.5

class clever(object):
        def __init__(self):
                self.auto1_attack=1
                self.auto1_goal=1
                self.auto_goal_inside=1
                self.auto1_round=0
                self.onetoone_begin_round=1
                self.auto1_all=1
                self.one_to_one_goal_auto1=1
                self.one_to_one_goal_attack=0
                self.one_to_one_goal_max=0
        def ajoute(self,nom,val):
                self.nom=val
        def begin_round(self):
                self.onetoone_begin_round=1
                self.one_to_one_goal_auto1=1
                self.one_to_one_goal_max=0
                self.one_to_one_goal_attack=0   
class Ball(MobileMixin):
    def __init__(self,*args,**kwargs):
        MobileMixin.__init__(self,*args,**kwargs)

    def next(self,sum_of_shoots):
        self.vitesse.norm = self.vitesse.norm - settings.ballBrakeSquare * self.vitesse.norm ** 2 - settings.ballBrakeConstant * self.vitesse.norm
        ## decomposition selon le vecteur unitaire de ball.speed
        snorm = sum_of_shoots.norm
        if snorm > 0:
            u_s = sum_of_shoots.copy()
            u_s.normalize()
            u_t = Vector2D(-u_s.y, u_s.x)
            speed_abs = abs(self.vitesse.dot(u_s))
            speed_ortho = self.vitesse.dot(u_t)
            speed = Vector2D(speed_abs * u_s.x - speed_ortho * u_s.y, speed_abs * u_s.y + speed_ortho * u_s.x)
            speed += sum_of_shoots
            self.vitesse = speed
        self.vitesse = self.vitesse.norm_max(settings.maxBallAcceleration)
        self.position += self.vitesse
    @property
    def position(self):
        return self.position
    @property
    def vitesse(self):
        return self.vitesse
        
class usefull(object): 
        def __init__(self):
            self.name="czc" 
            
        def nb_p(self,state): 
            return len([x for x in state._configs.keys()])
             
        def next_position_player(self,dis,config): 
            config_state_vitesse = config._state.vitesse * (1 - settings.playerBrackConstant) #frottemnt 
            config_state_vitesse = (config_state_vitesse+dis.norm_max(settings.maxPlayerAcceleration)).norm_max(settings.maxPlayerSpeed)
            config_state_position = config._state.position+ config_state_vitesse.norm_max(settings.maxPlayerSpeed) 
            #if self._state.position.x < 0 or self.position.x > settings.GAME_WIDTH or self.position.y < 0 or self.position.y > settings.GAME_HEIGHT: 
                #self._state.position.x = max(0, min(settings.GAME_WIDTH, self.position.x)) 
                #self._state.position.y = max(0, min(settings.GAME_HEIGHT, self.position.y)) 
                #self._state.vitesse.norm = 0 
            return config_state_position
        def next_position_ball(self,state):
                angle_factor = 1. - abs(math.cos((self.vitesse.angle - self.shoot.angle) / 2.))
                dist_factor = 1. - self._state.position.distance(ball.position) / (settings.PLAYER_RADIUS + settings.BALL_RADIUS)
                shoot = self.shoot * (1 - angle_factor * 0.25 - dist_factor * 0.25)
                shoot.angle = shoot.angle + (2 * random.random() - 1.) * (angle_factor + dist_factor) / 2. * settings.shootRandomAngle * math.pi / 2.
                self._action = SoccerAction()
                return shoot
        def babal(self,ball):
                br=Ball(ball)
                br.next(V2D())
                return br
        def test_after(self,ball,v2):
            ball2=ball
            d=ball2.vitesse

            while d.x >0.1:
                d.norm =d.norm - settings.ballBrakeSquare * d.norm ** 2 - settings.ballBrakeConstant * d.norm
                d =d.norm_max(settings.maxBallAcceleration)
                ball2.position += d
                print("ueruyzzutuztutztzuuttuzr",d,"d",ball2,"v2",v2)
            return ball2.position.x >= v2
        def has_ball(self,state,position): 
            return state.ball.position.distance(position) <=PLAYER_RADIUS + BALL_RADIUS
        def has_ball_merge(self,state,position,m): 
            return state.ball.position.distance(position) <=PLAYER_RADIUS + BALL_RADIUS +m
        def has_ball_next(self,state,id_team,id_player): 
            dis=state.ball.position - state.player_state(id_team, id_player).position 
            config=state.player(id_team,id_player) 
            f=self.next_position_player(dis,config) 
            return self.has_ball(state,f)
            
        def dvt (self,me,him,team):

            if team==1:
                return me.x-him.x >0 
            else: 
                return me.x <him.x

        def near_of_me(self,config1,id_team,state):
            po=0

            g=config1.position.distance(state.player(id_team,po).position)

            pp=1
            i=config1.position.distance(state.player(id_team,pp).position)


            if g<i:
                j=state.player(id_team,po)
            else:
                j=state.player(id_team,pp)
            print("near of me",po,j)
            return j

        def has_ball_dvt(self,state,dis,him,team): 
            return self.has_ball(state,dis) and not self.dvt(dis,him,team)
        
        def has_ball_dvt2(self,dis,him,team):
            return self.dvt(dis,him,team)

class all(AS):
        def __init__(self,num=0):
            self.clever=clever()
            self.num=num
            self.name="ALL"
        
        
            
        def compute_strategy(self,state,id_team,id_player):
            nb_pers=usefull().nb_p(state)
            if nb_pers==2:
                if self.num==0:
                    return ia().compute_strategy(state,id_team,id_player)
                else:
                    return illumination_one_to_one(self.num).compute_strategy(state,id_team,id_player,self.clever)
            elif nb_pers==4:
                return illumination_two_to_two(self.num).compute_strategy(state,id_team,id_player,self.clever)


        def begin_round(self, team1, team2, state):
            self.clever.begin_round()
            pass
			
class illumination_one_to_one(AS):
	def __init__(self,id=0):
		AS.__init__(self,"illumination") 
		self.id=id
		
	def compute_strategy(self,state,id_team,id_player,clever):
		if clever.one_to_one_goal_attack:
			return attack_one_to_one(id_team,id_player,state,clever).compute_strategy()
		if self.id==1:
			return forceur_one_to_one().compute_strategy(state,id_team,id_player,clever)
		elif self.id==2:
			return goal_one_to_one(id_team,id_player,state,clever).compute_strategy()
		elif self.id==3:
			return attack_one_to_one(id_team,id_player,state,clever).compute_strategy()

class illumination_two_to_two(AS):
    def __init__(self,id=0):
        AS.__init__(self,"illumijnation")
        self.id=id
        
    def compute_strategy(self,state,id_team,id_player,clever):

        if self.id==1:
            return forceur_two_to_two().compute_strategy(state,id_team,id_player,clever)
        elif self.id==2:
            return goal_two_to_two(id_team,id_player,state,clever).compute_strategy()
        elif self.id==3:
            return attack_two_to_two(id_team,id_player,state,clever).compute_strategy()


class goal_one_to_one(AS):
    def __init__(self,id_team,id_player,state,clever):
        AS.__init__(self,"goal_one_to_one")
        self.va_au_goal=1
        self.id_team=id_team
        self.id_player=id_player
        self.player=0
        if id_team==1:
            self.goal=GOAL1
            self.sens=T2_SENS
            self.autre=2
        elif id_team==2:
            self.goal=GOAL2
            self.sens=T2_SENS
            self.autre=1
        self.clever=clever
        self.config=state.player(id_team,id_player)
        self.state=state
        self.ball=state.ball.position
        self.goal_zone=self.goal + V2D(ZONE_GOAL*self.sens,0)
        self.autre_player=state.player(self.autre,self.player)
    def revien_goal(self):
        return SA(self.goal - self.config.position,V2D())
    def check_goal(self,marge=0):
        if self.id_team==1:
            return self.config.position.y >=self.goal.y-MODULO_GOAL and  self.config.position.y<=self.goal.y+MODULO_GOAL and self.config.position.x<= ZONE_GOAL + marge
        else:
            return self.config.position.y >=self.goal.y-MODULO_GOAL and  self.config.position.y<=self.goal.y+MODULO_GOAL and self.config.position.x>= GAME_WIDTH-ZONE_GOAL - marge
    def check_goal_dvt(self):
        angle=self.config.position.angle
        if self.check_goal(0):
            if self.id_team==1:
                return angle != ANGLE1
            else:
                return angle != ANGLE2 
    def dvt(self):
        if self.id_team==1:
            return SA(V2D(angle=ANGLE1,norm=NORM_DVT),V2D(4,4))
        else:
            return SA(V2D(angle=ANGLE2,norm=NORM_DVT),V2D(4,4))
    def attack(self):
        yy=self.projector2(self.state.ball)
        if self.config.position.y >=yy+1 or self.config.position.y <=yy-1:
            return SA(V2D(0,yy -self.config.position.y),V2D())
        return SA(self.ball-self.config.position,V2D())
        
    def check_attack(self):
        print("vitesse",self.state.ball.vitesse,"ball x",self.ball.x)
        print("ca")
        if self.id_team==1:
            yh= self.ball.x <=GOAL_ATTACK
        else:
            yh=self.ball.x >=GAME_WIDTH-GOAL_ATTACK
        return (abs(self.state.ball.vitesse.x) <= BALLE_MIN_VITESSE and abs(self.state.ball.vitesse.y) <= BALLE_MIN_VITESSE and yh and self.ball.y >= self.goal.y - 2 -GOAL_ATTACK and self.ball.y <= self.goal.y + 2 + GOAL_ATTACK and self.state.ball.vitesse.norm <=BALLE_MAX_NORM )or( yh and self.ball.y >= self.goal.y - 2 -GOAL_ATTACK and self.ball.y <= self.goal.y + 2 + GOAL_ATTACK)
    def projector(self,ball):	
        print("ball x",ball.position.x," posirion x",self.config.position.x)
        while (ball.position.x <= self.config.position.x) and ball.vitesse != V2D(0,0):
            if ball.vitesse == V2D(0,0):
                break
            ball.vitesse.norm = ball.vitesse.norm - settings.ballBrakeSquare * ball.vitesse.norm ** 2 - settings.ballBrakeConstant * ball.vitesse.norm
            ## decomposition selon le vecteur unitaire de ball.speed
            ball.vitesse = ball.vitesse.norm_max(settings.maxBallAcceleration)
            ball.position += ball.vitesse
            print("bp ", ball.vitesse )
        return ball.position.y
    def projector2(self,ball):
        if ball.vitesse.x != 0:
            lamda=(self.config.position.x-ball.position.x)/ball.vitesse.x
            return ball.vitesse.y*lamda + ball.position.y
        else:
            return ball.position.y
    def check_ball(self):
        return usefull().has_ball_dvt(self.state,self.config.position,self.autre_player.position,self.id_team)
    def alert(self):
	#fd=self.state.ball
        yy=self.projector2(self.state.ball)
        if yy>=35 and yy<=55:
            return SA(V2D(0,yy-self.config.position.y),V2D(0,0))
        else:
            return SA()
    def check_shoot(self):
        #print("lko")
        return usefull().has_ball(self.state,self.config.position)
    def shooti(self):
        if self.check_shoot():
            #print("dfez")
            return self.shoot()
    def goali(self):
        if not self.check_goal():
            return self.reviens_au_goal()
    def shoot(self):
        #print("prince")
#        print(self.autre_player.position.angle,self.autre_player.position.angle-math.pi/2)
        yy=(GAME_HEIGHT-self.autre_player.position.y )*1.5
        while abs(yy-self.autre_player.position.y) <=5:
            yy=yy*1.5
        
        y=V2D(75 ,yy)-self.state.ball.position
        return SA(V2D(),y)
    def check_stop_alert(self):
            ty=self.projector2(self.state.ball)
            print("ty, ",ty)
            return (ty <= self.goal.y-7 or self.goal.y + 7 <=ty )and not self.check_goal(15)
    def stop_alert(self):
            self.clever.one_to_one_goal_auto1=1
            return self.revien_goal()
    def check_alert(self):
        if self.id_team==1:
            yh=self.ball.x <= GOAL_ALERT
        else:
            yh=self.ball.x >= GAME_WIDTH-GOAL_ALERT
        return yh and not self.check_ball() and abs(self.state.ball.vitesse.x) >=0
    def check_angle(self):
        return self.config.position.y -self.autre_player.position.y >= 10
    def compute_strategy(self):
	# if usefull().has_ball(self.state,self.autre_player.position) and self.clever.one_to_one_goal_max:
	#	self.clever.one_to_one_goal_max=0
	#if self.clever.one_to_one_goal_attack and self.check_angle() and self.check_ball() or self.clever.one_to_one_goal_max :
	#	print("ANGLE")
	#	self.clever.one_to_one_goal_max=1
	#	return forceur_one_to_one().compute_strategy(self.state,self.id_team,self.id_player,self.clever)
        print("oooooooooooooooooooooooooooooooooooooooooo",self.id_team,self.id_player)
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
            self.clever.one_to_one_goal_attack=0
	    self.clever.one_to_one_goal_attack=1
            return attack_one_to_one(self.id_team,self.id_player,self.state,self.clever).compute_strategy()
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

class goal_two_to_two(AS):
    def __init__(self,id_team,id_player,state,clever):
        AS.__init__(self,"goal_one_to_one")
        self.va_au_goal=1
        self.id_team=id_team
        self.id_player=id_player
        self.player=0
        if id_team==1:
            self.goal=GOAL1
            self.sens=T2_SENS
            self.autre=2
        elif id_team==2:
            self.goal=GOAL2
            self.sens=T2_SENS
            self.autre=1
        self.clever=clever
        self.config=state.player(id_team,id_player)
        self.state=state
        self.ball=state.ball.position
        self.goal_zone=self.goal + V2D(ZONE_GOAL*self.sens,0)
        self.autre_player=state.player(self.autre,self.player)
    def revien_goal(self):
        return SA(self.goal - self.config.position,V2D())
    def check_goal(self,marge=0):
        if self.id_team==1:
            return self.config.position.y >=self.goal.y-MODULO_GOAL and  self.config.position.y<=self.goal.y+MODULO_GOAL and self.config.position.x<= ZONE_GOAL + marge
        else:
            return self.config.position.y >=self.goal.y-MODULO_GOAL and  self.config.position.y<=self.goal.y+MODULO_GOAL and self.config.position.x>= GAME_WIDTH-ZONE_GOAL - marge
    def check_goal_dvt(self):
        angle=self.config.position.angle
        if self.check_goal(0):
            if self.id_team==1:
                return angle != ANGLE1
            else:
                return angle != ANGLE2
    def dvt(self):
        if self.id_team==1:
            return SA(V2D(angle=ANGLE1,norm=NORM_DVT),V2D(4,4))
        else:
            return SA(V2D(angle=ANGLE2,norm=NORM_DVT),V2D(4,4))
    def attack(self):
        yy=self.projector2(self.state.ball)
        if (self.config.position.y >=yy+1 or self.config.position.y <=yy-1) and self.state.ball.vitesse.norm>0.2:
            return SA(V2D(0,yy -self.config.position.y),V2D())
        return SA(self.ball-self.config.position,V2D())

    def check_attack(self):
        print("vitesse",self.state.ball.vitesse,"ball x",self.ball.x)
        print("ca")
        if self.id_team==1:
            yh= self.ball.x <=GOAL_ATTACK
        else:
            yh=self.ball.x >=GAME_WIDTH-GOAL_ATTACK
        return (abs(self.state.ball.vitesse.x) <= BALLE_MIN_VITESSE and abs(self.state.ball.vitesse.y) <= BALLE_MIN_VITESSE and yh and self.ball.y >= self.goal.y - 2 -GOAL_ATTACK and self.ball.y <= self.goal.y + 2 + GOAL_ATTACK and self.state.ball.vitesse.norm <=BALLE_MAX_NORM )or( yh and self.ball.y >= self.goal.y - 2 -GOAL_ATTACK and self.ball.y <= self.goal.y + 2 + GOAL_ATTACK)
    def projector(self,ball):
        print("ball x",ball.position.x," posirion x",self.config.position.x)
        while (ball.position.x <= self.config.position.x) and ball.vitesse != V2D(0,0):
            if ball.vitesse == V2D(0,0):
                break
            ball.vitesse.norm = ball.vitesse.norm - settings.ballBrakeSquare * ball.vitesse.norm ** 2 - settings.ballBrakeConstant * ball.vitesse.norm
            ## decomposition selon le vecteur unitaire de ball.speed
            ball.vitesse = ball.vitesse.norm_max(settings.maxBallAcceleration)
            ball.position += ball.vitesse
            print("bp ", ball.vitesse )
        return ball.position.y
    def projector2(self,ball):
        if ball.vitesse.x != 0:
            lamda=(self.config.position.x-ball.position.x)/ball.vitesse.x
            return ball.vitesse.y*lamda + ball.position.y
        else:
            return ball.position.y
    def check_ball(self):
        return usefull().has_ball_dvt(self.state,self.config.position,self.autre_player.position,self.id_team)
    def alert(self):
        #fd=self.state.ball
        yy=self.projector2(self.state.ball)
        if yy>=35 and yy<=55:
            return SA(V2D(0,yy-self.config.position.y),V2D(0,0))
        else:
            return SA()
    def check_shoot(self):
        #print("lko")
        return usefull().has_ball(self.state,self.config.position)
    def shooti(self):
        if self.check_shoot():
            #print("dfez")
            return self.shoot()
    def goali(self):
        if not self.check_goal():
            return self.reviens_au_goal()
    def shoot(self):
        #print("prince")
        #        print(self.autre_player.position.angle,self.autre_player.position.angle-math.pi/2)
        yp=usefull().near_of_me(self.config,self.autre,self.state)
        print("yppppppppppppppppp",yp)
        yy=(GAME_HEIGHT-yp.position.y )
        print(yy)
        if yp.position.y >= GAME_HEIGHT/2:
            fk=-1
        else:
            fk=1
        while abs(yy-yp.position.y) <=6:
            yy=yy*1.5*fk

        print("rzrz",yy,self.state.ball.position)
        y=V2D(75 ,yy)-self.state.ball.position
        return SA(V2D(),y)
    def check_stop_alert(self):
        ty=self.projector2(self.state.ball)
        print("ty, ",ty)
        return (ty <= self.goal.y-7 or self.goal.y + 7 <=ty )and not self.check_goal(15)
    def stop_alert(self):
        self.clever.one_to_one_goal_auto1=1
        return self.revien_goal()
    def check_alert(self):
        if self.id_team==1:
            yh=self.ball.x <= GOAL_ALERT
        else:
            yh=self.ball.x >= GAME_WIDTH-GOAL_ALERT
        return yh and not self.check_ball() and abs(self.state.ball.vitesse.x) >=0
    def check_angle(self):
        return self.config.position.y -self.autre_player.position.y >= 10
    def compute_strategy(self):
        # if usefull().has_ball(self.state,self.autre_player.position) and self.clever.one_to_one_goal_max:
        #	self.clever.one_to_one_goal_max=0
        #if self.clever.one_to_one_goal_attack and self.check_angle() and self.check_ball() or self.clever.one_to_one_goal_max :
        #	print("ANGLE")
        #	self.clever.one_to_one_goal_max=1
        #	return forceur_one_to_one().compute_strategy(self.state,self.id_team,self.id_player,self.clever)
        print("oooooooooooooooooooooooooooooooooooooooooo",self.id_team,self.id_player)
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
            self.clever.one_to_one_goal_attack=0
            return self.shoot()
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


class attack_two_to_two(AS):
    def __init__(self,id_team,id_player,state,clever):
        AS.__init__(self,"goal_one_to_one")
        self.va_au_goal=1
        self.id_team=id_team
        self.id_player=id_player
        self.player=0
        if id_team==1:
            self.goal=GOAL1
            self.goal2=GOAL2
            self.sens=T2_SENS
            self.autre=2
        elif id_team==2:
            self.goal=GOAL2
            self.goal2=GOAL1
            self.sens=T2_SENS
            self.autre=1
        self.clever=clever
        self.config=state.player(id_team,id_player)
        self.state=state
        self.ball=state.ball.position
        self.goal_zone=self.goal + V2D(ZONE_GOAL*self.sens,0)
        self.autre_player=state.player(self.autre,self.player)
    def compute_strategy(self):
        print("oco",self.id_team,self.id_player)
        if (self.state.ball.position.distance(self.config.position) <= (PLAYER_RADIUS + BALL_RADIUS) ) :
            if abs(self.goal2.x- (self.config.position.x)) <=40:
                print("abs")
                return SA(V2D(0,0),(self.goal2-self.state.ball.position).norm_max(5))
            else:
                print("abs")
                yp=usefull().near_of_me(self.config,self.autre,self.state)
                e=usefull().has_ball_dvt2(self.config.position,yp.position,self.id_team)
                print("qui",e)
                if e:
                    print(self.goal)
                    return SA(V2D(0,0),(self.goal2-self.state.ball.position).norm_max(2))
                else:
                    return SA(V2D(0,0),(self.goal2-self.state.ball.position).norm_max(0.9))

        else:
            print("IIIo")
            return SA(self.state.ball.position-self.config.position,V2D(0,0))

class attack_one_to_one(AS):
	def __init__(self,id_team,id_player,state,clever):
		AS.__init__(self,"goal_one_to_one")
		self.va_au_goal=1
		self.id_team=id_team
		self.id_player=id_player
		self.player=0
		if id_team==1:
		    self.goal=GOAL1
		    self.goal2=GOAL2
		    self.sens=T2_SENS
		    self.autre=2
		elif id_team==2:
		    self.goal=GOAL2
		    self.goal2=GOAL1
		    self.sens=T2_SENS
		    self.autre=1
		self.clever=clever
		self.config=state.player(id_team,id_player)
		self.state=state
		self.ball=state.ball.position
		self.goal_zone=self.goal + V2D(ZONE_GOAL*self.sens,0)
		self.autre_player=state.player(self.autre,self.player)
    	def compute_strategy(self):
		print("oooooooooooooooooooooooo",self.id_team,self.id_player)

		if (self.state.ball.position.distance(self.config.position) <= (PLAYER_RADIUS + BALL_RADIUS) ) :
			
		
			e=usefull().has_ball_dvt2(self.config.position,self.autre_player.position,self.id_team)
			print("dvt",e,"goal2",self.goal2,"40",abs(self.goal2.x- (self.config.position.x)),"last_shoot",self.config._last_shoot)
			if e:
				if abs(self.goal2.x- (self.config.position.x)) <=40:
					y=self.goal2-self.state.ball.position

				else:


					y=(self.goal2-self.state.ball.position).norm_max(3)
				print("y",y)
				return SA(V2D(),y)
			else:
			    	dis = self.ball - self.autre_player.position
				moi = self.config.position
				s = usefull().next_position_player(dis, self.autre_player)
				jj=usefull().has_ball_merge(self.state,s,10)
				print("s",s,"jj",jj)
				if jj:
					if abs(self.goal2.x- (self.config.position.x)) <=40:
						y=self.goal2 + V2D(0,5)-self.state.ball.position
						return SA(V2D(0,0),y)
					else:
						yy=GAME_HEIGHT-self.autre_player.position.y 

						while abs(yy-self.autre_player.position.y) <=5:
			    				yy=yy*1.5

						y=V2D(self.ball.x+40*self.sens ,yy)-self.state.ball.position
					y=(y).norm_max(1)
					print("df",y)
			    		return SA(V2D(0,0),y)
				else:
					print("else dvt")
					return SA(V2D(0,0),(self.goal2-self.state.ball.position).norm_max(1))

		else:

		    return SA(self.state.ball.position-self.config.position,V2D(0,0))
class ia(AS):
    def __init__(self):
        AS.__init__(self,"ia") 
        
    def compute_strategy(self,state,id_team,id_player):
        return

class forceur_one_to_one(AS):
    def __init__(self):
        AS.__init__(self,"forceur_one_to_one") 
        
    def compute_strategy(self,state,id_team,id_player,clever):
        print("oooooooooooooooooooooooooooooooooooooooooo",id_team,id_player)

        vod=0
        if id_team==1:
            vod=T1_SENS*COEFF_FORCEUR
            vo=T1_BUT
        elif id_team==2:
            vod=T2_SENS*COEFF_FORCEUR
            vo=T2_BUT
        position=state.player(id_team,id_player).position
        ball_to_player=state.ball.position.distance(state.player(id_team,id_player).position)
        goal_to_player=state.player(id_team,id_player).position.distance(V2D(vo,GAME_HEIGHT/2))
        goal_to_ball= V2D(vo,GAME_HEIGHT/2) -state.ball.position
        ball= PLAYER_RADIUS + BALL_RADIUS
        print("vhg")
        if usefull().has_ball(state,position):
            print("SA")
            return SA(V2D(0,0),goal_to_ball)
        else:
            print("kje")
            return SA(state.ball.position - state.player(id_team,id_player).position,V2D(0,0))

class forceur_two_to_two(AS):
    def __init__(self):
        AS.__init__(self,"forceur_one_to_one")
    
    def compute_strategy(self,state,id_team,id_player,clever):
        print("oooooooooooooooooooooooooooooooooooooooooo",id_team,id_player)
        
        vod=0
        if id_team==1:
            vod=T1_SENS*COEFF_FORCEUR
            vo=T1_BUT
        elif id_team==2:
            vod=T2_SENS*COEFF_FORCEUR
            vo=T2_BUT
        position=state.player(id_team,id_player).position
        ball_to_player=state.ball.position.distance(state.player(id_team,id_player).position)
        goal_to_player=state.player(id_team,id_player).position.distance(V2D(vo,GAME_HEIGHT/2))
        goal_to_ball= V2D(vo,GAME_HEIGHT/2) -state.ball.position
        ball= PLAYER_RADIUS + BALL_RADIUS
        print("vhg")
        if usefull().has_ball(state,position):
            print("SA")
            return SA(V2D(0,0),goal_to_ball)
        else:
            print("kje")
            return SA(state.ball.position - state.player(id_team,id_player).position,V2D(0,0))


