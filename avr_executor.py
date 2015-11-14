import sys

class Executor(object):
    
    ip = 0
    sp = 0
    flag_t = 0
    flag_h = 0
    flag_s = 0
    flag_v = 0
    flag_n = 0
    flag_z = 0
    flag_c = 0
    
    def __init__(self, code):
        self.peripherals = Peripherals(self)
        self.words = code
        self.regs = [0] * 32
    
    def step(self):
        w = self.words[self.ip]
        w3 = w >> 12
        if w3 == 0b0000:
            self.i_0000(w)
        elif w3 == 0b0001:
            self.i_0001(w)
        elif w3 == 0b0010:
            self.i_0010(w)
        elif (w3 & 0xE) == 0b0100:
            self.i_subi(w)
        elif w3 == 0b1001:
            self.i_1001(w)
        elif w3 == 0b1011:
            self.i_in_out(w)
        elif w3 == 0b1110:
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
    
    def i_0000(self, w):
        w2 = (w >> 8) & 0x0F
        if (w2 >> 2) == 3:
            self.i_add(w)
        elif (w2 >> 2) == 2:
            self.i_sub(w, True)
        
    def i_0001(self, w):
        w2 = (w >> 8) & 0x0F
        if (w2 >> 2) == 3:
            self.i_add(w, True)
        elif (w2 >> 2) == 2:
            self.i_sub(w)
        
    def i_0010(self, w):
        w2 = (w >> 8) & 0x0F
        if (w2 >> 2) == 3:
            self.i_mov(w)
    def i_1001(self, w):
        c, r = self.code7_reg5(w)
        if c == 0x23:
            self.i_inc_dec(r, 1)
        elif c == 0x2A:
            self.i_inc_dec(r, -1)
    
    def i_add(self, w, with_carry = False):
        d, r = self.dest5_src5(w)
        a = self.regs[d]
        b = self.regs[r]
        res = (a + b + (self.flag_c if with_carry else 0)) & 0xFF
        self.set_flags_hvc(a, b, res)
        self.set_flags_nsz(res)
        self.regs[d] = res
    
    def i_sub(self, w, with_carry = False):
        d, r = self.dest5_src5(w)
        self.subtract(d, self.regs[r], with_carry)
    
    def i_subi(self, w, with_carry = False):
        r, k = self.dest4_const(w)
        self.subtract(r, k, with_carry)
    
    def subtract(self, rd, b, with_carry):
        a = self.regs[rd]
        res = (a - b - (self.flag_c if with_carry else 0)) & 0xFF
        self.set_flags_hvc(res, b, a)
        prev_z = self.flag_z
        self.set_flags_nsz(res)
        if with_carry:
            self.flag_z &= prev_z
        self.regs[rd] = res
    
    def i_inc_dec(self, r, k):
        o = self.regs[r]
        v = (o + k) & 0xFF
        self.regs[r] = v
        self.flag_v = 1 if (k == 1 and o == 0x7F) or (k == -1 and o == 0x80) else 0
        self.set_flags_nsz(v)
    
    def i_in_out(self, w):
        d = (w >> 11) & 0x01
        a = ((w >> 5) & 0x30) | (w & 0xF)
        r = (w >> 4) & 0x1F
        if d == 1:
            self.peripherals.write(a, self.regs[r])
        else:
            self.regs[r] = self.peripherals.read(a)
    
    def i_ldi(self, w):
        r, k = self.dest4_const(w)
        self.regs[r] = v
    
    def i_mov(self, w):
        d, r = self.dest5_src5(w)
        self.regs[d] = self.regs[r]
    
    def dest4_const(self, w):
        v = (w & 0xF) | ((w >> 4) & 0xF0)
        r = 16 + ((w >> 4) & 0x0F)
        return (r, v)
    
    def dest5_src5(self, w):
        d = (w >> 4) & 0x1F
        r = ((w >> 5) & 0x10) | (w & 0xF)
        return (d, r)
    
    def code7_reg5(self, w):
        r = (w >> 4) & 0x1F
        c = ((w >> 5) & 0x70) | (w & 0xF)
        return (c, r)
    
    def set_flags_hvc(self, a, b, c):
        a3 = (a >> 3) & 1
        b3 = (b >> 3) & 1
        nr3 = (~c >> 3) & 1
        self.flag_h = (a3 & b3) | (nr3 & a3) | (nr3 & b3)
        a7 = (a >> 7) & 1
        b7 = (b >> 7) & 1
        nc7 = (~c >> 7) & 1
        self.flag_v = 1 if a7 == b7 and a7 != nc7 else 0
        self.flag_c = (a7 & b7) | (nc7 & a7) | (nc7 & b7)
    
    def set_flags_nsz(self, r):
        self.set_flags_ns(r)
        self.flag_z = r == 0
    
    def set_flags_ns(self, r):
        self.flag_n = (r >> 7) & 1
        self.flag_s = self.flag_v ^ self.flag_n

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
        elif port == 0x3F:
            return self.io_sreg()
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
    
    def io_sreg(self):
        ex = self.executor
        res = ex.flag_c
        res |= ex.flag_z << 1
        res |= ex.flag_n << 2
        res |= ex.flag_v << 3
        res |= ex.flag_s << 4
        res |= ex.flag_h << 5
        res |= ex.flag_t << 6
        return res
    
