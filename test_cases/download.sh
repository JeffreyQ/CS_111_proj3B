#!/bin/bash

for i in {0..22}
do
	wget http://www.cs.pomona.edu/classes/cs134/projects/P3B-test_$i.csv
	wget http://www.cs.pomona.edu/classes/cs134/projects/P3B-test_$i.err
done
