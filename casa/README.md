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

      cd ~/mycasastuff                          # where-ever
      git clone https://github.com/teuben/QAC
      mkdir ~/.casa                             # in case it didn't exist
      ln -s `pwd`/QAC ~/.casa/QAC 
      cd QAC
      make tp2vis
      cat casa.init.py >> ~/.casa/init.py
      
      # run a benchmark, should be around 3 mins
      
      cd test
      curl http://admit.astro.umd.edu/~teuben/QAC/qac_bench.tar.gz | tar zxf -
      casa-config --version
      time casa --nogui -c bench.py

MacOS people may need to replace the casa command by (something like)

      time /Applications/CASA.app/Contents/MacOS/casa --nogui -c bench.py

For version 5.1.2 the final reported flux should be around 383.6 and you should see an "OK" at the
end of the last REGRESSION line


## TP2VIS

TP2VIS: a new routine to help with a Joint Deconvolution style of
combining single dish (TP) with interferometric data (VIS).

Installation can be done via QAC. See above or https://github.com/tp2vis/distribute


## SD2VIS

SD2VIS: similar to TP2VIS but only works on single pointings, no mosaic.

Installation can be done via QAC. See also https://www.oso.nordic-alma.se/software-tools.php


## AU

The Analysis Utilities (AU) are a set of CASA functions, and can be installed very much like
QAC by patching up your ~/.casa/init.py file.   Details are on
https://casaguides.nrao.edu/index.php/Analysis_Utilities but the following cut and pastable
commands should work from your Unix terminal:

        cd ~/.casa
and

        wget ftp://ftp.cv.nrao.edu/pub/casaguides/analysis_scripts.tar
        tar xf analysis_scripts.tar
	
or

        curl ftp://ftp.cv.nrao.edu/pub/casaguides/analysis_scripts.tar | tar xf -

and now add the following three lines to your ~/.casa/init.py file:

        sys.path.append(os.environ['HOME'] + '/.casa/analysis_scripts')
        import analysisUtils as au
        print "Added au"

