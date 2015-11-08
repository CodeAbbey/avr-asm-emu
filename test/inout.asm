.include "m8def.inc"
.org $0

; initializing stack to the last RAM address
ldi r16, low(RAMEND)
out spl, R16
ldi r16, high(RAMEND)
out sph, R16

; output few bytes to UART
ldi r16, 'H'
out UDR, r16
ldi r16, 'i'
out UDR, r16
ldi r16, '!'
out UDR, r16
ldi r16, 13
out UDR, r16
ldi r16, 10
out UDR, r16

