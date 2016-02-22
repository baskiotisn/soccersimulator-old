from soccersimulator import  Vector2D, SoccerTeam, Player, SoccerTournament, SoccerMatch, SoccerAction, show
from soccersimulator import KeyboardStrategy, BaseStrategy
from soccersimulator import settings
class RandomStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "Random")

    def compute_strategy(self, state, id_team, id_player):
        return SoccerAction(Vector2D.create_random(-1,1),Vector2D.create_random(-1,1))

class FonceurStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "Fonceur")

    def compute_strategy(self, state, id_team, id_player):
        hisg = Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)
        return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,
                            hisg-state.ball.position)

class DefenseStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "Fonceur")

    def compute_strategy(self, state, id_team, id_player):
        myg = Vector2D((id_team-1)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)
        hisg = Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)
        if (state.ball.position.distance(myg)<settings.GAME_WIDTH/5.):
            return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,
                                hisg-state.ball.position)
        return SoccerAction(myg-state.player_state(id_team,id_player).position,Vector2D())


#### Definition des strategies
strat_key = KeyboardStrategy()
strat_key.add("a",RandomStrategy())
strat_key.add("z",FonceurStrategy())
strat_key.add("e",DefenseStrategy())
teams_1p = [SoccerTeam("keyb",[Player("KBs", strat_key)]),
            SoccerTeam("foncteam",[Player("Fonceur", FonceurStrategy())])]
teams_2p = [SoccerTeam("keyb",[Player("KBs", strat_key),Player("Defense",DefenseStrategy())]),
            SoccerTeam("foncteam",[Player("Fonceur",FonceurStrategy()),Player("Defense", DefenseStrategy())])]


## Match
teams = teams_1p
match = SoccerMatch(teams[0],teams[1], 1000)
show(match)

## Sauvegarde des exemples, mettre False a True si concatenation des fichiers
strat_key.write("test.tree",False)


## Lecture du fichier cree
exemples = KeyboardStrategy.read("./test.tree")



