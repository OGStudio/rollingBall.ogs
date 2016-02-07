
from pymjin2 import *

CLEANER_ACTION           = "sequence.default.faceTrack"
CLEANER_ACTION_MPOSITION = "move.default.mPosition"
CLEANER_ACTION_RPOSITION = "rotate.default.rPosition"
CLEANER_ACTION_MRETURN   = "move.default.mReturn"
CLEANER_ACTION_RRETURN   = "rotate.default.rReturn"
CLEANER_POINT_NAME       = "point"

class CleanerImpl(object):
    def __init__(self, c):
        self.c = c
        self.speed = None
        self.initialPos = None
        self.initialRot = None
    def __del__(self):
        self.c = None
    def setup(self):
        p = self.c.get("$MPOSITION.point")
        self.speed = p[0].split(" ")[0]
        self.initialPos = self.c.get("node.$SCENE.$CLEANER.position")[0]
        self.initialPosSplit = self.initialPos.split(" ")
        self.initialRot = self.c.get("node.$SCENE.$CLEANER.rotation")[0]
        value = "{0} {1}".format(self.speed, self.initialPos)
        self.c.set("$MRETURN.point", value)
        value = "{0} {1}".format(self.speed, self.initialRot)
        self.c.set("$RRETURN.point", value)
    def setCatch(self, key, value):
        print "setCatch", key, value
        self.c.setConst("POINT", CLEANER_POINT_NAME + value[0])
        # The first call.
        if (self.speed is None):
            self.setup()
        # Motion.
        pos = self.c.get("node.$SCENE.$POINT.positionAbs")[0]
        dstPos = "{0} {1} {2}".format(self.initialPosSplit[0],
                                      self.initialPosSplit[1],
                                      pos.split(" ")[2])
        value = "{0} {1}".format(self.speed, dstPos)
        self.c.set("$MPOSITION.point", value)
        # Rotation.
        dstRot = self.c.get("node.$SCENE.$POINT.rotationAbs")[0]
        value = "{0} {1}".format(self.speed, dstRot)
        self.c.set("$RPOSITION.point", value)
        # Face the track.
        self.c.set("$FACE.$SCENE.$CLEANER.active", "1")

class Cleaner(object):
    def __init__(self, sceneName, nodeName, env):
        self.c = EnvironmentClient(env, "Cleaner")
        self.impl = CleanerImpl(self.c)
        self.c.setConst("SCENE",     sceneName)
        self.c.setConst("CLEANER",   nodeName)
        self.c.setConst("FACE",      CLEANER_ACTION)
        self.c.setConst("MPOSITION", CLEANER_ACTION_MPOSITION)
        self.c.setConst("RPOSITION", CLEANER_ACTION_RPOSITION)
        self.c.setConst("MRETURN",   CLEANER_ACTION_MRETURN)
        self.c.setConst("RRETURN",   CLEANER_ACTION_RRETURN)
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

