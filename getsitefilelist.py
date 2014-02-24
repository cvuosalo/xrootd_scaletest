#! /usr/bin/python

# Gets the list of published files from a site
# Outputs the file names to stdout
# May take an hour or so to run
# $1 -- the site name
#
# Author: Carl Vuosalo

import sys
import time
import urllib
import urllib2
import xml.etree.ElementTree as ET
import threading
import time


class querythread (threading.Thread):

    block = 'noblock'

    def __init__(self, threadID, blocknam):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.block = blocknam

    def run(self):
	doquery(self.block)


def doquery(blocknam):
	blocklist = { 'block' : blocknam }
	blockparam = urllib.urlencode(blocklist)
	query = 'https://cmsweb.cern.ch/phedex/datasvc/xml/prod/fileReplicas?' + blockparam
	fd = urllib2.urlopen(query)
	filetree = ET.parse(fd)
	fileroot = filetree.getroot()
	for fileBlock in fileroot:
		for fileReplica in fileBlock:
			threadLock.acquire(1)
			print fileReplica.get('name')
			threadLock.release()


# print 'arg is ', sys.argv[1]
if len(sys.argv) < 2:
	print 'Site name argument required. Exiting.'
	sys.exit(1)

node = sys.argv[1] + '*'
nodelist = {'node' : node }
nodelist  = urllib.urlencode(nodelist)
query = 'https://cmsweb.cern.ch/phedex/datasvc/xml/prod/blockReplicas?' + nodelist
fd = urllib2.urlopen(query)
tree = ET.parse(fd)

root = tree.getroot()

threadLock = threading.Lock()
thrdcnt = 0
numthrds = 50
thrdlst = []
for block in root.findall('block'):
	blocknam = block.get('name')
	if thrdcnt >= numthrds:
		while threading.activeCount() > 1:
			# print 'waiting on this many threads ', threading.activeCount() - 1
			time.sleep(1)
		thrdcnt = 0
		del thrdlst[:]
	thrdlst.insert(thrdcnt, querythread(thrdcnt, blocknam))
	thrdlst[thrdcnt].start()
	thrdcnt += 1
