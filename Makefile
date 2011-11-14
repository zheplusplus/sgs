ifndef PYTHON
	PYTHON=python
endif

check:
	$(PYTHON) test.py

clean:
	find | grep pyc | awk '{ print "rm", $$1 }' | sh


