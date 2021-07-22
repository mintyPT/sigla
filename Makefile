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
	poetry run flake8 . 

black:
	poetry run black . -l 79

isort:
	poetry run isort .

mypy:
	poetry run mypy -p sigla #--disallow-untyped-calls --disallow-untyped-defs

check: black isort test flake8 mypy