from interfaces import PygletObserver,pyglet

def play_battle(battle):
    obs=PygletObserver()
    obs.set_soccer_battle(battle)
    pyglet.app.run()
