Here we discuss CASA and derived products to do array combinations.

## CASA

CASA: (Common Astronomy Software Applications) is used for all ALMA
and VLA calibration and imaging, and the natural starting point
for any array combination procedures. Please have CASA 5.1
installed on your laptop, and follow the guidelines in 
https://casa.nrao.edu/casa_obtaining.shtml

Some people have experience with MIRIAD, and we will make a comparison
with MIRIAD procedures and capabilities at some points during the
workshop.

## QAC

QAC: (Quick Array Combinations) is a set of functions to help you
call CASA routines to exersize array combination techniques. It will
use a number of other methods (see tp2vis, sd2vis, ssc etc.)

See https://github.com/teuben/QAC how to install but here is the basic
rundown assuming you have CASA installed:

      # install
      git clone https://github.com/teuben/QAC
      ln -s ~/.casa/QAC 
      cd QAC
      make tp2vis
      cat casa.init.py >> ~/.casa
      # benchmark
      cd test
      curl http://admit.astro.umd.edu/~teuben/QAC/qac_bench.tar.gz | tar zxf -
      time casa --nogui -c bench.py

Mac people need to replace the casa command by

      time /Applications/CASA.app/Contents/MacOS/casa --nogui -c bench.py

For version 5.1.2 the final reported flux should be around 383.6


## TP2VIS

TP2VIS: a new routine to help with a Joint Deconvolution style of
combining single dish (TP) with interferometric data (VIS).

Installation can be done via QAC.


## SD2VIS

SD2VIS: similar to TP2VIS but only works on single pointings, no mosaic.

Installation can be done via QAC.


