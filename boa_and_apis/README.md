# Reduction of bolometer data with BoA and APIS

## BoA

In preparation for the Bolometer data reduction tutorials, you may
want to download and install a recent version of Boa, which includes
scripts and calibration files for Artemis. The easiest way is to
download the repository from GitHub:
https://github.com/FredSchuller/BoADAS.git

Note that this has been successfully installed on various flavours of
linux, but this does NOT compile on Mac OS X - although it does work
on a virtual machine running linux on a Mac.

A collection of example commands with detailed comments is provided
in the file boa_examply.py in this directory.



### Install

Some cut and pastable install notes:

    git clone https://github.com/FredSchuller/BoADAS.git
    curl 'https://uni-bonn.sciebo.de/s/zC6DlduTGcGBRTZ/download?path=%2F&files=BoaLib-2016-02-18.tgz' > BoaLib-2016-02-18.tgz

Then, uncompress the BoaLib tarball:

    tar xzvf BoaLib-2016-02-18.tgz

And follow the instructions in the README file included.


## APIS: Artemis Pipeline using IDL and Scanamorphos

The template scripts that were used during the tutorial are provided
in this directory. In addition, below are detailed instructions for
the installation of the software, and the configuration of the
various directories.

### Installation Instructions

- Download the three compressed archive files IDL_proc_mar2018.tgz, 
Calibration_2017.tgz, SCANAM_ARTEMIS_v3.tar.gz from the links at the bottom 
of http://www.apex-telescope.org/instruments/pi/artemis/data_reduction/

- IDL_proc_mar2018.tgz (basic pipeline) contains all IDL procedures needed for 
basic reduction of ArTeMiS data, located in the directory apexpro/ 

- Calibration_2017.tgz contains all required calibration files in directory
Calib_partemis/ 

- SCANAM_ARTEMIS_v3.tar.gz contains all Scanamorphos routines/files in the 
directory tree SCANAM_ARTEMIS


- Uncompress IDL_proc_mar2018.tgz in the directory where you plan to use
IDL and APIS (using: tar -zxvf IDL_proc_mar2018.tgz).
This will create the sub-directory apexpro/ with the APIS procedures.

- Uncompress Calibration_2017.tgz in your « work_dir » directory, which should 
preferentially be located in a disk where you have significant storage space.
This will create the sub-directory Calib_partemis/ with all required calibration 
tables.
Within your « work_dir », you should also create an "apexdata" directory 
(+ sub-directories) where data at various stages of the reduction process 
and other useful files will be stored:

Directory | Description
----------|-------------
work_dir/apexdata/rawdata/	 | this is where your ArTeMiS rawdata should be copied
work_dir/apexdata/obslogs/	 | where your available observing logs should be copied
work_dir/apexdata/basic_xdr/	 | where rawdata in IDL format will be stored
work_dir/apexdata/map_otf_xdr/   | where reduced data in IDL format will be stored
work_dir/apexdata/map_otf_fits/  | where masks and output fits files should be stored
 
More details may be found in "pipeline_IDL_artemis_october2014_v1.pdf".


- Move to directory apexpro and customize the file « obs1_artemis_config.pro ».
The items to be customized are: 
« work_dir » (which should give the path to the directory where the sub-directories 
Calib_partemis/ and apexdata/ are located on your system), 
« project_name » (the name of your APEX/ArTeMiS project), and « calibration_table » (e.g., for 2017 data, use calibration_table_350_2017 and 
calibration_table_450_2017).

- Uncompress SCANAM_ARTEMIS_v3.tar.gz in directory apexpro. This will create 
(or update) a subdirectory tree named SCANAM_ARTEMIS/ with all Scanamorphos 
routines/files.

- Add the directories apexpro, apexpro/SCANAM_ARTEMIS/pro_artemis, 
apexpro/SCANAM_ARTEMIS/pro_common_inst, and apexpro/SCANAM_ARTEMIS/pro_format_input 
to your IDL_PATH (or simply add +apexpro to recursively add apexpro and all the
subdirectories below it)

- You should also include the IDL Astronomy library to IDL_PATH. If it is not installed
on your system, you can get this library from: https://idlastro.gsfc.nasa.gov/


- You should then be ready to start reducing data with APIS.
Run IDL from, e.g., directory apexpro. An example of a typical data reduction 
session with the basic pipeline (without Scanamorphos) is provided in the 
template script file « ori_isf_artemis_tutorial.pro ».
For the Scanamorphos part, see the Scanamorphos Guide (arXiv:1803.04264).


NB: If you get stuck at any stage, please contact Philippe Andre (pandre@cea.fr), 
Frederic Schuller (frederic.schuller@cea.fr), 
or Pascal Gallais (pascal.gallais.cea.fr)

