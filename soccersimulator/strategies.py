# -*- coding: utf-8 -*-

from copy import deepcopy
from soccer_base import *
import mdpsoccer
import pickle

class SoccerStrategy(object):
    name="Not Defined"
    def __init__(self,name):
        self.name=name
    def begin_battles(self,state,count,max_step):
        pass
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def end_battles(self):
        pass
    def compute_strategy(self,state,player,teamid):
        raise NotImplementedError,"compute_strategy"

class CombineStrategy(SoccerStrategy):
    def __init__(self,name):
        self.name=name
        self.strategies=[]
    def add_strategy(self,strat):
        self.strategies.append(strat)
    def start_battle(self,state):
        for s in self.strategies:
            s.start_battle(state)
    def finish_battle(self,won):
        for s in self.strategies:
            s.finish_battle(won)
    def compute_strategy(self,state,player,teamid):
        socact=SoccerAction()
        for s in self.strategies:
            socact=s.compute_strategy(state,player,teamid)
        return socact

class ReplayStrategy(SoccerStrategy):
    def __init__(self,actions=None,states=None):
        super(ReplayStrategy,self).__init__("Replay")
        self.actions=actions
        self.states=states
        self.i_battles=0
        self.i_state=0
    def begin_battles(self,state,count,max_step):
        self.i_state=0
        self.i_battles=0
    def start_battle(self,state):
        self.i_state=0
        #if self.states[self.i_battles][self.i_state]!=state:
        #    raise Exception, "Not same initial state"
    def compute_strategy(self,state,player,teamid):
        #if state!=self.states[self.i_battles][self.i_state]:
        #        raise Exception,"Not same state : battle %d, state %d" % (self.i_battles,self.i_state)
        act=self.actions[self.i_battles][self.i_state]
        self.i_state+=1
        return act
    def finish_battle(self,won):
        self.i_battles+=1
