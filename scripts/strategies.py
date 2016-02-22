from soccersimulator import  Vector2D, SoccerTeam, Player, SoccerAction
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
        BaseStrategy.__init__(self, "Defense")

    def compute_strategy(self, state, id_team, id_player):
        myg = Vector2D((id_team-1)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)
        hisg = Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)
        if (state.ball.position.distance(myg)<settings.GAME_WIDTH/5.):
            return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,
                                hisg-state.ball.position)
        return SoccerAction(myg-state.player_state(id_team,id_player).position,Vector2D())


class DTreeStrategy(BaseStrategy):
    def __init__(self,tree,dic,gen_feat):
        BaseStrategy.__init__(self,"Tree Strategy")
        self.dic = dic
        self.tree = tree
        self.gen_feat= gen_feat
    def compute_strategy(self, state, id_team, id_player):
        label = self.tree.predict(self.gen_feat(state,id_team,id_player))[0]
        if label not in self.dic:
            print("Erreur : strategie %s non trouve" %(label,))
            return SoccerAction()
        return self.dic[label].compute_strategy(state,id_team,id_player)
