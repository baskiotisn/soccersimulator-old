#!/usr/bin/env python2

class FieldData:
    def __init__(self, value, falloff):
        self.value = value
        self.falloff = falloff

class PotentialFields:
    def __init__(self, b, g, a, e):
        self._ball_field = b
        self._goal_field = g
        self._ally_field = a
        self._enemy_field = e
    
    @property
    def ball_field(self):
        return self._ball_field
    
    @property
    def goal_field(self):
        return self._goal_field
    
    @property
    def ally_field(self):
        return self._ally_field
    
    @property
    def enemy_field(self):
        return self._enemy_field

def vector_from_field(origin, target, field):
    direction = target - origin
    distance = direction.norm
    direction.normalize()
    return direction * field.value * field.falloff(distance)

def no_falloff(distance):
    return 1

def linear_falloff(distance, maximum):
    if distance >= maximum:
        return 0
    return 1 - (distance * 1.0 / maximum)

def inverse_linear_falloff(distance, maximum):
    if distance >= maximum:
        return 1
    return distance * 1.0 / maximum
