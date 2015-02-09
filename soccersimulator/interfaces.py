# -*- coding: utf-8 -*-

##############################################################################
## Simple implémentation de l'observer pattern
##############################################################################
import pyglet
from pyglet import gl
import numpy as np
from soccer_base import *
import threading
import time

#soccer_base  cste


##############################################################################
## interfaces
##############################################################################

class AbstractSoccerObserver(object):
    def begin_battles(self,count):
        raise NotImplementedError,'begin_battles'
    def start_battle(self,state):
        raise NotImplementedError,'start_battle'
    def update_battle(self,state,step):
        raise NotImplementedError,'update_battle'
    def finish_battle(self,state,winner):
        raise NotImplementedError, 'finish_battle'
    def end_battles(self):
        raise NotImplementedError,'end_battles'
    def is_ready(self):
        return True

    def set_soccer_battle(self,soccer_battle):
        self._soccer_battle=soccer_battle
        self._soccer_battle.listeners+=self

class ConsoleListener(AbstractSoccerObserver):
    def __init__(self):
        pass
    def begin_battles(self,count):
        print "Debut combats : %d" % count
    def start_battle(self,state):
        print "Debut match"
    def update_battle(self,state,step):

        if step % 100==0:
            print "Update %d step " %step
            print str(state)
    def finish_battle(self,state,winner):
        print "Fin : %d" %winner
    def end_battles(self):
        print "Fin combats"


class LogListener(AbstractSoccerObserver):

    def __init__(self,filename=None,autosave=True):
        self._battles_list=[]
        self.autosave=autosave
        self.filename=filename
    def begin_battles(self,count):
        self._states=[]
    def start_battle(self,state):
        self._states=[state]
    def update_battle(self,state,step):
        self._states.append(state)
    def finish_battle(self,state,winner):
        self._battles_list.append(self._states)
        if self.autosave:
            self.save()
    def end_battles(self):
        pass
    def save(self):
        if self.filename:
            pickle.dump(self,file(self.filename,"wb"),3)


class ObjectSprite:
        def __init__(self,name="",movable=True,items=None):
            self.primitives=[]
            self.name=name
            self.has_vector=False
            self.movable=movable
            self._position=Vector2D()
            self._angle=0
            if items:
                self.add_primitives(items)
        def add_primitives(self,items):
            for item in items:
                self.primitives.append(item)
        def _get_object(self):
            raise NotImplementedError,"_get_object"
        @property
        def position(self):
            if self.movable:
                return self._get_object().position
            return self._position

        @property
        def angle(self):
            if self.movable:
                return self._get_object().angle
            return self._angle
        @angle.setter
        def angle(self,val):
            self._angle=val
        @position.setter
        def position(self,val):
            self._position=val
        def draw(self):
          try:
            gl.glPushMatrix()
            gl.glTranslatef(self.position.x,self.position.y,0)
            gl.glRotatef(self.angle*180./np.pi,0,0,1)
            for p in self.primitives:
                gl.glColor3f(*p.color)
                gl.glBegin(p.primtype)
                for vert in p.verts:
                    gl.glVertex2f(*vert)
                gl.glEnd()
            gl.glPopMatrix()
          except Exception,e:
              #print "***********\n------- %s -------\n**********" % self.name
              #print "***********\n------- %s \n %s \n %s -------\n**********" % (str(p.verts),str(p.color),str(p.primtype))
              time.sleep(1)
              #raise e

TEAM1_COLOR=[0.9,0.1,0.1]
TEAM2_COLOR=[0.1,0.1,0.9]
FIELD_COLOR=[0.3,0.9,0.3]
BALL_COLOR=[0.8,0.8,0.2]
LINE_COLOR=[1.,1.,1.]
BG_COLOR=[0.,0.,0.]
GOAL_COLOR=[0.2,0.2,0.2]

class Primitive2DGL(object):
        @staticmethod
        def create_circle(radius,color=[1,1,1],prct=1.,angle=0.):
            steps=int(10*radius*np.pi*prct)
            s=np.sin(2*np.pi/steps)
            c=np.cos(2*np.pi/steps)
            dx,dy=np.cos(angle)*radius,np.sin(angle)*radius
            res=[(0.,0.)]
            for i in range(steps):
                res.append((dx,dy))
                dx,dy=(dx*c-dy*s),(dy*c+dx*s)
            return [Primitive2DGL(res,color)]
        @staticmethod
        def create_vector(length,color=[1,1,1]):
            primtype=gl.GL_LINES
            verts=[(0,0),(length,0),(length,0),(length*0.9,0.1*length),(length,0),(length*0.9,-0.1*length)]
            return [Primitive2DGL(verts,color,primtype)]

        @staticmethod
        def create_player(color):
            rad=PLAYER_RADIUS
            eps=0.3*rad
            corps=Primitive2DGL([ (-rad,-rad), (-rad,rad),
                             (rad-eps,rad),(rad-eps,-rad)],color)
            front=Primitive2DGL([(rad-eps,rad*0.85),(rad,0),(rad-eps,-rad*0.85)],color)
            return [corps,front]
        @staticmethod
        def create_ball():
            rad=BALL_RADIUS
            return Primitive2DGL.create_circle(rad,BALL_COLOR)
        @staticmethod
        def create_field():
            field=Primitive2DGL([(0,0),(0,GAME_HEIGHT),
                                 (GAME_WIDTH,GAME_HEIGHT),
                                 (GAME_WIDTH,0)],FIELD_COLOR)
            bandes_1=Primitive2DGL([(0,0),(GAME_WIDTH,0),
                                  (GAME_WIDTH,GAME_HEIGHT),
                                    (0,GAME_HEIGHT),(0,0)],LINE_COLOR,gl.GL_LINE_STRIP)
            bandes_2=Primitive2DGL([(GAME_WIDTH/2,GAME_HEIGHT),
                                 (GAME_WIDTH/2,0)],LINE_COLOR,gl.GL_LINE_STRIP)
            y1=(GAME_HEIGHT-GAME_GOAL_HEIGHT)/2
            y2=(GAME_HEIGHT+GAME_GOAL_HEIGHT)/2
            xend=GAME_WIDTH
            goals_1=Primitive2DGL([(0,y1),(0,y2),(2,y2),(2,y1)],GOAL_COLOR)
            goals_2=Primitive2DGL([(xend,y2),(xend,y1),(xend-2,y1),(xend-2,y2)],GOAL_COLOR)
            return [field,bandes_1,bandes_2,goals_1,goals_2]
        def __init__(self,verts,color,primtype=gl.GL_TRIANGLE_FAN):
            self.verts=verts
            self.color=color
            self.primtype=primtype
        def offset(self,dx,dy):
            self.verts=[(v[0]+dx,v[1]+dy) for v in self.verts]

            return self


class VectorSprite(ObjectSprite):
        def __init__(self,position,angle):
            ObjectSprite.__init__(self,"")
            self._position=position
            self._angle=angle
        @ObjectSprite.position.getter
        def position(self):
            return self._position
        @ObjectSprite.angle.getter
        def angle(self):
            return self._angle

class PlayerSprite(ObjectSprite):
        def __init__(self,name,team,obs):
            ObjectSprite.__init__(self,name)
            self.team=team
            self._obs=obs
            color=TEAM1_COLOR
            #self._label=pyglet.text.Label(self.name,font_name='Times New Roman',font_size=20)
            if team!=1:
                color=TEAM2_COLOR
            self.add_primitives(Primitive2DGL.create_player(color))
        def _get_object(self):
            return self._obs._state.get_team(self.team)[self.name]
        def draw(self):
            ObjectSprite.draw(self)
            speed=self._get_object().speed
            v=VectorSprite(self.position,self.angle)
            v.add_primitives(Primitive2DGL.create_vector(speed*10,get_color_scale(speed/maxPlayerSpeed)))
            v.draw()
            #self._label.x=self._get_object().position.x
            #self._label.y=self._get_object().position.y
            #self._label.draw()

class BallSprite(ObjectSprite):
        def __init__(self,obs):
            ObjectSprite.__init__(self,"ball")
            self._obs=obs
            self.add_primitives(Primitive2DGL.create_ball())
        def _get_object(self):
            return self._obs._state.ball
        def draw(self):
            ObjectSprite.draw(self)
            speed=self._obs._state.ball.speed
            v=VectorSprite(self.position,speed.angle)
            v.add_primitives(Primitive2DGL.create_vector(speed.norm*10,get_color_scale(speed.norm/maxBallAcceleration)))
            v.draw()
class BackgroundSprite(ObjectSprite):
        def __init__(self,obs):
            ObjectSprite.__init__(self,"back",False)
            self.add_primitives(Primitive2DGL.create_field())

def get_color_scale(x):
        return [x,0.,1.-x]


class PygletObserver(pyglet.window.Window,AbstractSoccerObserver):

    key_handlers = {
        pyglet.window.key.ESCAPE: lambda w: w.exit(),
        pyglet.window.key._1: lambda w: w.start_config(),
        #pyglet.window.key._2: lambda w: w.start_multiple(),
        pyglet.window.key.N: lambda w: w.set_ready(),
        pyglet.window.key.M: lambda w: w.switch_manual_step(),

    }

    def __init__(self,width=1200,height=800):
        pyglet.window.Window.__init__(self,width=width,height=height,resizable=True)
        self._state=None
        self.focus()
        self._thread=None
        self.set_size(width,height)
        self._is_ready=True
        self._manual_step=True
        self._fps=40.
        self.stop_thread=False
    def create_drawable_objects(self):
        self.focus()
        self._sprites=dict()
        self._sprites[("ball",0)]=BallSprite(self)
        for p in self._soccer_battle.team1.players:
            self._sprites[(p.name,1)]=PlayerSprite(p.name,1,self)
        for p in self._soccer_battle.team2.players:
            self._sprites[(p.name,2)]=PlayerSprite(p.name,2,self)
        self._background=BackgroundSprite(self)

    def render(self,dt=0):
        if hasattr(self,"_state") and self._state:
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            self._background.draw()
            for d in self._sprites.values():
                d.draw()
    def on_draw(self):
        if self._thread:
            self.render()

    def start_config(self,num_games=1,num_steps=MAX_GAME_STEPS):
        self.start(self._soccer_battle.start_by_thread,(3,MAX_GAME_STEPS,self))
    def on_key_press(self,symbol, modifiers):
       handler = self.key_handlers.get(symbol, lambda w: None)
       handler(self)
    def start(self,target,args):
        if not self._thread:
            self._thread=threading.Thread(target=target,args=args)
            self._thread.daemon=False
            self._thread.start()

    def begin_battles(self,count):
        self._count=count
        self.create_drawable_objects()
    def start_battle(self,state):
        self.update_battle(state,0)
        self.render()
    def update_battle(self,state,step):
        self._state=state
        self._step=step
        self._is_ready=False
        if not self._manual_step:
            pyglet.clock.schedule_once(self.set_ready,1./self._fps)
    def set_ready(self,d=0):
        self._is_ready=True
    def finish_battle(self,state,winner):
        self.set_ready()
    def end_battles(self):
        self.set_ready()
        self._thread=None
    def on_resize(self,width, height):
        pyglet.window.Window.on_resize(self,width,height)
        self.focus()
        return pyglet.event.EVENT_HANDLED
    def focus(self):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.gluOrtho2D(0, GAME_WIDTH, 0, GAME_HEIGHT)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
    def is_ready(self):
        return self._is_ready
    def switch_manual_step(self):
        self._manual_step = not self._manual_step
        if not self._manual_step:
            self.set_ready()
    def on_close(self):
        res=pyglet.window.Window.on_close(self)
        self.exit()
        return res
    def exit(self):
        self.set_ready()
        self.stop_thread=True
        if self._thread:
            time.sleep(0.1)
        self.close()
        pyglet.app.exit()


def run():
    pyglet.app.run()
