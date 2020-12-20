install:
	poetry install

publish:
	poetry version patch
	read -p "Update the version on src/sigla/__init__.py before continuying... [ENTER]"
	poetry publish --build

show:
	poetry show -v

test:
	poetry run pytest

main-render:
	poetry run python src/sigla/cli.py render $(file)

version:
	poetry run python src/sigla/cli.py version

flake8:
	poetry run flake8

black:
	poetry run black .