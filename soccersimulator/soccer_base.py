# -*- coding: utf-8 -*-
import numpy as np
from copy import deepcopy
###############################################################################
# Constantes
###############################################################################


GAME_WIDTH=150
GAME_HEIGHT=90
GAME_GOAL_HEIGHT=20
PLAYER_RADIUS=1.
BALL_RADIUS=0.65
maxPlayerAcceleration=0.1
playerBrackConstant=0.1
ballBrakeSquare=0.01
ballBrakeConstant=0.08
maxPlayerSpeed=1.
maxBallAcceleration=5.
maxPlayerShoot=2.
shootRandomAngle=0.1
nbWithoutShoot=10
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

    def __init__(self,x=0,y=0):
        """ create a vector
        :param x: 1st coordinate
        :param y: 2nd coordiante
        :type x: float
        :type y: float
        """
        self._v=np.array((float(x),float(y)))
    def copy(self):
        return Vector2D(self.x,self.y)
    def __str__(self):
        return "(%f,%f)" % (self.x,self.y)
    def __repr__(self):
        return "Vector2D%s" % self.__str__()
    def dot(self,v):
        return self.v.dot(v.v)
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
        return self._v[0]
    @x.setter
    def x(self,value):
        self._v[0]=float(value)
    @property
    def y(self):
        """
        the 2nd coordinate
        :type: float
        """
        return self._v[1]
    @y.setter
    def y(self,value):
        self._v[1]=float(value)
    @property
    def v(self):
        """
        the associated numpy vector
        :type: numpy.array
        """
        return np.array(self._v)
    def random(self,low=0.,high=1.):
        """
        Randomize the vector
        :param float low: low limit
        :param float high: high limit
        :rtype: None
        """
        self._v=(np.random.rand()*(high-low)+low,np.random.rand()*(high-low)+low)
    @property
    def norm(self):
        """
        the norm of the vector
        :rtype: float
        """
        return np.sqrt(self.v.dot(self.v))
    @property
    def angle(self):
        """
        the angle of the vector
        """
        return np.arctan2(self.y,self.x)
    def distance(self,v):
        return np.sqrt((v-self).dot(v-self))
    def normalize(self):
        """
        Normalize the vector
        """
        n=self.norm
        if n!=0:
            self._v=self._v/n
    def product(self,a):
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
        return Vector2D(np.cos(angle)*norm,np.sin(angle)*norm)
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
