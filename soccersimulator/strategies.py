# -*- coding: utf-8 -*-


from soccer_base import *
import mdpsoccer

class SoccerStrategy:
    def __init__(self,name):
        self.name=name
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        raise NotImplementedError,"compute_strategy"
    @property
    def name(self):
        return self.name
    def copy(self):
        return self.__class__(self.name)
