CC = python3
ID = 804808179
TARBALL = lab3b-$(ID).tar.gz
sources = Makefile lab3b.py README 


default: lab3b
	@echo "python compiled without errors"

run: lab3b

lab3b:
	$(CC) lab3b.py $4

clean: 
	rm -rf lab3b lab3b-804808179.tar.gz

test: 
	./test.sh


dist: default 
	tar -zvcf lab3b-$(ID).tar.gz lab3b.py $(sources)
