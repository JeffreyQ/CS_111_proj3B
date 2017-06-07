CC = python
ID = 804808179
TARBALL = lab3b-$(ID).tar.gz
sources = Makefile lab3b README 


default:
	chmod u+x lab3b
	@echo "python compiled without errors"

clean: 
	rm -rf lab3b-804808179.tar.gz

test: 
	./test.sh


dist: default 
	tar -zvcf lab3b-$(ID).tar.gz lab3b.py $(sources)
