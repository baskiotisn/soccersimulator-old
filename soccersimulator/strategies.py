
# -*- coding: utf-8 -*-

from copy import deepcopy
from soccer_base import *
import mdpsoccer
import pickle
import os
import datetime
import numpy as np
from sklearn.tree import DecisionTreeClassifier,export_graphviz

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
    def __init__(self,list_key,list_strat,filename=None,save_all=False,append=True):
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
        self._append=append
    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if k != 'states':
                setattr(result, k, deepcopy(v, memo))
        result.states=self.states
        return result

    def compute_strategy(self,state,player,teamid):
        self.state=state
        if self.save_all:
            self.states.append((self.state,teamid,player.id,self.current.name))
        return self.current.compute_strategy(state,player,teamid)
    def send_to_strat(self,teamid,player,key):
        if key in self.list_key:
            self.current=self.strategies[self.list_key.index(key)]
            if not self.save_all:
                self.states.append((self.state,teamid,player.id,self.current.name))
            return True
        return False
    def start_battle(self,state):
        super(InteractStrategy,self).start_battle(state)
        self.state=state
        if self.fn:
            if self._append:
                self.cur_file=self.fn
            else:
                self.cur_file="%s-%s.pkl" % (self.fn,time_stamp(),)
        self.states=[]
    def finish_battle(self,won):
        super(InteractStrategy,self).finish_battle(won)
        if self.cur_file:
            with open(self.cur_file,"a" if self._append else "wb") as f :
                pickle.dump(self.states,f,-1)

class TreeIA:
    def __init__(self,gen_feat=None,strats=None):
        self.tree=None
        self.strats=strats
        self.gen_feat=gen_feat
    def learn(self,states=None,depth=5,min_samples=2,fn=None):
        if fn:
            states=[]
            with open(fn,"rb") as f:
                while(1):
                    try:
                        states+=pickle.load(f)
                    except EOFError:
                        break
        train_set=np.array([self.gen_feat(s[0],s[1],s[2]) for s in states])
        label_set=np.array([s[3] for s in states])
        self.tree=DecisionTreeClassifier(max_depth=depth,min_samples_split=min_samples)
        self.tree.fit(train_set,label_set)
    def save(self,fn):
        with open(fn,"wb") as f:
            pickle.dump(self.tree,f,-1)
    def load(self,fn):
        with open(fn,"rb") as f:
            self.tree=pickle.load(f)
    def to_dot(self,fn):
        export_graphviz(self.tree,out_file=fn)


class TreeStrategy(SoccerStrategy):
    def __init__(self,name,treeia=None):
        self.name=name
        self.treeia=treeia
    def compute_strategy(self,state,player,teamid):
        strat = self.treeia.tree.predict(self.treeia.gen_feat(state,teamid,player.id))[0]
        return self.treeia.strats[strat].compute_strategy(state,player,teamid)
