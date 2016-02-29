
from soccersimulator.mdpsoccer import  SoccerTeam, Player
from soccersimulator.mdpsoccer import  KeyboardStrategy
from soccersimulator.interfaces import MatchWindow, show
from strategies import *


strat1 = KeyboardStrategy(fn = "resultat") 
strat1.add("u",DefenseStrategy())
strat1.add("j",MarquerStrategy())
strat1.add("k",RandomStrategy())

strat2 = KeyboardStrategy() 
strat2.add("a",FoncerStrategy())
strat2.add("q",MarquerStrategy())
strat2.add("w",RandomStrategy())



team1 = SoccerTeam("team1",[Player("Alexous",strat1)])
team2 = SoccerTeam("team2",[Player("Sam",strat1), Player("Slex",RandomStrategy())])
#team3 = SoccerTeam("team3",[Player("Aam",strat1), Player("Alex",RandomStrategy())])
#team3 = SoccerTeam("team3",[Player("Alexous",TestStrategy()), Player("Alex",RandomStrategy())])
team4 = SoccerTeam("team4",[Player("Samounette",strat1), Player("Sam",strat2), Player("Al",strat2), Player("A",strat1)])

#team5 = SoccerTeam("team5",[Player("Alexous",DefenseStrategy()), Player("Alex",DribleStrategy()), Player("Al",DefenseStrategy()), Player("A",DefenseStrategy())])
#team6 = SoccerTeam("team6",[Player("Samounette",RandomStrategy()), Player("Sam",MarquerStrategy()), Player("Sa",DefenseStrategy()), Player("S",DefenseStrategy())])