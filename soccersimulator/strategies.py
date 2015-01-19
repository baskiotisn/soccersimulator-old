# -*- coding: utf-8 -*-


from soccer_base import *
import mdpsoccer

class SoccerStrategy:    
    def __init__(self,name):    
        self.name=name
    def start_battle(self,state):
        raise NotImplementedError,"start_battle"
    def finish_battle(self,won):
        raise NotImplementedError,"finish_battle"
    def compute_strategy(self,state,player,teamid):
        raise NotImplementedError,"compute_strategy"      
    @property
    def name(self):
        return self.name
    def copy(self):
        raise NotImplementedError,"copy"
    def create_strategy(self):
        raise NotImplementedError,"create_strategy"

