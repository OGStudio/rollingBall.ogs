
from pymjin2 import *

CLEANER_ACTION           = "sequence.default.faceTrack"
CLEANER_ACTION_MPOSITION = "move.default.mPosition"
CLEANER_ACTION_RPOSITION = "rotate.default.rPosition"
CLEANER_ACTION_MRETURN   = "move.default.mReturn"
CLEANER_ACTION_RRETURN   = "rotate.default.rReturn"
CLEANER_ACTION_PICK      = "delay.default.waitForBall"
CLEANER_POINT_NAME       = "point"
CLEANER_SOUND_MOVE       = "soundBuffer.default.drill"
CLEANER_SOUND_TAKE       = "soundBuffer.default.cleaner"

class CleanerImpl(object):
    def __init__(self, c):
        self.c = c
        self.speed = None
        self.initialPos = None
        self.initialRot = None
        self.trackPartID = None
    def __del__(self):
        self.c = None
    def onMotion(self, key, value):
        val = "play" if value[0] == "1" else "stop"
        self.c.set("$MOTIONSOUND.state", val)
    def onPicking(self, key, value):
        val = ""
        state = "stop"
        if (value[0] == "1"):
            val = self.trackPartID
            state = "play"
        self.c.report("$CLEANER.$SCENE.$CLEANER.picking", val)
        self.c.set("$TAKINGSOUND.state", state)
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
        self.trackPartID = value[0]
        self.c.setConst("POINT", CLEANER_POINT_NAME + self.trackPartID)
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
        self.c.setConst("SCENE",       sceneName)
        self.c.setConst("CLEANER",     nodeName)
        self.c.setConst("FACE",        CLEANER_ACTION)
        self.c.setConst("MPOSITION",   CLEANER_ACTION_MPOSITION)
        self.c.setConst("RPOSITION",   CLEANER_ACTION_RPOSITION)
        self.c.setConst("MRETURN",     CLEANER_ACTION_MRETURN)
        self.c.setConst("RRETURN",     CLEANER_ACTION_RRETURN)
        self.c.setConst("PICK",        CLEANER_ACTION_PICK)
        self.c.setConst("MOTIONSOUND", CLEANER_SOUND_MOVE)
        self.c.setConst("TAKINGSOUND", CLEANER_SOUND_TAKE)
        self.c.provide("$CLEANER.$SCENE.$CLEANER.catch", self.impl.setCatch)
        self.c.provide("$CLEANER.$SCENE.$CLEANER.picking")
        self.c.listen("$PICK.$SCENE.$CLEANER.active", None, self.impl.onPicking)
        self.c.listen("$MPOSITION.$SCENE.$CLEANER.active", None, self.impl.onMotion)
        self.c.listen("$MRETURN.$SCENE.$CLEANER.active", None, self.impl.onMotion)
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

