.PHONY: preview render publish

preview:
	mkdocs serve

render:
	mkdocs build

publish:
	mkdocs gh-deploy
