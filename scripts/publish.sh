
# patch, minor, major, prepatch, preminor, premajor, prerelease.
poetry version patch

version=$(poetry version -s)
sed -i '' -E "s/__version__ = \"[0-9]+.[0-9]+.[0-9]+\"/__version__ = \"$version\"/" sigla/__init__.py

git add sigla/__init__.py pyproject.toml
git commit -m "v$version"


git tag -a "v$version" -m "v$version"

# git push --tags
#poetry publish --build --username minty