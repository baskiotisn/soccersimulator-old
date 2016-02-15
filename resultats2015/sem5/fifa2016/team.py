
from soccersimulator.mdpsoccer import  SoccerTeam, Player
#from mdpsoccer import  KeyboardStrategy
from soccersimulator.interfaces import MatchWindow, show
from strategies import *


team1 = SoccerTeam("team1",[Player("Alexous",MarquerStrategy())])
team2 = SoccerTeam("team3",[Player("Alexous",DefenseStrategy()), Player("Alex",MarquerStrategy())])

#team3 = SoccerTeam("team3",[Player("Alexous",PasseStrategy()), Player("Alex",RandomStrategy())])
team4 = SoccerTeam("team4",[Player("Samounette",FoncerStrategy()), Player("Sam",RandomStrategy()), Player("Al",DefenseStrategy()), Player("A",MarquerStrategy())])

#team5 = SoccerTeam("team5",[Player("Alexous",DefenseStrategy()), Player("Alex",DribleStrategy()), Player("Al",DefenseStrategy()), Player("A",DefenseStrategy())])
#team6 = SoccerTeam("team6",[Player("Samounette",RandomStrategy()), Player("Sam",MarquerStrategy()), Player("Sa",DefenseStrategy()), Player("S",DefenseStrategy())])
