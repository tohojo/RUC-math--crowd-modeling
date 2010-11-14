#!/bin/bash

cd c-ext && python2 setup.py build && cp build/lib.linux-x86_64-2.7/optimised.so ..
