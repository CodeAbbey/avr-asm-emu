.include "m8def.inc"
.org $0

; initializing stack to the last RAM address
ldi r16, low(RAMEND)
out spl, R16
ldi r16, high(RAMEND)
out sph, R16

read_next:
in r16, UDR
mov r17, r16
subi r17, ' '
brlo finish
rcall switch_case
out UDR, r16
rjmp read_next

switch_case:
mov r17, r16
subi r17, 'a'
brsh islower
subi r16, -32
ret
islower:
subi r16, 32
ret

finish:
ldi r16, 13
out UDR, r16
ldi r16, 10
out UDR, r16

