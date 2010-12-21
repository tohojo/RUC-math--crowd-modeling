This project tracks the modelling project at RUC mathematics, fall 2010.

The subject of the project is crowd modelling. It is written by:

* Toke Høiland-Jørgensen (tohojo at ruc)
* Mikkel Hartmann (mihaje at ruc)
* Dan Albrechtsen (danalb at ruc)
* Malik Thrane (lmrt at ruc)
* Troels Christensen (tbc at ruc)
* Wence Xiao (wence at ruc)

The project report is available in crowd-modelling.pdf. Films of different 
simulation runs are available in the films/ subdirectory; the .parameters
files accompanying each film is a dump of the parameters used to create the
film. The source code is available in crowd-modelling-source.tar.gz. To code
should run using Python 2.5, 2.6 or 2.7 with the pygame, matplotlib and
numpy libraries on Windows, Mac OS X and Linux. To compile the c extension,
run `python setup.py build` in the c-ext directory and copy the file to the
main source code directory. build-c-ext.sh does this on Linux.

All non-source code content is licensed under the Creative Commons cc-by-sa 
license. See http://creativecommons.org/licenses/by-sa/3.0/

All source code is licensed under the GNU GPL version 3.
See http://www.gnu.org/licenses/gpl.html
