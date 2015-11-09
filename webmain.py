#!/usr/local/bin/python2.7

from intel_hex_loader import HexLoader
from avr_executor import Executor

import sys
import json
import base64
import StringIO

data = sys.stdin.read()
data = json.loads(data)

hl = HexLoader(8192)
hl.load(base64.b64decode(data['code']))
ex = Executor(hl.words)
for i in range(len(data['regs'])):
    ex.regs[i] = data['regs'][i]

ostdout = sys.stdout
mstdout = StringIO.StringIO()
sys.stdout = mstdout
ex.run()
sys.stdout = ostdout

res = {}
res['regs'] = ex.regs
res['stdout'] = base64.b64encode(mstdout.getvalue())

print 'Content-Type: application/json'
print ''
print json.dumps(res)

