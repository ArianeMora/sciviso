# sciviso

python -m pip install --user --upgrade twine
python setup.py sdist bdist_wheel
twine check dist/YOUR_PROJECT-1.0.0.tar.gz
twine upload dist/*
https://pypi.org/project/YOUR_PROJECT/