install:
	py -m poetry install

project:
	py -m poetry run project

build:
    py -m poetry build

publish:
    py -m poetry publish --dry-run

package-install:
    py -m pip install dist/*.whl

lint:
	py -m poetry run ruff check .