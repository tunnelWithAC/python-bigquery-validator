Build steps

python3 -m pip install --upgrade build
python3 -m build

Upload

python3 -m pip install --upgrade twine
python3 -m twine upload --repository testpypi dist/*
