run:
	python -m app.main

format:
	ruff format .

lint:
	mypy .
