python setup.py clean --dist --eggs --all
python setup.py sdist bdist_wheel
rm -rf dist/*
python -m twine upload --repository docker-entrypoint dist/*
