#!/bin/bash

if which python2 >/dev/null 2>&1; then
	PYTHON=python2
else
	PYTHON=python
fi

cd c-ext && $PYTHON setup.py build && cp $(find -name optimised.so -o -name optimised.pyd) ..
