global _start
section .data

newline_char: db 10
out_stmt: db 'shell go here :)', 10
fail_stmt: db 'failed check :(', 10

section .text
_start:
	mov rax, 1
	mov rdi, 1
	mov rsi, out_stmt
	mov rdx, 17
	syscall
read_bytes:
	sub rsp, 100 ; 100 bytes buffer
	mov rax, 0
	mov rdi, 0	
	mov rsi, rsp
	mov rdx, 100
	syscall

	mov rcx, 0
	mov rbx, 0x050f
	mov rdx, 0x80
	mov rdi, 96
.loop:
	mov rsi, [rsp+rcx] ; load rbp+rcx
	and rsi, 0xffff
	cmp rbx, rsi	; check for 0x0f05 (syscall)
	jz .fail
	inc rcx
	cmp rdi, rcx
	jnz .loop
	mov rcx, 0
	mov rbx, 0x80
	mov rdi, 98
.loop2:
	mov rsi, [rsp+rcx] ; change to one byte register
	and rsi, 0xff
	cmp rbx, rsi	; check for 0x80 (32-bit syscall)
	jz .fail
	inc rcx
	cmp rdi, rcx
	jnz .loop2
	jmp rsp
.fail:
	mov rax, 1
	mov rdi, 1
	mov rsi, fail_stmt
	mov rdx, 16
	syscall
exit:
	mov rax, 60
	xor rdi, rdi
	syscall

