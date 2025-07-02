copyfiles:
	cp $(filepath) .

compile:
	@echo 'Python solution. Nothing to compile.'

run:
	python3 Tournament-Network-Flow.py $(input) $(output)

list:
	ls *.py

show:
	@echo 'Showing python file Tournament-Network-Flow.py'
	cat Tournament-Network-Flow.py
