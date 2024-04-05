
; me writing this:

;-;

; password?
; - 72964
; cursed calling convention
; return address goes in rax
; parameters go in r10, r11, r12, r13
; save rsp in rbp sometimes

global _start

%macro customcall 1
    call $+5
    pop rax
    add rax, 10
    jmp %1
%endmacro

_start:
    lea r10, [prompt]
    mov r11, 6
    customcall print
    pop rax

    sub rsp, 32
    mov r10, rsp
    mov r11, 25
    customcall read
    pop rax
    
    lea rax, [correct]
    push rax
    push rax
    lea rax, [.continuation]

    mov rbp, rsp
    lea rsp, [key]
    jmp key

.continuation:
    leave
    ret
    
correct:
    lea r10, [correct_msg]
    mov r11, 9
    call $+5
    pop rax
    add rax, 7
    jmp print
    pop rax

    call exit
    
incorrect:
    lea r10, [incorrect_msg]
    mov r11, 9
    mov rax, 1
    mov rdi, 1
    mov rsi, r10
    mov rdx, r11
    syscall
    jmp exit

syscall:
    push rbp
    mov rbp, rsp
    sub rsp, 0x40
    syscall

exit:
    mov rax, 74
    mov rdi, 1
    syscall
    mov rax, 60
    mov rdi, 0
    syscall

print:
    push rax
    mov rax, 1
    mov rdi, 1
    mov rsi, r10
    mov rdx, r11
    syscall
    pop rax
    call rax

read:
    push rax
    mov rax, 0
    mov rdi, 0
    mov rsi, r10
    mov rdx, r11
    syscall
    pop rax
    call rax
    leave
    ret

key:
    mov r14, rax
    mov r8, 0
    mov eax, 0
    lea rbx, [.stuff]
.funny:
    mov ax, 0x3148
    stc
    jmp rbx
.loop:
.stuff:
    mov r9b, al
    movzx r9, r9b
    mov cl, [rsp + r9]
    mov dil, [r8 + r10]
    lea rbx, [rel .continuation]
    lea r9, [rel .funny + 2] 
    jmp r9
.continuation:
    mov dil, [r8 + data]
    cmp cl, dil
    jne incorrect
    test ax, 1
    jz .even
.odd:
    mov bx, ax
    shl ax, 1
    add ax, bx
    inc ax
    inc r8
    cmp r8, 0x18
    jl .loop
    jmp r14
.even:
    shr ax, 1
    inc r8
    cmp r8, 0x18
    jl .loop
    jmp r14

prompt:
db "flag? "
correct_msg:
db "correct!"
db 10
incorrect_msg:
db "wrong :("
db 10

data:
db 0xf2
db 0x0f
db 0x6c
db 0xec
db 0x1a
db 0xe2
db 0x57
db 0x70
db 0x70
db 0x86
db 0xea
db 0xba
db 0xb5
db 0x63
db 0xcf
db 0x8c
db 0xf8
db 0x0b
db 0x6c
db 0xe0
db 0x6e
db 0x15
db 0x53
db 0x45
