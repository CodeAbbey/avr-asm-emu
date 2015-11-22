.include "m8def.inc"
.org $0

mov r1, r0
mov r2, r0
com r0
in r16, SREG
neg r1
in r17, SREG
swap r2

