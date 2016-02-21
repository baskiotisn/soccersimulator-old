from soccersimulator import SoccerTeam
from Strategie import *
from soccersimulator import  Player 

team1 = SoccerTeam("JSK",[Player("Fonceur",P1_fonceur)])
team2 = SoccerTeam("JSK",[Player("Fonceur",T2_All),Player("9",attaque_Strategy)])
team4 = SoccerTeam("JSK",[Player("10",milieu),Player("9",attaque_Strategy),Player("4",defense_Strategy),Player("1",goal_strat)])