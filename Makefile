.PHONY: antlr

parse: antlr
	python3 parse.py examples/test.noise

debug: antlr
	sh antlr4-tester.sh noisy.g4 examples/test.noise spec

antlr:
	antlr4 noisy.g4
