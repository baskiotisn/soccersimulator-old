# -*- coding: utf-8 -*-<
import signal
import math
import string
import random

valid_chars = frozenset("%s%s%s" % (string.ascii_letters, string.digits, "_"))


def clean_fn(fn):
    return ''.join(c if c in valid_chars else '' for c in fn)


class DecodeException(Exception): pass

class Savable(object):
    def save(self, filename):
        with open(filename, "w") as f:
            f.write(self.to_str())\

    @classmethod
    def load(cls, filename):
        res = None
        with open(filename, "r") as f:
            res = cls.from_str(f.read())
        return res

    def __repr__(self):
        return str(self.__class__).split(".")[-1]+": "+self.__str__()

    def to_str(self):
        pass



class Vector2D(Savable):
    """ Vecteur 2D : peut etre creer soit par ses coordonnees (x,y) soit par ses coordonnees polaire
    angle et norme.
    """

    def __init__(self, x=0., y=0., angle=None, norm=None):
        """ create a vector
        :param x: 1ere coordonnee
        :param y: 2nd coordonnee
        :param angle: angle en radian
        ;param norm: norme du vecteur
        """
        if angle is not None and norm is not None:
            self._x = math.cos(angle) * norm
            self._y = math.sin(angle) * norm
            return
        self._x = float(x)
        self._y = float(y)

    @property
    def x(self):
        """
        1ere coordonnee
        """
        return self._x

    @x.setter
    def x(self, value):
        self._x = float(value)

    @property
    def y(self):
        """
        2nd coordonnee
        """
        return self._y

    @y.setter
    def y(self, value):
        self._y = float(value)

    @property
    def norm(self):
        """
        norme du vecteur
        :return : la norme
        """
        return math.sqrt(self.dot(self))

    @norm.setter
    def norm(self, n):
        if self.norm == 0:
            return
        self.normalize()
        self *= n

    @property
    def angle(self):
        """
        angle du vector
        """
        return math.atan2(self.y, self.x)

    @angle.setter
    def angle(self, a):
        n = self.norm
        self.x = math.cos(a) * n
        self.y = math.sin(a) * n

    def set(self, v):
        """ Fixe la valeur du vecteur
        :param v: Vecteur
        :return:
        """
        self.x = v.x
        self.y = v.y
        return self

    def random(self, low=0., high=1.):
        """
        Randomize the vector
        :param float low: low limit
        :param float high: high limit
        """
        self.x = random.random() * (high - low) + low
        self.y = random.random() * (high - low) + low
        return self

    def distance(self, v):
        """ distance au vecteur
        :param v: vecteur
        ;return : distance
        """
        return (v - self).norm

    def dot(self, v):
        """ produit scalaire
            ;param v: vecteur
        """
        return self.x * v.x + self.y * v.y

    def normalize(self):
        """
        Normalise le vecteur
        """
        n = self.norm
        if n != 0:
            self *= 1. / n
        return self

    def scale(self, a):
        """
        Multiplie par a le vecteur
        :param float a: facteur
        """
        self.x *= a
        self.y *= a
        return self

    def norm_max(self, n):
        """ Normallise le vecteur a la norme n si supéroeir
        :param n:
        :return: vecteur normalise
        """
        n_old = self.norm
        if n_old == 0:
            return Vector2D()
        if n_old <= n:
            return self.copy()
        return self * n / n_old

    def copy(self):
        """ operateur de copie
        """
        return Vector2D(self.x, self.y)

    @classmethod
    def from_polar(cls, angle, norm):
        """
        Cree le vecteur a partir des coordonnees polaires
        :param float angle: angle
        :param float norm: norme
        :return: vecteur
        """
        return cls(angle=angle, norm=norm)

    @classmethod
    def create_random(cls, low=0, high=1.):
        """
        Cree un vecteur aleatoire entre lov et high
        :param float low: valeur minimale
        :param float high: valeur maximale exclue
        :return: vecteur
        """
        res = cls()
        res.random(low, high)
        return res

    @classmethod
    def from_str(cls, strg):
        """ Cree un vecteur a partir de la representation texte (x,y)
        :param strg: representation texte
        :return: vecteur
        """
        l_pos = strg.split(",")
        if len(l_pos) != 2 or l_pos[0][0] != "(" or l_pos[1][-1] != ")":
            raise DecodeException("Wrong format for %s : %s", (cls, strg))
        return cls(float(l_pos[0][1:]), float(l_pos[1][:-1]))

    @classmethod
    def from_list_str(cls, strg):
        """ Cree une liste de vecteur a partir de la representation texte (x1,y1)(x2,y2)...
        :param strg: representation texte
        :return: vecteur
        """
        res = []
        idx = 0
        nidx = strg.find(")", idx)
        while nidx != -1:
            res.append(cls.from_str(strg[idx:(nidx + 1)]))
            idx = nidx + 1
            nidx = strg.find(")", idx)
        return res

    def to_str(self):
        return "(%f,%f)" % (self.x, self.y)

    def __str__(self):
        return "(%f,%f)" % (self.x, self.y)


    def __eq__(self, other):
        return (other.x == self.x) and (other.y == self.y)

    def __add__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        return Vector2D(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y)
        return Vector2D(self.x - other, self.y - other)

    def __iadd__(self, other):
        if isinstance(other, Vector2D):
            self.x += other.x
            self.y += other.y
        else:
            self.x += other
            self.y += other
        return self

    def __isub__(self, other):
        if isinstance(other, Vector2D):
            self.x -= other.x
            self.y -= other.y
        else:
            self.x -= other
            self.y -= other
        return self

    def __imul__(self, other):
        if isinstance(other, Vector2D):
            self.x *= other.x
            self.y *= other.y
        else:
            self.x *= other
            self.y *= other
        return self

    def __mul__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x * other.x, self.y * other.y)
        return Vector2D(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __idiv__(self, other):
        if isinstance(other, Vector2D):
            self.x /= other.x
            self.y /= other.y
        else:
            self.x /= other
            self.y /= other
        return self

    def __div__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x / other.x, self.y / other.y)
        return Vector2D(self.x / other, self.y / other)


class MobileMixin(object):
    """ Mixin pour représenter un objet mobile. Dispose d'un vecteur position et d'un vecteur vitesse.
    """

    def __init__(self, position=None, vitesse=None, *args, **kwargs):
        """
        :param position: position du mobile (Vector2D)
        :param vitesse: vitesse du mobile (Vector2D)
        :return:
        """
        if position is None:
            position = Vector2D()
        if vitesse is None:
            vitesse = Vector2D()
        self._position = position
        self._vitesse = vitesse

    @property
    def vitesse(self):
        return self._vitesse

    @vitesse.setter
    def vitesse(self, v):
        self._vitesse.set(v)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, v):
        self._position.set(v)

    @classmethod
    def from_position(cls, x, y):
        """ Construit a partir de deux reels (x,y)
        :param x:
        :param y:
        :return:
        """
        return cls(position=Vector2D(x, y))

    def to_str(self):
        """
        :return: representation texte du mobile
        """
        return self.__str__()

    @classmethod
    def from_str(cls, strg):
        """ Construit le mobile a partir de la description texte
        :param strg:
        :return:
        """
        tmp = Vector2D.from_list_str(strg)
        return cls(tmp[0], tmp[1])

    def __str__(self):
        return "%s%s" % (self.position, self.vitesse)

    def __repr__(self):
        return self.__str__()


class Events(object):
    def __init__(self):
        for e in self.__events__:
            self.__getattr__(e)

    def __getattr__(self, name):
        if hasattr(self.__class__, '__events__'):
            assert name in self.__class__.__events__, \
                "Event '%s' is not declared" % name
        self.__dict__[name] = ev = _EventSlot(name)
        return ev

    def __str__(self):
        return 'Events :' + str(list(self))

    __repr__ = __str__

    def __len__(self):
        if len(self.__dict__) != 0:
            return len(self.__dict__.values()[0])
        return 0

    def __iter__(self):
        def gen(dictitems=self.__dict__.items()):
            for attr, val in dictitems:
                if isinstance(val, _EventSlot):
                    yield val

        return gen()

class _EventSlot(object):
    def __init__(self, name):
        self.targets = []
        self.__name__ = name

    def __repr__(self):
        return self.__name__

    def __call__(self, *a, **kw):
        return [f(*a, **kw) for f in self.targets]

    def __iadd__(self, f):
        self.targets.append(f)
        return self

    def __isub__(self, f):
        while f in self.targets: self.targets.remove(f)
        return self

    def __len__(self):
        return len(self.targets)


class SoccerEvents(Events):
    __events__ = ('begin_match', 'begin_round', 'update_round', 'end_round', 'end_match', 'is_ready')
    def __iadd__(self, f):
        for e in self:
            try:
                e += getattr(f, str(e))
            except:
                pass
        return self

    def __isub__(self, f):
        for e in self:
            try:
                while getattr(f, str(e)) in e.targets: e.targets.remove(getattr(f, str(e)))
            except:
                pass
        return self
#
# def deadline(timeout, *args):
#     p =  None
#     def decorate(f):
#         def new_f(*args):
#             def handler(pr):
#                 print "handled"
#                 pr.terminate()
#             def run(r):
#                 r.put(f(*args))
#                 print("here %d" %(r.qsize(),))
#             result = multiprocessing.Queue()
#             p = multiprocessing.Process(target = run,args=(result,))
#             tmer = threading.Timer(timeout,lambda : handler(p))
#             p.start()
#             print("here5")
#             p.join()
#             tmer.cancel()
#             print "timed out %d" %(result.qsize(),)
#             if result.qsize()>0:
#                 return result.get()
#             return None
#         new_f.__name__ = f.__name__
#         return new_f
#     return decorate