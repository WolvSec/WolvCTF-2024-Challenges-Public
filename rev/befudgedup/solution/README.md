# befudged up

befunge rev :P

i'm sorry

## the machine

register machine using stack

instructions:

loc:
add r r r
sub r r r
mul r r r
div r r r
mod r r r
mov r imm
push r
pop r
jeq r r loc
jle r r loc
jmp loc
call loc
ret
hlt

read_in r
write_out r

program layout:

program prelude
```
      xP
123456789

vRRRRRRRR
>>>>>>>v
>>v
```

every instruction is 5 high

column 1: entry to arbitrary PC jump logic
column 2, 3, 4: arbitrary PC jump logic: go down from top and go right if 
column 5: blank
column 6 - x: used for given PC jump
column x+1: previous PC entry
column x+2 - ...: instruction
```
      xPI
123456789abcdef0123456789

^ 1   
^ -#        <  arbitrary jump
^ :   ^     <  normal jump
^v_$>> >(instr)  v
^>v    v<<<<<<<<<<
```

