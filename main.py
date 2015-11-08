from intel_hex_loader import HexLoader
from avr_executor import Executor

import sys
s = sys.stdin.read()
hl = HexLoader(8192)
hl.load(s)
for i in range(15):
    print "%04X" % hl.words[i]
ex = Executor(hl.words)
ex.run()
ex.printRegs()

