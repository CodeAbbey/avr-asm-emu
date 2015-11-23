.include "m8def.inc"
.org $0

mov r3, r0
mov r4, r0
mov r5, r0
mov r16, r0
mov r17, r0

and r3, r1
in r19, SREG
eor r4, r1
in r20, SREG
or r5, r1
in r21, SREG
andi r16, 0x5A
in r22, SREG
ori r17, 0x5A
in r23, SREG

