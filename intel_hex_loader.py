import re

class HexLoader(object):
    
    def __init__(self, mem_size_bytes):
        self.words = [0] * (mem_size_bytes / 2)
    
    def load(self, data):
        lines = data.split('\n')
        i = 1
        for line in lines:
            if line.strip() != '':
                if not self.validLine(line):
                    raise ValueError("Line #%s has incorrect format: " % i)
                self.parseLine(line)
            i += 1
    
    def validLine(self, line):
        return True
    
    def parseLine(self, line):
        size = int(line[1:3], 16)
        rtype = int(line[7:9], 16)
        if rtype == 2:
            self.segAddr(line)
        elif rtype == 0:
            self.data(line, size)
    
    def segAddr(self, line):
        self.seg = int(line[9:13], 16) * 16
    
    def data(self, line, bytes):
        addr = int(line[3:7], 16)
        i = 0
        for i in range(bytes / 2):
            offs = 9 + i * 4
            lo = int(line[offs:offs+2], 16)
            hi = int(line[offs+2:offs+4], 16)
            self.words[self.seg + addr / 2 + i] = ((hi << 8) | lo)
    
    def printWords(self, count):
        for i in range(count):
            print "%04X" % self.words[i]

if __name__ == '__main__':
    import sys
    s = sys.stdin.read()
    hl = HexLoader(8192)
    hl.load(s)
    hl.printWords(3)

