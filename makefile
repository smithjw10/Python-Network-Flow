copyfiles:
	cp $(filepath) .

compile:
	@echo 'Python solution. Nothing to compile.'

run:
	python3 soccer-elimination.py $(input) $(output)

list:
	ls *.py

show:
	@echo 'Showing python file soccer-elimination.py'
	cat soccer-elimination.py
