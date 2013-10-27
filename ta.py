class C(object):
    def __init__(self):
        self.x = None
    def getx(self):
        print 'yeay'
        return self.x    
    def setx(self, value):
        self.x = value + 1
    def delx(self):
        del self.x
    x = property(getx, setx, delx, "I'm the 'x' property.")


# func = 'woot'
# locals()[func]()

# a_inst = a()
# func = 'play'
# getattr(a_inst,'t')
# getattr(a_inst,func)()
# getattr(a_inst,'t')
