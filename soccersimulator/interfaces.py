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
import mdpsoccer
import soccerobj
import strategies
import pickle
import traceback
import zlib
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
        self._soccer_battle=None
        self.battles=[]
    def set_soccer_battle(self,soccer_battle):
        super(LogObserver,self).set_soccer_battle(soccer_battle)
    def begin_battles(self,state,count,max_step):
        self.battles=[]
    def start_battle(self,state):
        self.battles.append([])
    def update_battle(self,state,step):
        self.battles[-1].append(state)
    def finish_battle(self,winner):
        pass
    def end_battles(self):
        self.write()
        self.battles=[]
    def write(self,fn=None):
        if not fn:
            fn = self.filename
        if self.filename:
            #battles=[ [(s["team1.name"],s["team2.name"],s["team1",s]) for s in b] for b in battles]
            ## nbp team1_name team2_name count max_steps
            ##
            res=""
            for b in self.battles:
                for s in b:
                    res+="%s" % s.to_blockfile()
                    res+="++++++++++++\n"
                res+="**************\n"
            cres=zlib.compress(res,9)
            with open(self.filename,"a" if self._append else "wb") as f:
                f.write(cres+"\n")
                f.write("-------------\n")
                # for b in self.battles:
                #     for s in b:
                #         f.write("%s" % s.to_blockfile())
                #         f.write("++++++++++++\n")
                #     f.write("**************\n")
                # f.write("-------------\n")
                    #pickle.dump({"soccer_battle":self._soccer_battle.copy(True),"battles":self.battles},f)

    @staticmethod
    def read(fn):
        block=[]
        states=[]
        battles=[]
        tour=[]
        soc_battle=None
        team1=None
        team2=None
        zread=""
        with open(fn,"rb") as f:
            for zl in f:
                if zl.startswith("----"):
                    try:
                        line=zlib.decompress(zread)
                    except:
                        import pdb
                        pdb.set_trace()
                    for l in line.split("\n"):
                        if l =="":
                            continue
                        if l.startswith("++++"):
                            states.append(block)
                            #mdpsoccer.SoccerState.from_blockfile(block,team1,team2))
                            block=[]
                            if soc_battle==None:
                                st=mdpsoccer.SoccerState.from_blockfile(states[-1])
                                team1=st.team1
                                team2=st.team2
                                soc_battle=mdpsoccer.SoccerBattle(team1,team2,st.battles_count,st.max_steps)
                                soc_battle.battles_block=[]
                            continue
                        if l.startswith("****"):
                            soc_battle.battles_block.append(states)
                            states=[]
                            continue
                        block.append(l)
                    #if l.startswith("----"):
                    tour.append(soc_battle)
                    soc_battle=None
                    team1=None
                    team2=None
                    zread=""
                    #continue
                else:
                    zread+=zl
        return tour



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
              print e,traceback.print_exc()
TEAM1_COLOR=[0.9,0.1,0.1]
TEAM2_COLOR=[0.1,0.1,0.9]
FIELD_COLOR=[0.3,0.9,0.3]
BALL_COLOR=[0.8,0.8,0.2]
LINE_COLOR=[1.,1.,1.]
BG_COLOR=[0.,0.,0.]
GOAL_COLOR=[0.2,0.2,0.2]
SCALE_NAME=0.05
HUD_HEIGHT=10
HUD_WIDTH=0
HUD_BKG_COLOR=[0.3,0.3,0.3]
HUD_TEAM1_COLOR=[int(x*255) for x in TEAM1_COLOR]+[200]
HUD_TEAM2_COLOR=[int(x*255) for x in TEAM2_COLOR]+[200]
HUD_TEXT_COLOR=[0,200,0,255]
MSG_TEXT_COLOR=[200,200,200,255]

FPS=40.
FPS_MOD=5.

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
        @staticmethod
        def create_hud():
            hud = Primitive2DGL([(0,GAME_HEIGHT),(0,GAME_HEIGHT+HUD_HEIGHT),\
                        (GAME_WIDTH,GAME_HEIGHT+HUD_HEIGHT),(GAME_WIDTH,GAME_HEIGHT)],HUD_BKG_COLOR)
            return [hud]
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
class TextSprite:
    def __init__(self,text="",color=[255,255,255,255],scale=0.1,position=Vector2D()):
        self._label=pyglet.text.Label(text,color=color,font_name="Arial",font_size=40)
        self.scale=scale
        self.position=position
    def draw(self):
        try:
            gl.glPushMatrix()
            #gl.glLoadIdentity()
            gl.glTranslatef(self.position.x,self.position.y,0)
            gl.glScalef(self.scale,self.scale,1)
            self._label.draw()
            gl.glPopMatrix()
            pass
        except Exception,e:
            time.sleep(0.0001)
            print e,traceback.print_exc()

        except Exception,e:
            time.sleep(0.0001)
            print e,traceback.print_exc()

class PlayerSprite(ObjectSprite):
        def __init__(self,name,team,obs):
            ObjectSprite.__init__(self,name)
            self.team=team
            self._obs=obs
            self.color=TEAM1_COLOR
            if team!=1:
                self.color=TEAM2_COLOR
            self.add_primitives(Primitive2DGL.create_player(self.color))
            self._text=TextSprite(self.name,[int(x*255) for x in self.color]+[200],SCALE_NAME)
        def _get_object(self):
            return self._obs.get_state().get_team(self.team)[self.name]
        def draw(self):
            ObjectSprite.draw(self)
            speed=self._get_object().speed
            self._text.position=self.position
            #strat=TextSprite(self._get_object().strategy.name,[int(x*255) for x in self.color]+[200],SCALE_NAME)
            #strat.position=self.position
            #strat.position.y-=2
            #strat.draw()
            #self._text._label.text=self._get_object().name+"("+self._get_object().strategy.name+")"
            self._text.draw()
            v=VectorSprite(self.position,self.angle)
            v.add_primitives(Primitive2DGL.create_vector(speed*10,get_color_scale(speed/maxPlayerSpeed)))
            v.draw()

class BallSprite(ObjectSprite):
        def __init__(self,obs):
            ObjectSprite.__init__(self,"ball")
            self._obs=obs
            self.add_primitives(Primitive2DGL.create_ball())
        def _get_object(self):
            return self._obs.get_state().ball
        def draw(self):
            ObjectSprite.draw(self)
            speed=self._obs.get_state().ball.speed
            v=VectorSprite(self.position,speed.angle)
            v.add_primitives(Primitive2DGL.create_vector(speed.norm*10,get_color_scale(speed.norm/maxBallAcceleration)))
            v.draw()
class BackgroundSprite(ObjectSprite):
        def __init__(self,obs):
            ObjectSprite.__init__(self,"back",False)
            self.add_primitives(Primitive2DGL.create_field())
            self.add_primitives(Primitive2DGL.create_hud())
def get_color_scale(x):
        return [x,0.,1.-x]


class Hud:
    def __init__(self):
        self.sprites=dict()
        self.sprites["team1"]=TextSprite(color=HUD_TEAM1_COLOR,scale=0.07,position=Vector2D(0,GAME_HEIGHT+6))
        self.sprites["team2"]=TextSprite(color=HUD_TEAM2_COLOR,scale=0.07,position=Vector2D(0,GAME_HEIGHT+2))
        self.sprites["ongoing"]=TextSprite(position=Vector2D(GAME_WIDTH-50,GAME_HEIGHT+7),color=HUD_TEXT_COLOR,scale=0.05)
        self.sprites["ibattle"]=TextSprite(position=Vector2D(GAME_WIDTH-50,GAME_HEIGHT+4),color=HUD_TEXT_COLOR,scale=0.05)
        self.sprites["itour"]=TextSprite(position=Vector2D(GAME_WIDTH-50,GAME_HEIGHT+1),color=HUD_TEXT_COLOR,scale=0.05)
    def set_val(self,**kwargs):
        for k,v in kwargs.items():
            self.sprites[k]._label.text=v

    def draw(self):
        for s in self.sprites.values():
            s.draw()
class PygletAbstractObserver(pyglet.window.Window):

    key_handlers = {
            pyglet.window.key.ESCAPE: lambda w: w.exit(),
            pyglet.window.key.N: lambda w: w.set_ready(),
            pyglet.window.key.M: lambda w: w.switch_manual_step(),
            pyglet.window.key.PLUS: lambda w: w.increase_fps(),
            pyglet.window.key.MINUS: lambda w: w.decrease_fps(),
            pyglet.window.key._0: lambda w: w.switch_hud_names(),
            pyglet.window.key.NUM_ADD : lambda w : w.increase_fps(),
            pyglet.window.key.NUM_SUBTRACT : lambda w: w.decrease_fps()
    }

    def __init__(self,width=1200,height=800):
        pyglet.window.Window.__init__(self,width=width,height=height,resizable=True)
        self.focus()
        self.set_size(width,height)
        self.clear()
        self._is_ready=False
        self._manual_step=False
        self._fps=FPS
        self._soccer_battle=None
        self._tournament=None
        self._nb_tournaments=0
        self.hud=Hud()
        self._hud_names=True
        pyglet.clock.schedule_interval(self.update,1./self._fps)
        self.ongoing=False
        self._list_msg=["Touches :", "p -> jouer", "","m -> switch manuel/auto","n -> avancement manuel",\
                        "+ -> increases fps", "- -> decreases fps","esc -> sortir"]
        self.welcome=self.get_welcome(self._list_msg)
        self._save_fps=0
    def get_welcome(self,list_msg):
        gw=GAME_WIDTH*0.35
        gh=GAME_HEIGHT*0.8
        res=[]
        for x in list_msg:
            res.append(TextSprite(x,color=MSG_TEXT_COLOR,scale=0.08,position=Vector2D(gw,gh)))
            gh-=5
        return res

    def set_soccer_battle(self,battle):
        self._soccer_battle=battle
        battle.obs=self
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
            if self.ongoing:
                #if self.is_ready():
                    if  self.get_state():
                        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
                        self._background.draw()
                        for d in self._sprites.values():
                            d.draw()
            else:
                for d in self.welcome:
                    d.draw()
            self.hud.draw()
        except Exception,e:
            time.sleep(0.0001)
            print e,traceback.print_exc()
    def on_draw(self):
        self.render()

    def on_key_press(self,symbol, modifiers):
        if symbol in self.key_handlers:
            handler = self.key_handlers.get(symbol, lambda w: None)
            handler(self)
            return pyglet.event.EVENT_HANDLED

    def update(self,dt):
        team1=team2=ongoing=ibattle=itour=""
        if self._soccer_battle and self.get_state():
            team1="%s - %s" % (self._soccer_battle.team1.name, self.get_state().score_team1)
            team2="%s - %s" % (self._soccer_battle.team2.name,self.get_state().score_team2)
            ongoing="Round : %d/%d" % (self.get_state().cur_step,self.get_state().max_steps)
            ibattle="Battle : %d/%d" % (self.get_state().cur_battle,self.get_state().battles_count)
        if self._tournament and self._nb_tournaments>0:
            itour="Tournament : %d/%d" %(self._i_tour+1,self._nb_tournaments)
        self.hud.set_val(team1=team1,team2=team2,ongoing=ongoing,ibattle=ibattle,itour=itour)
        if self.ongoing and self._is_ready:
            self._is_ready=False
            self.update_state()
            if not self._manual_step:
                self.set_ready()
    def switch_hud_names(self):
        self._hud_names=not self._hud_names

    def update_state(self):
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
            gl.gluOrtho2D(0, GAME_WIDTH+HUD_WIDTH, 0, GAME_HEIGHT+HUD_HEIGHT)
            gl.glMatrixMode(gl.GL_MODELVIEW)
            gl.glLoadIdentity()
        except Exception:
            time.sleep(0.0001)
            print e,traceback.print_exc()
    def on_close(self):
        res=pyglet.window.Window.on_close(self)
        self.exit()
        return res
    def exit(self):
        self.ongoing=False
        self.set_ready()
        self.close()
        pyglet.app.exit()

    def start_battle(self):
        pass
    def end_battles(self):
        pass
    def begin_battles(self,battles_count,max_steps):
        pass
    def finish_battle(self,win):
        pass
    def set_fps(self):
        pyglet.clock.unschedule(self.update)
        pyglet.clock.schedule_interval(self.update,1./self._fps)

    def increase_fps(self):
        self._fps=min(self._fps+FPS_MOD,300)
        print self._fps
        self.set_fps()
    def decrease_fps(self):
        self._fps=max(self._fps-FPS_MOD,1)
        self.set_fps()

class PygletReplay(PygletAbstractObserver):

    def __init__(self,width=1200,height=800):
        super(PygletReplay,self).__init__(width,height)
        self.key_handlers.update({pyglet.window.key.P: lambda w: w.play(),\
                                  pyglet.window.key.A: lambda w: w.play_prev_tour(),\
                                  pyglet.window.key.Z : lambda w: w.play_next_tour(),\
                                  pyglet.window.key.Q: lambda w: w.play_prev_battle(),\
                                  pyglet.window.key.S: lambda w: w.play_next_battle()})
        self._tournament=None
        self._i_tour=None
        self._list_msg.insert(2,"a -> macth precedent")
        self._list_msg.insert(3,"z -> match suivant")
        self._list_msg.insert(4,"q -> round precedent")
        self._list_msg.insert(5,"s -> round suivant")
        self.welcome=self.get_welcome(self._list_msg)

    def get_state(self):
        if self._soccer_battle and self._soccer_battle.cur_battle<len(self._soccer_battle.battles)\
            and self._soccer_battle.cur_step<len(self._soccer_battle.battles[self._soccer_battle.cur_battle]):
            return self._soccer_battle.battles[self._soccer_battle.cur_battle][self._soccer_battle.cur_step]
        return None
    def play(self):
        if self.ongoing:
            return
        self.ongoing=True
        self.play_round()

    def play_round(self):
        if not self.ongoing:
            return
        if self._i_tour>=len(self._tournament):
            return
        #self.set_soccer_battle(mdpsoccer.SoccerBattle.from_save(self._tournament[self._i_tour]))
        #self.battles=self._tournament[self._i_tour]["battles"]
        self.set_soccer_battle(self._tournament[self._i_tour])
        self._soccer_battle.battles=[ [mdpsoccer.SoccerState.from_blockfile(s) for s in b] for b in self._soccer_battle.battles_block]
        #self._soccer_battle.battles=[[mdpsoccer.SoccerState.from_blockfile()]]
        self.play_battle()

    def play_battle(self):
        if not self.ongoing:
            return
        self._soccer_battle.cur_step=0
        self.set_ready()


    def play_prev_battle(self):
        if not self.ongoing:
            return
        self._is_ready=False
        if self._soccer_battle.cur_battle>0:
            self._soccer_battle.cur_battle-=1
            self.play_battle()
        else:
            self.set_ready()

    def play_next_battle(self):
        if not self.ongoing:
            return
        self._is_ready=False
        if self._soccer_battle.cur_battle<len(self._soccer_battle.battles)-1:
            self._soccer_battle.cur_battle+=1
            self.play_battle()
        else:
            self.play_next_tour()
        #self.set_ready()

    def play_prev_tour(self):
        if not self.ongoing:
            return
        self._is_ready=False
        if self._i_tour>0:
            self._i_tour-=1
            self.play_round()
        else:
            self.set_ready()

    def play_next_tour(self):
        if not self.ongoing:
            return
        self._is_ready=False
        if self._i_tour<(self._nb_tournaments-1):
            self._i_tour+=1
            self.play_round()
        else:
            self.set_ready()

    def update_state(self):
        if not self.ongoing:
            return55
        if self._soccer_battle.cur_step<len(self._soccer_battle.battles[self._soccer_battle.cur_battle]):
            self._soccer_battle.cur_step+=1
        else:
            self.play_next_battle()

    def load(self,fn):
        #tour=[]
        #with open(fn,"rb") as f:
        #    while 1:
        #        try:
        #            tour.append(pickle.load(f))
        #        except EOFError:
        #            break
        #self._tournament=tour
        self._tournament=LogObserver.read(fn)
        self._nb_tournaments=len(self._tournament)
        self._i_tour=0
        print "Fin Load de %d matchs" %(self._nb_tournaments,)

class PygletObserver(PygletAbstractObserver):

    def __init__(self,width=1200,height=800):
        super(PygletObserver,self).__init__(width,height)
        self.key_press=None
        self.key_handlers.update({pyglet.window.key.P: lambda w: w.start_config()})
    def start_config(self):
        if self._soccer_battle and not self.ongoing:
            self._soccer_battle.run_multiple_battles(father=self)
            self.ongoing=True
            self.set_ready()
    def on_key_press(self,symbol, modifiers):
        if super(PygletObserver,self).on_key_press(symbol,modifiers) != pyglet.event.EVENT_HANDLED:
            k=pyglet.window.key.symbol_string(symbol)
            if modifiers & pyglet.window.key.MOD_SHIFT:
                k=k.capitalize()
            else:
                k=k.lower()
            self.key_press=k
            if self._soccer_battle:
                self._soccer_battle.send_to_strat(self.key_press)
    def get_state(self):
        if self._soccer_battle:
            return self._soccer_battle.state
        return None

    def update_state(self):
        if not self.ongoing:
            return
        self._soccer_battle.update()
        if not self._soccer_battle._ongoing:
            self.end_my_battles()
    def end_my_battles(self):
        self.ongoing=False
        self._soccer_battle=None
    def exit(self):
        self.ongoing=False
        self._soccer_battle=None
        super(PygletObserver,self).exit()


class PygletTournamentObserver(PygletObserver):
    def __init__(self,width=1200,height=800):
        super(PygletTournamentObserver,self).__init__(width,height)
        self.key_handlers[pyglet.window.key.P]= lambda w: w.start_tournament()
        self.key_handlers[pyglet.window.key.ENTER]= lambda w: w.skip_battles()
        self._list_msg.insert(3,"Enter -> round suivant")
        self.welcome=self.get_welcome(self._list_msg)

    def set_tournament(self,tour):
        self._tournament=tour
        self._tournament.obs=self
        self._i_tour=0

    def skip_battles(self):
        if self.ongoing:
            _thread=threading.Thread(target=self._soccer_battle.run_until_end)
            _thread.start()
        else:
            self.start_tournament()
    def start_tournament(self):
        if not self.ongoing:
            self._tournament.play_round()
            self.start_config()
    def on_key_press(self,symbol, modifiers):
        if super(PygletObserver,self).on_key_press(symbol,modifiers) != pyglet.event.EVENT_HANDLED:
            k=pyglet.window.key.symbol_string(symbol)
            if modifiers & pyglet.window.key.MOD_SHIFT:
                k=k.capitalize()
            else:
                k=k.lower()
            self.key_press=k
            if self._soccer_battle:
                self._soccer_battle.send_to_strat(self.key_press)
    def update_state(self):
        if not self.ongoing:
            return
        self._soccer_battle.update()
        self._i_tour=self._tournament._i_tour
        self._nb_tournaments=self._tournament.cur_nb_tour
        if not self._soccer_battle._ongoing:
            self._is_ready=False
            self._tournament._i_tour+=1
            self._soccer_battle=None
            self._tournament.play_round()
            self.ongoing=False
            self.start_config()
        self.ongoing=self._tournament.ongoing

    def exit(self):
        self.ongoing=False
        self._soccer_battle=None
        super(PygletTournamentObserver,self).exit()
