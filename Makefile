lint: 
	pylint .

bandit:
	bandit -r .

coverage:
	python -m unittest discover -s . -p "test_*.py"
	coverage report
	coverage html
