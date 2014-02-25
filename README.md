xrootd_scaletest
================

To compile:
./compile.sh

The program is run with two arguments
./xrd_test file_name open_rate

file_name needs to be a list of file names in this format:

root://{XrootD server name}//store/test/xrootd/{site name}/{file name}

For example:

root://xrootd.unl.edu//store/test/xrootd/T2_US_Caltech/store/data/Run2012D/DoublePhoton/AOD/PromptReco-v1/000/207/231/9ACED4AD-4B30-E211-9D8E-003048CFB40C.root

open_rate is a floating-point number like 0.5 or 1.0,
which is the number of seconds between file-open attempts.
