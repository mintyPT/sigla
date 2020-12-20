install:
	poetry install

publish:
	poetry version patch
	poetry publish --build

show:
	poetry show -v

test:
	poetry run pytest

main-render:
	poetry run python src/sigla/cli.py render $(file)

flake8:
	poetry run flake8

black:
	poetry run black .