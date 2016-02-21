#!/usr/bin/env python2

import soccersimulator
from soccersimulator import settings
from soccersimulator import AbstractStrategy, SoccerAction
from soccersimulator import Vector2D

from potentialfield import vector_from_field
from util import *

class PotentialFieldStrategy(AbstractStrategy):
    def __init__(self, fields):
        AbstractStrategy.__init__(self, "PotentialFields")
        self.fields = fields
    
    def compute_strategy(self, state, id_team, id_player):
        result = Vector2D(0, 0)
        myself = player_position(state, id_team, id_player)
        
        result += vector_from_field(myself, ball_position(state),
                                    self.fields.ball_field)
        result += vector_from_field(myself, goal_position(state, id_team),
                                    self.fields.goal_field)
        for ally in players_exclude(state, id_team ^ 1, id_player):
            result += vector_from_field(myself, ally.position,
                                        self.fields.ally_field)
        for enemy in players_exclude(state, id_team, -1):
            result += vector_from_field(myself, enemy.position,
                                        self.fields.enemy_field)
        
        return SoccerAction(result)
