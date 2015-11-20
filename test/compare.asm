.include "m8def.inc"
.org $0

clz
ldi r18, $19
mov r19, r18
again:
cpse r18, r19
rjmp again

ldi r16, $33
cpi r16, $30
in r0, SREG
cpi r16, $32
in r1, SREG
cpi r16, $33
in r2, SREG
cpi r16, $34
in r3, SREG

ldi r16, $CC
ldi r17, $CB
cp r17, r16
in r4, SREG
dec r16
cp r17, r16
in r5, SREG
dec r16
cp r17, r16
in r6, SREG
ldi r16, $50
cp r17, r16
in r7, SREG

