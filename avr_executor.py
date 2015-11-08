import sys

class Executor(object):
    
    ip = 0
    sp = 0
    
    def __init__(self, code):
        self.peripherals = Peripherals(self)
        self.words = code
        self.regs = [0] * 32
    
    def step(self):
        w = self.words[self.ip]
        w3 = w >> 12
        if w3 == 0b0010:
            self.i_0010(w)
        if w3 == 0b1011:
            self.i_in_out(w)
        if w3 == 0b1110:
            self.i_ldi(w)
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
        print "ip=%04X, sp=%04X" % (self.ip, self.sp)
    
    def i_0010(self, w):
        w2 = (w >> 8) & 0x0F
        if (w2 >> 2) == 3:
            self.i_mov(w)
    
    def i_in_out(self, w):
        d = (w >> 11) & 0x01
        a = ((w >> 5) & 0x30) | (w & 0xF)
        r = (w >> 4) & 0x1F
        if d == 1:
            self.peripherals.write(a, self.regs[r])
        else:
            self.regs[r] = self.peripherals.read(a)
    
    def i_ldi(self, w):
        v = (w & 0xF) | ((w >> 4) & 0xF0)
        r = 16 + ((w >> 4) & 0x0F)
        self.regs[r] = v
    
    def i_mov(self, w):
        d = (w >> 4) & 0x1F
        r = ((w >> 5) & 0x10) | (w & 0xF)
        self.regs[d] = self.regs[r]

class Peripherals(object):
    
    def __init__(self, executor):
        self.executor = executor
    
    def write(self, port, value):
        if port == 0x0C:
            self.io_udr(value)
        elif port == 0x3D:
            self.io_spl(value)
        elif port == 0x3E:
            self.io_sph(value)
        else:
            raise ValueError('Unsupported IO register for OUT: ' + str(port))
    
    def read(self, port):
        if port == 0x0C:
            return self.io_udr()
        elif port == 0x3D:
            return self.io_spl()
        elif port == 0x3E:
            return self.io_sph()
        else:
            raise ValueError('Unsupported IO register for IN: ' + str(port))
    
    def io_udr(self, value = None):
        if value != None:
            sys.stdout.write(chr(value))
        else:
            ch = sys.stdin.read(1)
            return ord(ch) if len(ch) > 0 else 0
    
    def io_spl(self, value = None):
        ex = self.executor
        if value != None:
            ex.sp = (ex.sp & 0xFF00) | value
        else:
            return ex.sp & 0xFF
    
    def io_sph(self, value = None):
        ex = self.executor
        if value != None:
            ex.sp = (ex.sp & 0xFF) | (value << 8)
        else:
            return (ex.sp >> 8) & 0xFF

