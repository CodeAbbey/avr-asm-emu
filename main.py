from intel_hex_loader import HexLoader
from avr_executor import Executor

import sys

if len(sys.argv) < 2:
    raise Exception('Usage: python main.py <file.hex> [reg0 reg1 ...]')

regs = [int(x) for x in sys.argv[2:]]

with open(sys.argv[1]) as hexfile:
    s = hexfile.read()
hl = HexLoader(8192)
hl.load(s)
ex = Executor(hl.words)
for i in range(len(regs)):
    ex.regs[i] = regs[i]
ex.run()
ex.printRegs()

