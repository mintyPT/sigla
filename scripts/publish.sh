# patch, minor, major, prepatch, preminor, premajor, prerelease.
poetry version patch

version=$(poetry version -s)
sed -i '' -E "s/__version__ = \"[0-9]+.[0-9]+.[0-9]+\"/__version__ = \"$version\"/" core/__init__.py

poetry build


git add core/__init__.py pyproject.toml dist
git commit -m "v$version"
git tag -a "v$version" -m "v$version"


git push
git push --tags

poetry publish --username minty