# -*- coding: utf-8 -*-

from copy import deepcopy
from soccer_base import *
import mdpsoccer
import pickle
import os
import datetime

def time_stamp():
    return datetime.datetime.now().strftime("%y%m%d-%H%M%S-%f")

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

class ListStrategy(SoccerStrategy):
    def __init__(self):
        self.name="Abstract list strategy"
        self.strategies=[]
    def begin_battles(self,state,count,max_step):
        for s in self.strategies:
            s.begin_battles(state,count,max_step)
    def add_strategy(self,strat):
        self.strategies.append(strat)
    def start_battle(self,state):
        for s in self.strategies:
            s.start_battle(state)
    def finish_battle(self,won):
        for s in self.strategies:
            s.finish_battle(won)
    def end_battles(self):
        for s in self.strategies:
            s.end_battles()


class SelectorStrategy(ListStrategy):
    def __init__(self,list_strat,list_cond):
        self.name="Selecteur elegant"
        self.strategies = list_strat
        self.list_cond = list_cond
    def selector(self,state,player,teamid):
        for i,cond in enumerate(self.list_cond):
            if cond(state,player,teamid):
                return i
        return -1
    def compute_strategy(self,state,player,teamid):
        return self.strategies[self.selector(state,player,teamid)].compute_strategies(state,player,teamid)

class CombineStrategy(ListStrategy):
    def __init__(self):
        self.name=name
        self.strategies=[]
    def compute_strategy(self,state,player,teamid):
        socact=SoccerAction()
        for s in self.strategies:
            socact+=s.compute_strategy(state,player,teamid)
        return socact


class InteractStrategy(ListStrategy):
    def __init__(self,list_key,list_strat,filename=None,save_all=False):
        self.name="Interact Strat abstract"
        if len(list_strat)!=len(list_key):
            raise Exception("InteractStrategy : pas meme longueur pour key_config et list_strat")
        self.strategies=list(list_strat)
        self.list_key=list(list_key)
        self.current=self.strategies[0]
        self.states=[]
        self.save_all=save_all
        self.fn=filename
        self.cur_file=None
        self.state=None

    def __getstate__(self):
        odict=self.__dict__.copy()

        return odict

    def compute_strategy(self,state,player,teamid):
        self.state=state
        if self.save_all:
            self.states.append((self.state.copy_safe(),teamid,player.id,self.current.name))
        return self.current.compute_strategy(state,player,teamid)
    def send_to_strat(self,teamid,player,key):
        if key in self.list_key:
            self.current=self.strategies[self.list_key.index(key)]
            if not self.save_all:
                self.states.append((self.state.copy_safe(),teamid,player.id,self.current.name))
            return True
        return False
    def start_battle(self,state):
        super(InteractStrategy,self).start_battle(state)
        self.state=state
        if self.fn:
            self.cur_file="%s-%s.pkl" % (self.fn,time_stamp(),)
        self.states=[]
    def finish_battle(self,won):
        super(InteractStrategy,self).finish_battle(won)
        if self.cur_file:
            with open(self.cur_file,"wb") as f :
                pickle.dump(self.states,f)
