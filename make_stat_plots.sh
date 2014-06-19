#export test_directory="/afs/hep.wisc.edu/user/dan/AAA_scaletest/rapid-redirect-2013-09-25/wisconsin"
#export test_directory="/afs/hep.wisc.edu/user/dan/AAA_scaletest/rapid-redirect-2013-09-25/wisconsin_internal"
#export test_directory="/afs/hep.wisc.edu/user/dan/AAA_scaletest/rapid-redirect-2013-09-25/nebraska/"

#export test_directory="/afs/hep.wisc.edu/user/dan/AAA_scaletest/rapid-redirect-2013-11-08/nebraska_global/"
#export test_directory="/afs/hep.wisc.edu/user/dan/AAA_scaletest/rapid-redirect-2013-11-08/nebraska_internal/"

#ls $test_directory/stdout* > test_files.txt

#python make_stat_plots.py test_files_wisconsin.txt 8000 500 1380125156
#python make_stat_plots.py test_files_wisconsin_internal.txt 4000 300 1380139669
#python make_stat_plots.py test_files_nebraska.txt 3600 300 1380129980

#python make_stat_plots.py test_files_nebraska_global.txt 4000 400 1383947801 
#python make_stat_plots.py test_files_nebraska_internal.txt 3600 300 1383942846 

#python make_stat_plots.py test_files_nov29.txt 7200 400 1385791943
#python make_stat_plots.py test_files_nov30.txt 7200 400 1385860556 

# python make_stat_plots.py test_files_dec4.txt 14400 1000 1386196063
# python make_stat_plots.py testfilesjan21.txt 4304  200 1390333448
# python make_stat_plots.py t2wisctestjan24.txt 3600  180 1390857140
# python make_stat_plots.py t2ucsdtestjan27.txt 4630  200 1390878870
# python make_stat_plots.py t2wisctestjan28.txt 6884  200 1390941080
# python make_stat_plots.py t2wisctestjan28eve.txt 6801  200 1390964870
# python make_stat_plots.py t2wisctestjan29.txt 6670  300 1391031522
# python make_stat_plots.py t2nebrtestjan29.txt 3650  180 1391050325 T2_US_Nebraska
# python make_stat_plots.py t2purduetestjan30.txt 4811  160 1391104319
# python make_stat_plots.py t2mit_testjan30.txt 3653  180 1391109265 T2_US_MIT
# python make_stat_plots.py t2purduefulltestjan30.txt 3659  180 1391113458 T2_US_Purdue
# python make_stat_plots.py t2caltechtestjan30.txt 3658  180 1391120280 T2_US_Caltech
# python make_stat_plots.py t2ucsdtestjan29.txt 4481  220 1391012412 T2_US_UCSD
# python make_stat_plots.py t2wisctestjan30.txt 3684  180 1391124716 T2_US_Wisconsin
# python make_stat_plots.py t2wisctestjan31.txt 3189  180  1391196190 T2_US_Wisconsin
# python make_stat_plots.py t2wisctestfeb5.txt 3659  180  1391638257 T2_US_Wisconsin
# python make_stat_plots.py t2nebrtestfeb4.txt 3657  30 1391533911 T2_US_Nebraska
# python make_stat_plots.py t2purduetestfeb6.txt 3673  180 1391703966 T2_US_Purdue
# python make_stat_plots.py t2floridatestfeb6.txt 3658 180 1391712761 T2_US_Florida
# python make_stat_plots.py t2wisctestfeb6.txt 3180  150  1391729942 T2_US_Wisconsin
# python make_stat_plots.py t2caltechtestfeb5.txt 3662  180 1391622109 T2_US_Caltech
# python make_stat_plots.py t2caltechtestfeb6.txt 3655  180 1391718881 T2_US_Caltech
# python make_stat_plots.py t2wisctestfeb7.txt 3420  170  1391792054 T2_US_Wisconsin
# python make_stat_plots.py t2wisctestfeb7b.txt 3120  150  1391797207 T2_US_Wisconsin
# python make_stat_plots.py t2caltechtestfeb7.txt 3671  180 1391807687 T2_US_Caltech
# python make_stat_plots.py t2purduetestfeb7.txt 3653  180 1391818976 T2_US_Purdue
# python make_stat_plots.py t2purduetestfeb10.txt 3723  180 1392066856 T2_US_Purdue
# python make_stat_plots.py t2caltechmar4.txt 2936  120 1393950069 T2_US_Caltech
# python make_stat_plots.py t2purduemar4.txt 2936  120 1393955334 T2_US_Purdue
# python make_stat_plots.py t2wisctestmar7.txt 3032  150  1394238096 T2_US_Wisconsin
# python make_stat_plots.py t2wisctestmar7.txt 3032  150  1394238096 T2_US_Wisconsin
# python make_stat_plots.py t2wiscmar10.txt 2995  120  1394485612 T2_US_Wisconsin
# python make_stat_plots.py t2caltechmar11.txt 3099  120 1394552090 T2_US_Caltech
# python make_stat_plots.py t2caltechmar11cl.txt 2941  120 1394557806 T2_US_Caltech
# python make_stat_plots.py t2caltechgdflmar11.txt 2236  100 1394564411 T2_US_Caltech
# python make_stat_plots.py t2caltechgdflmar13.txt 2955  120 1394730198 T2_US_Caltech
# python make_stat_plots.py t2caltechmar18.txt 2961  120 1395156776 T2_US_Caltech
# python make_stat_plots.py t2purduemar18.txt 2982  120 1395161563 T2_US_Purdue
# python make_stat_plots.py t2vanderbiltmar27.txt 3672  180 1395959125 T2_US_Vanderbilt
# python make_stat_plots.py t2caltechmar28.txt 3423  120 1396028073 T2_US_Caltech
# python make_stat_plots.py t2caltechcutoffmar28.txt 1154  60 1396034448 T2_US_Caltech
# python make_stat_plots.py t2purdueapr1.txt 3915  180 1396365093 T2_US_Purdue
# python make_stat_plots.py t2mittest_apr1.txt 3790  180 1396365360 T2_US_MIT
# python make_stat_plots.py t2nebrtestapr7c.txt 2868 140 1396902789 T2_US_Nebraska
# python make_stat_plots.py t2vandyapr17.txt 2856 180 1397772196 T2_US_Vanderbilt
# python make_stat_plots.py t2ucsdcmsxrdapr18.txt 2853  140 1397851400 T2_US_UCSD-cmsxrootd.fnal.gov
# python make_stat_plots.py t2ucsdxrdunlapr18.txt 2868  140 1397859787 T2_US_UCSD-xrootd.unl.edu
# python make_stat_plots.py t2ucsdcmsxrd1apr21.txt 2840 140 1398099543 T2_US_UCSD-cmsxrootd1.fnal.gov
# python make_stat_plots.py t2purdueapr21b.txt 2874 140 1398114658 T2_US_Purdue
# python make_stat_plots.py t2wisccmsxrd1apr21.txt 2847 140 1398106310 T2_US_Wisconsin-cmsxrootd1.fnal.gov
# python make_stat_plots.py t2wisccmsxrd1apr22.txt 2848 140 1398184818 T2_US_Wisconsin-cmsxrootd1.fnal.gov
# python make_stat_plots.py t2wisccmsxrdapr22.txt 2868 140 1398189609 T2_US_Wisconsin-cmsxrootd.fnal.gov
# python make_stat_plots.py t2wisccmsxrdapr22v.txt 2858 140 1398199358 T2_US_Wisconsin-cmsxrootd.fnal.gov
# python make_stat_plots.py t2ucsdcmsxrdapr22.txt 2882  140 1398198626 T2_US_UCSD-cmsxrootd.fnal.gov
# python make_stat_plots.py t2purdueapr24.txt 2871 140 1398354214 T2_US_Purdue
# python make_stat_plots.py t2purdueapr25.txt 2820 140 1398452280 T2_US_Purdue
# python make_stat_plots.py t2purdueapr28.txt 2885 140 1398724963 T2_US_Purdue
# python make_stat_plots.py t1fnalmay1.txt 2873 140 1398972645 T1_US_FNAL
# python make_stat_plots.py t2purduemay1.txt 2857 140 1398961677 T2_US_Purdue
# python make_stat_plots.py t2purduemay1rcac.txt 2866 140 1398985603 T2_US_Purdue
# python make_stat_plots.py t1fnalmay2.txt 2859 140 1399046867 T1_US_FNAL
# python make_stat_plots.py t2purduemay5.txt 2861 140 1399333968 T2_US_Purdue
# python make_stat_plots.py t2purduemay8.txt 2853 140 1399575652 T2_US_Purdue
# python make_stat_plots.py t2purduemay8b.txt 2859 140 1399582421 T2_US_Purdue
# python make_stat_plots.py t2purduemay8c.txt 2835 140 1399589876 T2_US_Purdue
# python make_stat_plots.py t2ucsdtestjan29.txt 4481  220 1391012412 T2_US_UCSD
# python make_stat_plots.py t2purduemay8c.txt 2835 140 1399589876 T2_US_Purdue
# python make_stat_plots.py t2purduejun2.txt 2860 140 1401734660 T2_US_Purdue
# python make_stat_plots.py t2purduejun5.txt 2832 140 1402004616 T2_US_Purdue
# python make_stat_plots.py t2purduejun6.txt 2913 140 1402082241 T2_US_Purdue
# python make_stat_plots.py t2mitjun6.txt 1663 90 1402085406 T2_US_MIT
# python make_stat_plots.py t2purduejun17.txt 2872 140 1403035637 T2_US_Purdue
python make_stat_plots.py t2purduejun18.txt 2838 140 1403117141 T2_US_Purdue
