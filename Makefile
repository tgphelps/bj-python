
STRATEGY=data/basic-double-split.txt
mypy:
	mypy *.py
test:
	./bj.py --test -n 1 -v -t -s 5 data/house.cfg $(STRATEGY)
play10k:
	./bj.py        -n 10000 -v -t data/house.cfg $(STRATEGY)
	./verify.py
play1m:
	./bj.py        -n 200000 -s 5    data/house.cfg $(STRATEGY)
test1m:
	./bj.py --test -n 200000 -s 5 -t data/house.cfg $(STRATEGY)
hugetest:
	./bj.py --test -n 2000000 -s 5 data/house.cfg $(STRATEGY)
quicktest:
	./bj.py --test -n 20000 -s 5 -t data/house.cfg $(STRATEGY)
play10m:
	./play10m.sh $(STRATEGY)
run:
	./bj.py        -n 100000  -s 5     data/house.cfg data/never-bust.txt
archive:
	cd .. && tar cvzf bj.tar.gz bj
flake8:
	flake8 *.py
testbj:
	./testbj.py
	cp results.db save-results.db
