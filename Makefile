install:
	poetry install

publish:
	poetry version patch
	poetry version | cut -d" " -f2
	version=$(shell poetry version | cut -d" " -f2)
	read -p "Update the version on sigla/__init__.py before continuying... [ENTER]"
	git add sigla/__init__.py pyproject.toml
	git commit -m "build & publish: $(version)"
	git push
	poetry publish --build --username minty

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
	poetry run flake8

black:
	poetry run black . -l 79

mypy:
	poetry run mypy -p sigla #--disallow-untyped-calls --disallow-untyped-defs

check: black flake8 mypy