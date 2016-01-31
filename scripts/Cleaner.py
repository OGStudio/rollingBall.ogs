
from pymjin2 import *

#_ACTION = "spawn.default.rollDown"

class CleanerImpl(object):
    def __init__(self, c):
        self.c = c
    def __del__(self):
        self.c = None
    def setCatch(self, key, value):
        print "setCatch", key, value
        #self.c.set("$MOVE.$SCENE.$BALL.active", "1")

class Cleaner(object):
    def __init__(self, sceneName, nodeName, env):
        self.c = EnvironmentClient(env, "Cleaner")
        self.impl = CleanerImpl(self.c)
        self.c.setConst("SCENE",   sceneName)
        self.c.setConst("CLEANER", nodeName)
        #self.c.setConst("MOVE",  BALL_ACTION)
        self.c.provide("$CLEANER.$SCENE.$CLEANER.catch", self.impl.setCatch)
        #self.c.listen("$MOVE.$SCENE.$BALL.active", "0", self.impl.onStopped)
    def __del__(self):
        # Tear down.
        self.c.clear()
        # Destroy.
        del self.impl
        del self.c

def SCRIPT_CREATE(sceneName, nodeName, env):
    return Cleaner(sceneName, nodeName, env)

def SCRIPT_DESTROY(instance):
    del instance

