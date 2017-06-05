CC = python3
ID = 804808179
TARBALL = lab3b-$(ID).tar.gz
sources = Makefile lab3b.py README* 


default: lab3b
	@echo "python compiled without errors"

clean: 
	rm -rf lab3b lab3b-804808179.tar.gz

run: default
	./lab3a $1

run_test: default 
	./lab3a trivial.img

dist: default 
	tar -zvcf lab3b-804808179.tar.gz Makefile README lab3b lab3b.py
