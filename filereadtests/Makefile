xrdloc := /usr

# both: xrdfragcp xrdfragcpnew

xrdfragcp: xrdfragcp.cxx
	${CXX} -o $@ -I${xrdloc}/include/xrootd -L${xrdloc}/lib -l XrdCl -l pcrecpp -pthread $<

xrdfragcpnew: xrdfragcpnew.cxx
	${CXX} -o $@ -I${xrdloc}/include/xrootd -L${xrdloc}/lib  -lXrdCl -lXrdUtils -lpcrecpp -pthread $<

hdtools.jar: hdtools/HadoopTools.java
	javac -classpath '/usr/lib/hadoop-0.20/*:/usr/lib/hadoop-0.20/lib/*' $<
	jar cvfm $@ hdtools/Manifest.txt hdtools

clean:
	rm -rf xrdfragcp
