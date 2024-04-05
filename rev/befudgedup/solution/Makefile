prog.befunge: prog.txt
	python3 assembler.py > $@

.PHONY: clean
clean:
	rm prog.befunge

.PHONY: run
run: prog.befunge
	python3 runner.py
