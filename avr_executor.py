class Executor(object):
    
    ip = 0
    
    def __init__(self, code):
        self.words = code
        self.regs = [0] * 32
    
    def step(self):
        w = self.words[self.ip]
        w3 = w >> 12
        if w3 == 14:
            self.i_ldi(w)
        if w3 == 2:
            self.i_0010(w)
        self.ip += 1
    
    def run(self):
        while self.words[self.ip] != 0:
            self.step()
    
    def printRegs(self):
        for i in range(0, 16):
            print "%02X" % self.regs[i],
        print
        for i in range(16, 32):
            print "%02X" % self.regs[i],
        print
    
    def i_0010(self, w):
        w2 = (w >> 8) & 0x0F
        if (w2 >> 2) == 3:
            self.i_mov(w)
    
    def i_ldi(self, w):
        v = (w & 0xF) | ((w >> 4) & 0xF0)
        r = 16 + ((w >> 4) & 0x0F)
        self.regs[r] = v
    
    def i_mov(self, w):
        d = (w >> 4) & 0x1F
        r = ((w >> 5) & 0x10) | (w & 0xF)
        self.regs[d] = self.regs[r]

