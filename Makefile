.PHONY: build pybuild upload clean man release

build: | clean man pybuild

pybuild:
	python3 -m build

upload:
	python3 -m twine upload $(wildcard dist/roff-*)

clean:
	rm -f -- $(wildcard dist/roff-*)
	rm -f -- $(wildcard docs/roff.?)

man:
	./roff convert docs/roff.1.md
	./roff convert docs/roff.5.md

release: | clean man pybuild upload
