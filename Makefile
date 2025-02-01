
build:
	@echo Generating Distribution Packages
	@python -m build

test-publish:
	@python -m twine upload --repository testpypi dist/*


publish-pypi:
	@python -m twine upload dist/*

