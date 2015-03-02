# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 19:04:42 2015

@author: baskiotisn
"""
from soccersimulator import pyglet
from soccersimulator import PygletObserver, LogObserver, PygletReplay
from soccersimulator import SoccerBattle
from soccersimulator import SoccerPlayer, SoccerTeam, InteractStrategy
from strats import RandomStrategy, FonceurStrategy

import glob
import pickle



team1=SoccerTeam("Fonceur/Random")
team1.add_player(SoccerPlayer("Fonceur",FonceurStrategy()))
team1.add_player(SoccerPlayer("Random",RandomStrategy()))

team2=SoccerTeam("Random/Random")
team2.add_player(SoccerPlayer("Random 1",RandomStrategy()))
team2.add_player(SoccerPlayer("Random 2",RandomStrategy()))


list_key_player1=['a','z']
list_key_player2=['q','s']
list_strat_player1=[RandomStrategy(),FonceurStrategy()]
list_strat_player2=[RandomStrategy(),FonceurStrategy()]

# arguemnts :  liste des touches, liste des strategies, nom du fichier, tout sauvegarder ou non, concatener dans un meme fichier a la suite ou non
inter_strat_player1=InteractStrategy(list_key_player1,list_strat_player1,"test_interact.pkl")
inter_strat_player2=InteractStrategy(list_key_player2,list_strat_player2,"test_interact.pkl",True)
team3 = SoccerTeam("Interactive")
team3.add_player(SoccerPlayer("Inter 1",inter_strat_player1))
team3.add_player(SoccerPlayer("Inter 2",inter_strat_player2))
teams =[team1,team2,team3]


def exemple_simple():
    battle=SoccerBattle(teams[0],teams[1])
    obs = PygletObserver()
    obs.set_soccer_battle(battle)
    pyglet.app.run()

def exemple_interact():
    battle=SoccerBattle(teams[0],teams[2])
    obs = PygletObserver()
    obs.set_soccer_battle(battle)
    pyglet.app.run()
    return battle

def exemple_sauvegarde():
    battle=SoccerBattle(teams[0],teams[1])
    obs=PygletObserver()
    obs.set_soccer_battle(battle)
    ## False si on ne veut pas cumuler les sauvegardes dans un meme fichier, True sinon
    log=LogObserver("replay1.pkl",False)
    log.set_soccer_battle(battle)
    pyglet.app.run()
    return battle

def exemple_sans_interface(log=False):
    battle=SoccerBattle(teams[0],teams[1])
    if log:
        log=LogObserver("replay1.pkl",False)
        log.set_soccer_battle(battle)
    battle.run_multiple_battles(5,2000)
    return battle

def exemple_replay():
    obs=PygletReplay()
    obs.load("replay1.pkl")
    pyglet.app.run()


def exemple_load_interact(fn):
    states=[]
    with open(fn,"rb") as f:
        while(1):
            try:
                states+=pickle.load(f)
            except EOFError:
                break
    print "%d etats dans la sauvegarde:" % (len(states))
    for e in states:
        state=e[0]
        teamid=e[1]
        playerid=e[2]
        strat=e[3]
        player=state.team1[playerid] if teamid==1 else state.team2[playerid]
        print "team n°%d, joueur n°%d, strategie %s, joueur : %s, position %s " % (teamid,playerid,strat,player,player.position)

if __name__=="__main__":
    exemple_simple()
