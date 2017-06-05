#!/bin/bash

echo "BEGIN MY CODE"

for i in {0..22}
do
	echo ".csv #$i"
	python lab3b.py test_cases/P3B-test_$i.csv
	echo ".err #$i"
	cat test_cases/P3B-test_$i.err
done
