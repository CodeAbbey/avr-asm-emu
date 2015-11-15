.org $0
.include "m8def.inc"

rjmp main

greeting:
.db "Hi, People!", 13, 10, 0

main:
ldi ZH, HIGH(greeting<<1)
ldi ZL, LOW(greeting<<1)

repeat:
lpm r16, Z+
subi r16, 0
breq finish
out UDR, r16
brne repeat

finish:

