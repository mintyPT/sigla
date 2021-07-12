install:
	poetry install

upload:
	poetry publish --username minty

show:
	poetry show -v

test:
	poetry run pytest --cov-config=.coveragerc --cov=sigla -x -s -vv .

main-render:
	poetry run sigla render $(file)

version:
	poetry run sigla version

flake8:
	poetry run flake8 . --max-cognitive-complexity=7

black:
	poetry run black . -l 79

mypy:
	poetry run mypy -p sigla #--disallow-untyped-calls --disallow-untyped-defs

check: black flake8 mypy