.PHONY: preview render publish

preview:
	mkdocs serve

render:
	mkdocs build

publish:
	mike deploy --push --update-aliases $(version) $(alias)
