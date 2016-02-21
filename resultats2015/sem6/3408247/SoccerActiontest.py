# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 17:36:29 2016

@author: 3408247
"""

from soccersimulator import Vector2D, SoccerAction
action=SoccerAction(acceleration=Vector2D(x=1,y=10),shoot=Vector2D())
action2=action+action

print action
print(    )

print action2