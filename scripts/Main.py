
from pymjin2 import *

MAIN_BALL_NAME      = "ball"
MAIN_CLEANER_NAME   = "cleaner"
MAIN_TRACK_PARTS_NB = 8
MAIN_PLAIN_NAME     = "plain"
MAIN_CATCH_NAME     = "catch"

class MainImpl(object):
    def __init__(self, c):
        self.c = c
        self.trackPartID = 0
        self.ballInitialPos = None
    def __del__(self):
        self.c = None
    def onBallStopped(self, key, value):
        self.trackPartID = self.trackPartID + 1
        if (self.trackPartID == MAIN_TRACK_PARTS_NB):
            self.trackPartID = 0
        self.c.set("node.$SCENE.$BALL.parent",
                   MAIN_PLAIN_NAME + str(self.trackPartID))
        self.c.set("node.$SCENE.$BALL.position", self.ballInitialPos)
        self.rollBall()
    def onCatch(self, key, value):
        print "onCatch", key, value
        nodeName = key[2]
        v = nodeName.split(MAIN_CATCH_NAME)
        if (len(v) == 2):
            self.c.set("$CLEANER.$SCENE.$CLEANER.catch", v[1])
    def onGameStart(self, key, value):
        print "Game started", key, value
        self.ballInitialPos = self.c.get("node.$SCENE.$BALL.position")[0]
        self.rollBall()
    def rollBall(self):
        self.c.set("ball.$SCENE.$BALL.moving", "1")

class Main(object):
    def __init__(self, sceneName, nodeName, env):
        self.c = EnvironmentClient(env, "Main")
        self.impl = MainImpl(self.c)
        self.c.setConst("SCENE",    sceneName)
        self.c.setConst("BALL",     MAIN_BALL_NAME)
        self.c.setConst("CLEANER",  MAIN_CLEANER_NAME)
        self.c.listen("input.SPACE.key", "1", self.impl.onGameStart)
        self.c.listen("$BALL.$SCENE.$BALL.moving", "0", self.impl.onBallStopped)
        self.c.listen("node.$SCENE..selected", "1", self.impl.onCatch)
    def __del__(self):
        # Tear down.
        self.c.clear()
        # Destroy.
        del self.impl
        del self.c

def SCRIPT_CREATE(sceneName, nodeName, env):
    return Main(sceneName, nodeName, env)

def SCRIPT_DESTROY(instance):
    del instance

