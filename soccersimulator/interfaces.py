# -*- coding: utf-8 -*-
import pyglet
# pyglet.options["debug_gl"]=True
# pyglet.options["debug_trace"]=True
# pyglet.options["debug_gl_trace"]=True

import math
from pyglet import gl
import time
import traceback
import settings
from utils import Vector2D, MobileMixin
from mdpsoccer import Score, SoccerMatch


TEAM1_COLOR = [0.9, 0.1, 0.1]
TEAM2_COLOR = [0.1, 0.1, 0.9]
FIELD_COLOR = [0.3, 0.9, 0.3]
BALL_COLOR = [0.8, 0.8, 0.2]
LINE_COLOR = [1., 1., 1.]
BG_COLOR = [0., 0., 0.]
GOAL_COLOR = [0.2, 0.2, 0.2]
SCALE_NAME = 0.05
HUD_HEIGHT = 10
HUD_WIDTH = 0
HUD_BKG_COLOR = [0.3, 0.3, 0.3]
HUD_TEAM1_COLOR = [int(x * 255) for x in TEAM1_COLOR] + [200]
HUD_TEAM2_COLOR = [int(x * 255) for x in TEAM2_COLOR] + [200]
HUD_TEXT_COLOR = [0, 200, 0, 255]
MSG_TEXT_COLOR = [200, 200, 200, 255]
PANEL_WIDTH = 40
PANEL_BKG_COLOR = [1, 1, 1]
PANEL_TXT_COLOR = [10, 10, 10, 200]
PANEL_SCORE_COLOR = [200, 10, 10, 100]
PANEL_DELTA = 6
FPS = 30.
FPS_MOD = 5.


def minmax(x, mi=0, ma=1):
    return max(mi, min(ma, x))


def get_color_scale(x):
    return [minmax(x), 0., minmax(1. - x)]


def col2rgb(color):
    return [int(minmax(x * 255, 0, 255)) for x in color]


class ObjectSprite:
    def __init__(self, items=None):
        self.primitives = []
        self._info = MobileMixin()
        if items:
            self.add_primitives(items)

    def add_primitives(self, items):
        for item in items:
            self.primitives.append(item)

    @property
    def vitesse(self):
        return self._info.vitesse

    @vitesse.setter
    def vitesse(self, v):
        self._info.vitesse = v

    @property
    def position(self):
        return self._info.position

    @position.setter
    def position(self, v):
        self._info.position = v

    def draw(self):
        try:
            gl.glPushMatrix()
            gl.glTranslatef(self.position.x, self.position.y, 0)
            gl.glRotatef(self.vitesse.angle * 180. / math.pi, 0, 0, 1)
            vec_prim = []
            if self.vitesse.norm != 0:
                vec_prim = Primitive2DGL.create_vector(self.vitesse.norm * 10, get_color_scale(
                        self.vitesse.norm / settings.maxBallAcceleration))
            for p in self.primitives + vec_prim:
                gl.glColor3f(*p.color)
                gl.glBegin(p.primtype)
                for vert in p.verts:
                    gl.glVertex2f(*vert)
                gl.glEnd()
        except Exception, e:
            time.sleep(0.0001)
            print(e, traceback.print_exc())
        finally:
            gl.glPopMatrix()


class Primitive2DGL(object):
    @staticmethod
    def create_circle(radius, color=None, prct=1., angle=0.):
        if not color:
            color = [1, 1, 1]
        steps = int(10 * radius * math.pi * prct)
        s = math.sin(2 * math.pi / steps)
        c = math.cos(2 * math.pi / steps)
        dx, dy = math.cos(angle) * radius, math.sin(angle) * radius
        res = [(0., 0.)]
        for i in range(steps):
            res.append((dx, dy))
            dx, dy = (dx * c - dy * s), (dy * c + dx * s)
        return [Primitive2DGL(res, color)]

    @staticmethod
    def create_vector(length, color=None):
        if not color:
            color = [1, 1, 1]
        primtype = gl.GL_LINES
        verts = [(0, 0), (length, 0), (length, 0), (length * 0.9, 0.1 * length), (length, 0),
                 (length * 0.9, -0.1 * length)]
        return [Primitive2DGL(verts, color, primtype)]

    @staticmethod
    def create_player(color):
        rad = settings.PLAYER_RADIUS
        eps = 0.3 * rad
        corps = Primitive2DGL([(-rad, -rad), (-rad, rad),
                               (rad - eps, rad), (rad - eps, -rad)], color)
        front = Primitive2DGL([(rad - eps, rad * 0.85), (rad, 0), (rad - eps, -rad * 0.85)], color)
        return [corps, front]

    @staticmethod
    def create_ball():
        rad = settings.BALL_RADIUS
        return Primitive2DGL.create_circle(rad, BALL_COLOR)

    @staticmethod
    def create_field():
        field = Primitive2DGL([(0, 0), (0, settings.GAME_HEIGHT),
                               (settings.GAME_WIDTH, settings.GAME_HEIGHT),
                               (settings.GAME_WIDTH, 0)], FIELD_COLOR)
        bandes_1 = Primitive2DGL([(0, 0), (settings.GAME_WIDTH, 0),
                                  (settings.GAME_WIDTH, settings.GAME_HEIGHT),
                                  (0, settings.GAME_HEIGHT), (0, 0)], LINE_COLOR, gl.GL_LINE_STRIP)
        bandes_2 = Primitive2DGL([(settings.GAME_WIDTH / 2, settings.GAME_HEIGHT),
                                  (settings.GAME_WIDTH / 2, 0)], LINE_COLOR, gl.GL_LINE_STRIP)
        y1 = (settings.GAME_HEIGHT - settings.GAME_GOAL_HEIGHT) / 2
        y2 = (settings.GAME_HEIGHT + settings.GAME_GOAL_HEIGHT) / 2
        xend = settings.GAME_WIDTH
        goals_1 = Primitive2DGL([(0, y1), (0, y2), (2, y2), (2, y1)], GOAL_COLOR)
        goals_2 = Primitive2DGL([(xend, y2), (xend, y1), (xend - 2, y1), (xend - 2, y2)], GOAL_COLOR)
        return [field, bandes_1, bandes_2, goals_1, goals_2]

    @staticmethod
    def create_hud():
        hud = Primitive2DGL([(0, settings.GAME_HEIGHT), (0, settings.GAME_HEIGHT + HUD_HEIGHT),
                             (settings.GAME_WIDTH + PANEL_WIDTH, settings.GAME_HEIGHT + HUD_HEIGHT),
                             (settings.GAME_WIDTH + PANEL_WIDTH, settings.GAME_HEIGHT)], HUD_BKG_COLOR)
        return [hud]

    @staticmethod
    def create_panel():
        panel = Primitive2DGL(
                [(settings.GAME_WIDTH, settings.GAME_HEIGHT + HUD_HEIGHT), (settings.GAME_WIDTH + PANEL_WIDTH,
                                                                            settings.GAME_HEIGHT + HUD_HEIGHT),
                 (settings.GAME_WIDTH + PANEL_WIDTH, 0), (settings.GAME_WIDTH, 0)], PANEL_BKG_COLOR)
        return [panel]

    def __init__(self, verts, color, primtype=gl.GL_TRIANGLE_FAN):
        self.verts = verts
        self.color = color
        self.primtype = primtype

    def offset(self, dx, dy):
        self.verts = [(v[0] + dx, v[1] + dy) for v in self.verts]
        return self


class TextSprite:
    def __init__(self, text="", position=None, color=None, scale=0.1):
        if not position:
            position = Vector2D()
        if not color:
            color = [255, 255, 255, 255]
        try:
            self._label = pyglet.text.Label(text, color=color, font_name="Arial", font_size=40)
        except Exception, e:
            print(e, traceback.print_exc())
        self.scale = scale
        self.position = position
        self._ready = True

    def draw(self):
        try:
            gl.glPushMatrix()
            gl.glLoadIdentity()
            gl.glTranslatef(self.position.x, self.position.y, 0)
            gl.glScalef(self.scale, self.scale, 1)
            self._label.draw()
        except Exception, e:
            print(e, traceback.print_exc())
            time.sleep(0.0001)
            raise e
        finally:
            gl.glPopMatrix()


class PlayerSprite(ObjectSprite):
    def __init__(self, name, color):
        ObjectSprite.__init__(self)
        self.name = name
        self.color = color
        self.add_primitives(Primitive2DGL.create_player(self.color))
        self.text = TextSprite(self.name, color=col2rgb(self.color) + [200], scale=SCALE_NAME)

    def draw(self):
        self.text.position = self.position
        ObjectSprite.draw(self)
        self.text.draw()


class BallSprite(ObjectSprite):
    def __init__(self):
        ObjectSprite.__init__(self)
        self.add_primitives(Primitive2DGL.create_ball())


class BackgroundSprite(ObjectSprite):
    def __init__(self):
        ObjectSprite.__init__(self)
        self.add_primitives(Primitive2DGL.create_field())
        self.add_primitives(Primitive2DGL.create_hud())
        self.add_primitives(Primitive2DGL.create_panel())

class Hud:
    def __init__(self):
        self.sprites = dict()
        self.sprites["team1"] = TextSprite(color=HUD_TEAM1_COLOR, scale=0.07,
                                           position=Vector2D(0, settings.GAME_HEIGHT + 6))
        self.sprites["team2"] = TextSprite(color=HUD_TEAM2_COLOR, scale=0.07,
                                           position=Vector2D(0, settings.GAME_HEIGHT + 2))
        self.sprites["ongoing"] = TextSprite(position=Vector2D(settings.GAME_WIDTH - 50, settings.GAME_HEIGHT + 7),
                                             color=HUD_TEXT_COLOR,
                                             scale=0.05)
        self.sprites["ibattle"] = TextSprite(position=Vector2D(settings.GAME_WIDTH - 50, settings.GAME_HEIGHT + 4),
                                             color=HUD_TEXT_COLOR,
                                             scale=0.05)
        self.sprites["itour"] = TextSprite(position=Vector2D(settings.GAME_WIDTH - 50, settings.GAME_HEIGHT + 1),
                                           color=HUD_TEXT_COLOR,
                                           scale=0.05)

    def set_val(self, **kwargs):
        for k, v in kwargs.items():
            self.sprites[k]._label.text = v

    def draw(self):
        for s in self.sprites.values():
            s.draw()


class Panel:
    def __init__(self):
        self.scale = 0.055
        self._is_ready = True
        self.sprites = []

    def from_list(self, l):
        self._is_ready = False
        delta = -PANEL_DELTA
        self.sprites = []
        for i, s in enumerate(l):
            t1 = TextSprite("%d - %s" % (i + 1, s[1]), color=PANEL_TXT_COLOR, scale=self.scale,
                            position=Vector2D(settings.GAME_WIDTH,
                                              settings.GAME_HEIGHT + HUD_HEIGHT + delta))
            t2 = TextSprite(s[2], color=PANEL_SCORE_COLOR, scale=self.scale, position=Vector2D(settings.GAME_WIDTH
                                                                                               + PANEL_WIDTH * 1 / 4.,
                                                                                               settings.GAME_HEIGHT + HUD_HEIGHT + delta - PANEL_DELTA / 2.))
            self.sprites.append([t1, t2])
            delta -= PANEL_DELTA
            self._is_ready = True

    def draw(self):
        if self._is_ready:
            for s in self.sprites:
                s[0].draw()
                s[1].draw()

class MatchWindow(pyglet.window.Window):
    key_handlers = {
        pyglet.window.key.ESCAPE: lambda w: w.exit(),
        pyglet.window.key.P: lambda w: w.play(),
        pyglet.window.key.PLUS: lambda w: w._increase_fps(),
        pyglet.window.key.MINUS: lambda w: w._decrease_fps(),
        pyglet.window.key.NUM_0: lambda w: w._switch_hud_names(),
        pyglet.window.key.L: lambda w: w._switch_hud_names(),
        pyglet.window.key.NUM_ADD: lambda w: w._increase_fps(),
        pyglet.window.key.NUM_SUBTRACT: lambda w: w._decrease_fps(),
        pyglet.window.key.NUM_9: lambda w: w._switch_speed(),
        pyglet.window.key.O: lambda w: w._switch_speed(),
        pyglet.window.key.N: lambda w: w._switch_manual_step_flag(),
        pyglet.window.key.M: lambda w: w._switch_manual_step()
    }
    list_msg = ["Touches :", "p -> jouer", "", "m -> switch manuel/auto", "n -> avancement manuel",
                "+ -> increases fps", "- -> decreases fps", "esc -> sortir"]

    def __init__(self, width=1200, height=800):
        pyglet.window.Window.__init__(self, width=width, height=height, resizable=True)
        self.set_size(width, height)
        self.hud = Hud()
        self.panel = Panel()
        self.focus()
        self.clear()
        self._fps = FPS
        self._hud_names = True
        self._sprites = dict()
        self._background = BackgroundSprite()
        self._state = None
        self._match=None
        self._manual_step=False
        self._create_draw = True
        self._to_update = True
        self._speed = False
        self._tournament = None
        self.scores = dict()
        self._rebuild_panel = False
        self._kill = False
        self._manual_step_flag = False
        pyglet.clock.schedule_interval(self.update, 1. / 25)

    def set(self, match, run=True):
        if hasattr(match, "nb_matches"):
            self._tournament = match
            self._tournament._listeners += self
            self._match = None
        else:
            self._match = match
            self._match._listeners += self
            self._create_draw = True
        if run:
            pyg_start()

    def update(self, dt=None):
        self.render()

    def get_welcome(self):
        gw = settings.GAME_WIDTH * 0.35
        gh = settings.GAME_HEIGHT * 0.8
        res = []
        for x in self.list_msg:
            res.append(TextSprite(x, color=MSG_TEXT_COLOR, scale=0.08, position=Vector2D(gw, gh)))
            gh -= 5
        return res

    def play(self):
        if self._tournament:
            self._tournament.play(False)
            return
        if self._match:
            self._match.play(False)
            return

    @property
    def state(self):
        return self._state

    def create_drawable_objects(self):
        if not self.state:
            return
        self._create_draw = False
        self.focus()
        self._sprites = dict()
        self._sprites["ball"] = BallSprite()
        for k, v in self.state.players:
            if not self.get_team(k):
                name_p = '%d %d|' % (k, v)
            else:
                name_p = self.get_team(k).player_name(v)
            self._sprites[(k, v)] = PlayerSprite(name_p, color=TEAM1_COLOR if k == 1 else TEAM2_COLOR)

    def render(self):
        try:
            if self._kill:
                pyg_stop()
                return
            if self.state:
                if self._create_draw:
                    self.create_drawable_objects()
                if self._to_update:
                    self._update_sprites()
                if self._rebuild_panel:
                    self.panel.from_list(
                            sorted([(score.points, k[0], score.str_nocolor()) for k, score in self.scores.items()],
                                   reverse=True))

                gl.glClear(gl.GL_COLOR_BUFFER_BIT)
                self._background.draw()
                for d in self._sprites.values():
                    d.draw()
                self.hud.draw()
                self.panel.draw()
                return True
            else:
                for d in self.get_welcome():
                    d.draw()
            return True
        except Exception, e:
            time.sleep(0.0001)
            print(e, traceback.print_exc())
            raise e
        return False

    def _update_sprites(self):
        team1 = team2 = ongoing = ""
        if self.state:
            team1 = "%s %s - %s" % (self.get_team(1).name,self.get_team(1).login, self.state.score_team1)
            team2 = "%s %s - %s" % (self.get_team(2).name, self.get_team(2).login, self.state.score_team2)
            ongoing = "Round : %d/%d" % (self.state.step, self._match.max_steps)
            self.hud.set_val(team1=team1, team2=team2, ongoing=ongoing)
            for k in self.state.players:
                self._sprites[k].position = self.state.player_state(k[0], k[1]).position
                self._sprites[k].vitesse= self.state.player_state(k[0], k[1]).vitesse
            self._sprites["ball"].position = self.state.ball.position
            self._sprites["ball"].vitesse = self.state.ball.vitesse
        self._to_update = False

    def update_round(self, team1, team2, state):
        self.change_state(state)
        if not self._speed and not self._manual_step:
            time.sleep(1. / self._fps)
        if self._manual_step:
            self._manual_step_flag = True
            while self._manual_step_flag:
                time.sleep(0.0001)

    def change_state(self, state):
        self._state = state.copy()
        self._to_update = True

    def get_team(self, i):
        if self._match:
            return self._match.get_team(i)
        return None

    def _switch_manual_step_flag(self):
        self._manual_step_flag = False

    def _switch_manual_step(self):
        self._manual_step = not self._manual_step
        if not self._manual_step:
            self._switch_manual_step_flag()

    def _switch_hud_names(self):
        self._hud_names = not self._hud_names

    def _switch_speed(self):
        self._speed = not self._speed

    def on_draw(self):
        self.render()

    def on_key_press(self, symbol, modifiers):
        if symbol in self.key_handlers:
            handler = self.key_handlers.get(symbol, lambda w: None)
            handler(self)
            return pyglet.event.EVENT_HANDLED
        if self._match and hasattr(self._match,"send_to_strategies"):
            k=pyglet.window.key.symbol_string(symbol)
            if modifiers & pyglet.window.key.MOD_SHIFT:
                k=k.capitalize()
            else:
                k=k.lower()
            self._match.send_to_strategies(k)
        return pyglet.event.EVENT_UNHANDLED

    def on_resize(self, width, height):
        pyglet.window.Window.on_resize(self, width, height)
        self.focus()
        return pyglet.event.EVENT_HANDLED

    def focus(self):
        try:
            gl.glMatrixMode(gl.GL_PROJECTION)
            gl.glLoadIdentity()
            gl.gluOrtho2D(0, settings.GAME_WIDTH + PANEL_WIDTH, 0, settings.GAME_HEIGHT + HUD_HEIGHT)
            gl.glMatrixMode(gl.GL_MODELVIEW)
            gl.glLoadIdentity()
        except Exception, e:
            time.sleep(0.0001)
            print(e, traceback.print_exc())

    def on_close(self):
        pyglet.window.Window.on_close(self)
        return pyglet.event.EVENT_HANDLED

    def exit(self):
        if hasattr(self._match, "kill"):
            self._match.kill()
        if hasattr(self._tournament, "kill"):
            self._tournament.kill()
        self._kill = True
        pyglet.clock.unschedule(self.update)
        self.close()
        pyg_stop()
        return pyglet.event.EVENT_HANDLED

    def _increase_fps(self):
        self._fps = min(self._fps + FPS_MOD, 200)

    def _decrease_fps(self):
        self._fps = max(self._fps - FPS_MOD, 1)

    def begin_match(self, team1, team2, state):
        if self._tournament:
            self._match = self._tournament.cur_match
        self._create_draw = True
        self.change_state(self._match.state)
        if team1 and team2:
            if (team1.name, team1.login) not in self.scores:
                self.scores[(team1.name, team1.login)] = Score()
            if (team2.name, team2.login) not in self.scores:
                self.scores[(team2.name, team2.login)] = Score()

    def begin_round(self, *args, **kwargs):
        return

    def end_round(self, *args, **kwargs):
        return

    def end_match(self, team1, team2, state, *args, **kwargs):
        if team1 and team2:
            self.scores[(team1.name, team1.login)].add(state.score_team1, state.score_team2)
            self.scores[(team2.name, team2.login)].add(state.score_team2, state.score_team1)
        self._rebuild_panel = True


def pyg_start():
    pyglet.app.run()


def pyg_stop():
    pyglet.app.exit()


def show(match):
    if isinstance(match,list):
        MatchWindow().set(SoccerMatch(states=match))
        return
    MatchWindow().set(match)

