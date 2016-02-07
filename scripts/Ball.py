
from pymjin2 import *

BALL_ACTION        = "spawn.default.rollDown"
BALL_ACTION_REPORT = "delay.default.ballIsWaiting"

class BallImpl(object):
    def __init__(self, c):
        self.c = c
    def __del__(self):
        self.c = None
    def onReport(self, key, value):
        self.c.report("$BALL.$SCENE.$BALL.waiting", value[0])
    def onStopped(self, key, value):
        self.c.report("$BALL.$SCENE.$BALL.moving", "0")
    def setMoving(self, key, value):
        self.c.set("$MOVE.$SCENE.$BALL.active", value[0])

class Ball(object):
    def __init__(self, sceneName, nodeName, env):
        self.c = EnvironmentClient(env, "Ball")
        self.impl = BallImpl(self.c)
        self.c.setConst("SCENE",  sceneName)
        self.c.setConst("BALL",   nodeName)
        self.c.setConst("MOVE",   BALL_ACTION)
        self.c.setConst("REPORT", BALL_ACTION_REPORT)
        self.c.provide("$BALL.$SCENE.$BALL.moving", self.impl.setMoving)
        self.c.provide("$BALL.$SCENE.$BALL.waiting")
        self.c.listen("$MOVE.$SCENE.$BALL.active", "0", self.impl.onStopped)
        self.c.listen("$REPORT.$SCENE.$BALL.active", None, self.impl.onReport)
    def __del__(self):
        # Tear down.
        self.c.clear()
        # Destroy.
        del self.impl
        del self.c

def SCRIPT_CREATE(sceneName, nodeName, env):
    return Ball(sceneName, nodeName, env)

def SCRIPT_DESTROY(instance):
    del instance

