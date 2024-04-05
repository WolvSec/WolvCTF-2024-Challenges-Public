
prog: prog.o
	ld -o $@ $^

prog.o: prog.asm
	nasm -f elf64 -o $@ $^

.PHONY: clean
clean:
	-rm -f prog
	-rm -f prog.o

