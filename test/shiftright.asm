.include "m8def.inc"
.org $0

mov r1, r0
mov r2, r0
lsr r0
in r16, SREG
asr r1
in r17, SREG
ror r2
in r18, SREG
