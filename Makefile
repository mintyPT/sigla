install:
	poetry install

publish:
	poetry version patch
	read -p "Update the version on src/sigla/__init__.py before continuying... [ENTER]"
	git add src/sigla/__init__.py pyproject.toml
	git commit -m "build: bump version before publish"
	poetry publish --build
	git push

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