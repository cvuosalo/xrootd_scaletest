#!/bin/sh


export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/xrootd/4.0.4/lib:/nfs_scratch/cvuosalo/work/fileopenplots/CMSSW_7_0_0/lib/slc6_amd64_gcc481:/nfs_scratch/cvuosalo/work/fileopenplots/CMSSW_7_0_0/external/slc6_amd64_gcc481/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc481/cms/cmssw/CMSSW_7_0_0/lib/slc6_amd64_gcc481:/cvmfs/cms.cern.ch/slc6_amd64_gcc481/cms/cmssw/CMSSW_7_0_0/external/slc6_amd64_gcc481/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/gcc/4.8.1/lib64:/cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/gcc/4.8.1/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/xrootd/4.0.4/lib


./xrdfragcpXrdCl $*
# /afs/hep.wisc.edu/cms/sw/AAA/scaletest/xrdfragcpXrdCl $*
