from soccersimulator import Vector2D,  SoccerAction, SoccerStrategy


class RandomStrategy(SoccerStrategy):
    def __init__(self):
        self.name="Random"
        self.keys=[]
    def compute_strategy(self,state,player,teamid):
	       return SoccerAction(Vector2D.create_random(-0.1,0.1),Vector2D.create_random(-0.1,0.1))


class FonceurStrategy(SoccerStrategy):
    def __init__(self):
        self.name="Fonceur"
    def compute_strategy(self,state,player,teamid):
    	acc=state.ball.position-player.position
    	acc.scale(1000)
    	shoot=state.get_goal_center((3-teamid))-player.position
    	shoot.scale(1000)
        return SoccerAction(acc,shoot)
