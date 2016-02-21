#!/usr/bin/env python2

from soccersimulator import settings
from soccersimulator import Vector2D

def player_position(state, id_team, id_player):
    return state.player_state(id_team, id_player).position

def ball_position(state):
    return state.ball.position

def goal_position(state, id_team):
    return Vector2D(settings.GAME_WIDTH if id_team == 1 else 0,
                    settings.GAME_HEIGHT / 2)

def players_exclude(state, id_team, id_player):
    for elem in state.players:
        if elem[0] != id_team and elem[1] != id_player:
            yield state.player_state(elem[0], elem[1])
