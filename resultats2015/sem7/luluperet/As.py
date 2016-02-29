import soccersimulator, soccersimulator.settings,math
from soccersimulator.settings import * 
from soccersimulator import SoccerTeam as STe,SoccerMatch as SM, Player, SoccerTournament as ST, BaseStrategy as AS, SoccerAction as SA, Vector2D as V2D,SoccerState as SS

settings=soccersimulator.settings

class usefull:
    def __init__(self):
        self.name="czc"
    def nb_p(self,state):
        return len([x for x in state._configs.keys()])
    def next_position_player(self,dis,config):
        #config_action <=>self._action
        #config_state_vitesse <=> self._state.vitesse
        #config_state_position <=>self._state.position
        
        config_state_vitesse = config._state.vitesse * (1 - settings.playerBrackConstant) #frottemnt
        config_state_vitesse = (config_state_vitesse+dis.norm_max(settings.maxPlayerAcceleration)).norm_max(settings.maxPlayerSpeed)#sef.acc = _action.norm-max ET verif vitesse pas max
        config_state_position = config._state.position+ config_state_vitesse.norm_max(settings.maxPlayerSpeed)
            #if self._state.position.x < 0 or self.position.x > settings.GAME_WIDTH \
           # or self.position.y < 0 or self.position.y > settings.GAME_HEIGHT:
            #   self._state.position.x = max(0, min(settings.GAME_WIDTH, self.position.x))
            #    self._state.position.y = max(0, min(settings.GAME_HEIGHT, self.position.y))
            #    self._state.vitesse.norm = 0
        return config_state_position

    def has_ball(self,state,dis):
       return  state.ball.position.distance(dis) <=PLAYER_RADIUS + BALL_RADIUS
    
    def has_ball_next(self,state,id_team,id_player):
        dis=state.ball.position - state.player_state(id_team, id_player).position
        config=state.player(id_team,id_player)
        f=self.next_position_player(dis,config)
        return f
    
    def dvt (self,me,him,team):
        if team==1:
            return me.x-him.x >0
        else:
            return me.x -him.x<0
    def has_ball_dvt(self,state,dis,me,team):
        return self.has_ball(state,dis) and not self.dvt(me,dis,team)
class all:
    def __init__(self,num=1):
        print("NUM: ",num)
        self.num=num
    def compute_strategy(self,state,id_team,id_player):
        print("NUM222: ",self.num)
        if self.num==1:
            return coco().compute_strategy(state,id_team,id_player)
        elif self.num==0:
            return cocof().compute_strategy(state,id_team,id_player)
        elif self.num==3:
            return cf().compute_strategy(state,id_team,id_player)

#!/usr/bin/python
# -*- coding: utf-8 -*-

class coco(AS):

    def __init__(self):
        AS.__init__(self, 'Mourinho')
        self.tri=0
        self.coi=0
    def donne_autre(self, state, d):
        a = [x for x in state.players if x[0] == d][0]
        (x, y) = a
        return y
    
    def one_to_one(self,state,id_team,id_player):
        print("LUCAS")
        if id_team == 1:
            nb = GAME_WIDTH
            nbb = 5
            qui = 2
        elif id_team == 2:
            nb = 0
            nbb = -5
            qui = 1
        self.coi+=1
        autre = self.donne_autre(state, qui)
        coc = 0
        n = state.player(qui, autre)
        dis = state.ball.position - state.player_state(qui, autre).position
        moi = state.player_state(id_team, id_player).position
        ball_to_player = state.ball.position.distance(state.player_state(id_team,id_player).position)
        s = usefull().next_position_player(dis, n)
        p=usefull().has_ball_dvt(state,s,moi,id_team)
        print("has basll: ",p)
        print("ball to: ",ball_to_player)
        bh=40
        if ball_to_player <= PLAYER_RADIUS + BALL_RADIUS:
            print("COCOAC")
            if not p:
                if self.tri==1:
                    print("PRUNEEEEEEEE")
                    return SA(state.ball.position - state.player_state(id_team,id_player).position, V2D(nb, 45) - state.ball.position)
                else:
                    print("BANANE")
                    return SA(state.ball.position - state.player_state(id_team,id_player).position, (V2D(nb, 45) - state.ball.position).norm_max(1-(state.ball.vitesse).norm))
            else:
                print("tri terapi")
                self.tri=1
                self.coi=0
                return SA(V2D(0, 0), (V2D(nb, 45) - state.ball.position).norm_max(5)+V2D(nbb,-2))
        
        else:
            if ball_to_player <= 55 or self.tri==1:
                print("KAKAO")
                if usefull().dvt(moi,s,id_team):
                    return SA(state.ball.position - state.player_state(id_team,id_player).position, V2D(nb, 45) - state.ball.position)
                else:
                    hh=usefull().has_ball_next(state,id_team,id_player)
                    if usefull().has_ball(state,hh):
                        return SA(state.ball.position - state.player_state(id_team,id_player).position, (V2D(nb, 45) - state.ball.position).norm_max(5)+V2D(nbb,-2))
                    else:
                        return SA(state.ball.position - state.player_state(id_team,id_player).position, V2D(0, 0))

            else:
                return SA(V2D(0, 0), V2D(1, 0))

    def compute_strategy(self,state,id_team,id_player,):
                # print("f",state.ball.vitesse.norm)
        if usefull().nb_p(state) >= 2 :
            return self.one_to_one(state, id_team, id_player)

			                
                
class simple(AS):
    def __init__(self):
        AS.__init__(self,"Gardiola")
    def compute_strategy(self,state,id_team,id_player):
        return SA(V2D(0,45)-state.player_state(id_team,id_player).position,V2D(0,0))

class cf(AS):
    
    def __init__(self):
        AS.__init__(self, 'Mourinho')
        self.tri=0
        self.coi=0
    def donne_autre(self, state, d):
        a = [x for x in state.players if x[0] == d][0]
        (x, y) = a
        return y
    
    def one_to_one(self,state,id_team,id_player):
        print("-------------------------------------------")
        print("team  ", id_team)
        if id_team == 1:
            nb = GAME_WIDTH
            nbb = 4
            qui = 2
        elif id_team == 2:
            nb = 0
            nbb = -4
            qui = 1
        self.coi+=1
        autre = self.donne_autre(state, qui)
        coc = 0
        n = state.player(qui, autre)
        dis = state.ball.position - state.player_state(qui, autre).position
        moi = state.player_state(id_team, id_player).position
        ball_to_player = state.ball.position.distance(state.player_state(id_team,id_player).position)
        s = usefull().next_position_player(dis, n)
        p=usefull().has_ball_dvt(state,s,moi,id_team)
        print("has basll: ",p)
        print("ball to: ",ball_to_player)
        if ball_to_player <= PLAYER_RADIUS + BALL_RADIUS:
            print("COCOAC")
            if not p:
                if self.tri==1:
                    print("PRUNEEEEEEEE")
                    return SA(state.ball.position - state.player_state(id_team,id_player).position, V2D(nb, 45) - state.ball.position)
                else:
                    print("BANANE")
                    if usefull().dvt(moi,s,id_team):
                        print("choxo")
                        return SA(state.ball.position - state.player_state(id_team,id_player).position, V2D(nb, 45) - state.ball.position)
                    else:
                        print("hio")
                        return SA(state.ball.position - state.player_state(id_team,id_player).position, (V2D(nb, 45) - state.ball.position).norm_max(1-(state.ball.vitesse).norm))
            else:
                print("tri terapi")
                self.tri=1
                self.coi=0
                return SA(V2D(0, 0), (V2D(nb, 45) - state.ball.position).norm_max(5))
        
        else:
            hh=usefull().has_ball_next(state,id_team,id_player)
            if usefull().has_ball(state,hh):
                return SA(state.ball.position - state.player_state(id_team,id_player).position, (V2D(nb, 45) - state.ball.position).norm_max(5)+V2D(nbb,-2))
            else:
                return SA(state.ball.position - state.player_state(id_team,id_player).position, V2D(0, 0))

    def compute_strategy(self,state,id_team,id_player,):
    # print("f",state.ball.vitesse.norm)
    
        if usefull().nb_p(state) >= 2:
            return self.one_to_one(state, id_team, id_player)

class cocof(AS):
    def __init__(self):
        AS.__init__(self,"Gardiola")
        self._bl=False
    def compute_strategy(self,state,id_team,id_player):
        global GAME_WIDTH,BALL_RADIUS,PLAYER_RADIUS
        if (state.ball.position.distance(state.player_state(id_team,id_player).position) <= (PLAYER_RADIUS + BALL_RADIUS) ) :
            print("oco")
            if id_team==1:
                nb=GAME_WIDTH
                nbb=4
            elif id_team==2:
                nb=0
                nbb=-4
            self._bl=True
	    if nb- state.player_state(id_team,id_player).position.x <=40: 
            	return SA(V2D(0,0),(V2D(nb,45)-state.ball.position).norm_max(5))
	    else:
		return SA(V2D(0,0),(V2D(nb,45)-state.ball.position).norm_max(0.5))
        else:
            print("IIIo")
            self_bl=False
            return SA(state.ball.position-state.player_state(id_team,id_player).position,V2D(0,0))
