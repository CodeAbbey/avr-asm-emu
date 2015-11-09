from intel_hex_loader import HexLoader
from avr_executor import Executor

import sys
s = sys.stdin.read()
hl = HexLoader(8192)
hl.load(s)
ex = Executor(hl.words)
ex.run()
ex.printRegs()

