.org $0
.include "m8def.inc"

mov r18, r0

again:
inc r16
dec r0
brne again

repeat:
inc r17
subi r18, 1
brcc repeat
