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
	poetry run python src/sigla/main.py render $(file)

