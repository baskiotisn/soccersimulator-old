# -*- coding: utf-8 -*-
from copy import deepcopy
import math
import random
###############################################################################
# Constantes
###############################################################################


GAME_WIDTH=150
GAME_HEIGHT=90
GAME_GOAL_HEIGHT=20
PLAYER_RADIUS=1.
BALL_RADIUS=0.65

maxPlayerSpeed=1.
maxPlayerAcceleration=0.2
playerBrackConstant=0.1
nbWithoutShoot=10
maxPlayerShoot=3.

maxBallAcceleration=5.
shootRandomAngle=0.1

#ballBrakeConstant=0.04
#ballBrakeSquare=0.002
ballBrakeConstant=0.08
ballBrakeSquare=0.01

MAX_GAME_STEPS=5000
NB_MAX_EXCEPTIONS=1

class Vector2D(object):
    """ 2D vector oject and operations with float coordinates

    :Example:

    >>> from tools import Vector2D
    >>> o=Vector2D()
    >>> v=Vector2D(2,3)
    >>> w = Vector2D.create_random()
    >>> w=v+v
    """

    def __init__(self,x=0,y=0,angle=None,norm=None):
        """ create a vector
        :param x: 1st coordinate
        :param y: 2nd coordiante
        :type x: float
        :type y: float
        """
        if angle and norm:
            self.x=math.cos(angle)*norm
            self.y=math.sin(angle)*norm
            return
        self.x=float(x)
        self.y=float(y)
    def copy(self):
        return Vector2D(self.x,self.y)
    def __str__(self):
        return "(%f,%f)" % (self.x,self.y)
    def __repr__(self):
        return "Vector2D%s" % self.__str__()
    def dot(self,v):
        return self.x*v.x+self.y*v.y
    def __eq__(self,other):
        return (other.x==self.x) and (other.y==self.y)
    def __add__(self,other):
        return Vector2D(self.x+other.x,self.y+other.y)
    def __sub__(self,other):
        return Vector2D(self.x-other.x,self.y-other.y)
    def __iadd__(self,other):
       self.x+=other.x
       self.y+=other.y
       return self
    def __isub__(self,other):
        self.x-=other.x
        self.y-=other.y
        return self
    @property
    def x(self):
        """
        the 1st coordinate
        :type: float
        """
        return self._x
    @x.setter
    def x(self,value):
        self._x=float(value)
    @property
    def y(self):
        """
        the 2nd coordinate
        :type: float
        """
        return self._y
    @y.setter
    def y(self,value):
        self._y=float(value)
    def random(self,low=0.,high=1.):
        """
        Randomize the vector
        :param float low: low limit
        :param float high: high limit
        :rtype: None
        """
        self.x=random.random()*(high-low)+low
        self.y=random.random()*(high-low)+low
    @property
    def norm(self):
        """
        the norm of the vector
        :rtype: float
        """
        return math.sqrt(self.dot(self))
    @norm.setter
    def norm(self,n):
        if self.norm!=0:
            self.normalize()
            self.scale(n)
    @property
    def angle(self):
        """
        the angle of the vector
        """
        return math.atan2(self.y,self.x)
    @angle.setter
    def angle(self,a):
        n=self.norm
        self.x=math.cos(a)*n
        self.y=math.sin(a)*n
    def distance(self,v):
        return (v-self).norm
    def normalize(self):
        """
        Normalize the vector
        """
        n=self.norm
        if n!=0:
            self.x=self.x/n
            self.y=self.y/n
    def product(self,a):
        """
        Multiply the vector by float a
        :param float a: scale factor
        """
        self.x*=a
        self.y*=a
    def scale(self,a):
        """
        Multiply the vector by float a
        :param float a: scale factor
        """
        self.x*=a
        self.y*=a

    @staticmethod
    def create_polar(angle,norm):
        """
        Create a vector from an angle and a norm
        :param float angle: angle parameter
        :param float norm: norm parameter
        :return: a vector
        :rtype: Vector2D
        """
        return Vector2D(angle=angle,norm=norm)
    @staticmethod
    def create_random(low=0,high=1.):
        """
        Create a random vector
        :param float low: low limit
        :param float high: high limit
        :return: vector
        :rtype: Vector2D
        """
        res=Vector2D()
        res.random(low,high)
        return res


# class SoccerException(Exception):
#     def __init__(self,msg):
#         self.msg=msg
#     def __str__(self):
#         return "Exception %s : %s" % (self.__class__,self.msg)
# class IncorrectTeamException(SoccerException):
#     pass
# class PlayerException(SoccerException):
#     pass
# class StrategyException(SoccerException):
#     pass
# class SoccerBattleException(SoccerException):
#     pass
# class SoccerStateException(SoccerException):
#     pass
