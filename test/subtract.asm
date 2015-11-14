.org $0
.include "m8def.inc"

mov r16, r0
mov r17, r1

sub r0, r2
in r4, SREG
sbc r1, r3
in r5, SREG

subi r16, 5
in r8, SREG
sbci r17, 3
in r9, SREG

