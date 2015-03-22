import numpy as np
import pickle
from soccersimulator import TreeIA, TreeStrategy
from strats import *
import os
# Quelques generateurs de features

def distance_ball(state,teamid,playerid):
    return (state.get_team(teamid)[playerid].position-state.ball.position).norm

def distance_mon_but(state,teamid,playerid):
    return (state.get_goal_center(teamid)-state.get_team(teamid)[playerid].position).norm

def distance_autre_but(state,teamid,playerid):
    return (state.get_goal_center(3-teamid)-state.get_team(teamid)[playerid].position).norm

def distance_ball_mon_but(state,teamid,playerid):
    return (state.get_goal_center(teamid)-state.ball.position).norm


def distance_ball_autre_but(state,teamid,playerid):
    return (state.get_goal_center(3-teamid)-state.ball.position).norm


list_fun_features=[distance_ball,distance_mon_but,distance_autre_but,distance_ball_mon_but,distance_ball_autre_but]

# Une fonction de generation de feature.
# np.array permet de transformer en vecteur une liste
def gen_feature_simple(state,teamid,playerid):
    return np.array([f(state,teamid,playerid) for f in list_fun_features])

if __name__=="__main__":
    treeia=TreeIA(gen_feature_simple)
    treeia.learn(fn="test_interact.pkl")
    treeia.save("myfirsttree.pkl")
