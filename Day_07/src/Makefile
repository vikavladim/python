all: build

build:
	docker-compose run -it day07_cont bash

html:
	sphinx-build -b html docs docs/_build

clean:
	rm -rf docs/_build/* docs/build/*