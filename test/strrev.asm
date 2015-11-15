.include "m8def.inc"
.org $0

; initializing stack to the last RAM address
ldi r16, low(RAMEND)
out spl, R16
ldi r16, high(RAMEND)
out sph, R16

ldi r18, 0

read_next:
in r16, UDR
mov r17, r16
subi r17, ' '
brlo do_output
push r16
inc r18
rjmp read_next

do_output:
pop r16
out UDR, r16
dec r18
brne do_output

ldi r16, 13
out UDR, r16
ldi r16, 10
out UDR, r16

