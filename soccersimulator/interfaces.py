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
import soccerobj
import strategies
import pickle
#soccer_base  cste


##############################################################################
## interfaces
##############################################################################

class AbstractSoccerObserver(object):
    def begin_battles(self,state,count,max_step):
        pass
    def start_battle(self,state):
        pass
    def update_battle(self,state,step):
        pass
    def finish_battle(self,winner):
        pass
    def end_battles(self):
        pass
    def is_ready(self):
        return True
    def set_soccer_battle(self,soccer_battle):
        self._soccer_battle=soccer_battle
        self._soccer_battle.listeners+=self

class ConsoleListener(AbstractSoccerObserver):
    def __init__(self):
        pass
    def begin_battles(self,state,count,max_step):
        print "Debut combats : %d" % count
    def start_battle(self,state):
        print "Debut match"
    def update_battle(self,state,step):

        if step % 100==0:
            print "Update %d step " %step
            print str(state)
    def finish_battle(self,winner):
        print "Fin : %d" %winner
    def end_battles(self):
        print "Fin combats"


class LogListener:
    pass
class LogObserver(AbstractSoccerObserver):
    def __init__(self,filename=None,append=True,autosave=True):
        self.autosave=autosave
        self.filename=filename
        self._append=append
    def set_soccer_battle(self,soccer_battle):
        super(LogObserver,self).set_soccer_battle(soccer_battle)
        self._soccer_battle=soccer_battle.copy_safe()
    def begin_battles(self,state,count,max_step):
        self._soccer_battle.count=count
        self._soccer_battle.max_step=max_step
        self._soccer_battle.battles=[]
    def start_battle(self,state):
        self._soccer_battle.battles.append([])
    def update_battle(self,state,step):
        self._soccer_battle.battles[-1].append(state.copy_safe())
    def finish_battle(self,winner):
        pass
    def end_battles(self):
        if self.autosave:
            self.write()
    def write(self,fn=None):
        if not fn:
            fn = self.filename
        if self.filename:
            with file(self.filename,"a" if self._append else "wb") as f:
                pickle.dump(self._soccer_battle,f,-1)


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
              time.sleep(0.0001)

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



class PygletAbstractObserver(pyglet.window.Window):

    key_handlers = {
            pyglet.window.key.ESCAPE: lambda w: w.exit(),
            pyglet.window.key.N: lambda w: w.set_ready(),
            pyglet.window.key.M: lambda w: w.switch_manual_step()
    }

    def __init__(self,width=1200,height=800):
        pyglet.window.Window.__init__(self,width=width,height=height,resizable=True)
        self._state=None
        self.focus()
        self.set_size(width,height)
        self._is_ready=False
        self._manual_step=True
        self._fps=40.
        self._soccer_battle=None
        pyglet.clock.schedule_interval(self.update,1./self._fps)


    def set_soccer_battle(self,battle):
        self._soccer_battle=battle
        self.create_drawable_objects()
    def create_drawable_objects(self):
        self.focus()
        self._sprites=dict()
        self._sprites[("ball",0)]=BallSprite(self)
        for p in self._soccer_battle.team1.players:
            self._sprites[(p.name,1)]=PlayerSprite(p.name,1,self)
        for p in self._soccer_battle.team2.players:
            self._sprites[(p.name,2)]=PlayerSprite(p.name,2,self)
        self._background=BackgroundSprite(self)
    def render(self):
        try:
            if hasattr(self,"_state") and self._state:
                gl.glClear(gl.GL_COLOR_BUFFER_BIT)
                self._background.draw()
                for d in self._sprites.values():
                    d.draw()

        except Exception:
            time.sleep(0.0001)

    def on_draw(self):
        self.render()

    def on_key_press(self,symbol, modifiers):
        if symbol in self.key_handlers:
            handler = self.key_handlers.get(symbol, lambda w: None)
            handler(self)
            return pyglet.event.EVENT_HANDLED

    def update(self,dt):
        #self.render()
        pass

    def switch_manual_step(self):
        self._manual_step = not self._manual_step
        if not self._manual_step:
            self.set_ready()
    def on_resize(self,width, height):
        pyglet.window.Window.on_resize(self,width,height)
        self.focus()
        return pyglet.event.EVENT_HANDLED
    def set_ready(self,d=0):
        self._is_ready=True
    def is_ready(self):
        return self._is_ready
    def focus(self):
        try:
            gl.glMatrixMode(gl.GL_PROJECTION)
            gl.glLoadIdentity()
            gl.gluOrtho2D(0, GAME_WIDTH, 0, GAME_HEIGHT)
            gl.glMatrixMode(gl.GL_MODELVIEW)
            gl.glLoadIdentity()
        except Exception:
            time.sleep(0.0001)
    def on_close(self):
        res=pyglet.window.Window.on_close(self)
        self.exit()
        return res
    def exit(self):
        self.set_ready()
        self.close()
        pyglet.app.exit()

class PygletReplay(PygletAbstractObserver):

    def __init__(self,width=1200,height=800):
        super(PygletReplay,self).__init__(width,height)
        self.key_handlers.update({pyglet.window.key.P: lambda w: w.play(),\
                                  pyglet.window.key.A: lambda w: w.play_prev_tour(),\
                                  pyglet.window.key.Z : lambda w: w.play_next_tour(),\
                                  pyglet.window.key.Q: lambda w: w.play_prev_battle(),\
                                  pyglet.window.key.S: lambda w: w.play_next_battle()})
        pyglet.clock.schedule_interval(self.update,1./self._fps)
        self._i_battle=0
        self.i=0
        self._tournament=None

    def play(self):
        if not self._tournament:
            return
        self.set_soccer_battle(self._tournament[self._i_tour])
        self._i_battle=0
        self.cur_battle=self._soccer_battle.battles[self._i_battle]
        self.i=0
        self.set_ready()

    def play_prev_battle(self):
        self._is_ready=False
        if self._i_battle>0:
            self.i_battle-=1
            self.cur_battle=self._soccer_battle.battles[self._i_battle]
            self.i=0
        self._is_ready=True

    def play_next_battle(self):
        self._is_ready=False
        self._i_battle+=1
        if self._i_battle<len(self._soccer_battle.battles):
            self.cur_battle=self._soccer_battle.battles[self._i_battle]
            self.i=0
        else:
            self.play_next_tour()
        self._is_ready=True

    def play_prev_tour(self):
        self._is_ready=False
        if self._i_tour>0:
            self._i_tour-=1
            self.play()
        self._is_ready=True

    def play_next_tour(self):
        self._is_ready=False
        self._i_tour+=1
        if self._i_tour<len(self._tournament):
            self.play()
        self._is_ready=True

    def update(self,dt):
        if not self.is_ready() or not self._soccer_battle:
            return
        if self.i<len(self.cur_battle):
            self._state=self.cur_battle[self.i]
            self.i+=1
        else:
            self.play_next_battle()
        super(PygletReplay,self).update(dt)

    def load(self,fn):
        battles=[]
        with open(fn,"rb") as f:
            while 1:
                try:
                    battles.append(pickle.load(f))
                except EOFError:
                    break
        self._tournament=battles
        self._i_tour=0
        print "Fin Load"

class PygletObserver(PygletAbstractObserver):

    def __init__(self,width=1200,height=800):
        super(PygletObserver,self).__init__(width,height)
        self._thread=None
        self.stop_thread=False
        self.key_press=None
        self.key_handlers.update({pyglet.window.key._1: lambda w: w.start_config()})

    def start_config(self,num_games=None,num_steps=None):
        self.start(self._soccer_battle.start_by_thread,(self,num_games,num_steps))

    def start(self,target,args):
        if not self._thread:
            self._thread=threading.Thread(target=target,args=args)
            self._thread.daemon=False
            self._thread.start()

    def on_key_press(self,symbol, modifiers):
        if super(PygletObserver,self).on_key_press(symbol,modifiers) != pyglet.event.EVENT_HANDLED:
            k=pyglet.window.key.symbol_string(symbol)
            if modifiers & pyglet.window.key.MOD_SHIFT:
                k=k.capitalize()
            else:
                k=k.lower()
            self.key_press=k
            self._soccer_battle.send_to_strat(self.key_press)
    def update(self,dt):
        if self.is_ready():
            self._soccer_battle.update()
            self._state=self._soccer_battle.state
            if self._manual_step:
                self._is_ready=False
            super(PygletObserver,self).update(dt)


    def exit(self):
        self.set_ready()
        self.stop_thread=True
        if self._thread:
            time.sleep(0.1)
        super(PygletObserver,self).exit()
