import os, sys
import yaml
import numpy
from matplotlib import pyplot
from xml.dom import minidom
import time
import subprocess
import glob
import json
from matplotlib.ticker import MaxNLocator
from astropy.time import Time

CHOICE = int(sys.argv[1]) # 0:run LC, 1: draw LC

# start and end of the mission
mintime = 239557417 # 2008-08-04T15:43:33.000
maxtime = 528835414.0 #492018214 # 2016-08-04T15:43:59.600 

def make_yaml(baseYaml, nname):
    d = yaml.load(open(baseYaml))
    d['selection']['target'] = nname
    outputyaml = '%s/%s.yaml'%(ndir,nname.replace(' ','_'))
    print outputyaml
    stream = file(outputyaml, 'w')
    yaml.dump(d,stream)
    return outputyaml

def make_run(baseRun, outname):
    fbase = open(baseRun,'r')
    fbaseL = fbase.read()
    fbase.close()
    fnew = open(outname,'w')
    fnew.write(fbaseL) # .replace('novaname',nname))
    fnew.close()

# read list of novae
filename = "/nfs/farm/g/glast/u/afrancko/software/blazarFlares/sourceList.txt"
f = open(filename)
fl = f.readlines()
f.close()

outdir = "/u/gl/afrancko/workdir/software/blazarFlares/blazars"

scriptPath = "/u/gl/afrancko/workdir/software/blazarFlares/lcpipe"
baseYaml = "%s/base.yaml"%scriptPath
baseRun = "%s/runLC.py"%scriptPath

nsubmit = 0

STARTFRESH = False

# loop over sources
for n in fl:
    # skip lines that are commented out
    if n[0] == "#":
        continue

    # read values for novae
    nname = n.replace('\n','')

    # create directory for novae
    ndir = "%s/%s"%(outdir,nname.replace(' ','_'))
    os.system("mkdir -p %s"%(ndir))

    if STARTFRESH:
       print "remove srcmdl fit files"
       cmd = 'rm %s/*.fits'%ndir
       print cmd
       os.system(cmd)
       cmd = 'rm %s/srcmdl*.xml'%ndir
       print cmd
       os.system(cmd)
       cmd = 'rm %s/*.par'%ndir
       print cmd
       os.system(cmd)

    # place a modified config file in each time bin directory
    yamlFile = '%s/%s.yaml'%(ndir,nname.replace(' ','_'))
    print "make yaml"
    yamlFile = make_yaml(baseYaml, nname)

    logFile = yamlFile.replace('.yaml','.log')

    if CHOICE == 0:

       nJobs = subprocess.check_output(["bjobs"]).count('afranck')
       while (True):
          nJobs = subprocess.check_output(["bjobs"]).count('afranck')
          print "number of jobs ", nJobs
          if nsubmit%30==0 and nsubmit>0:
             print "submitted 30. Wait 30 sec."
             time.sleep(30)
          if nJobs>600:
             print "wait 10 sec"
             time.sleep(10)
          else:
             break


       cmd = 'bsub -W 1500 -n 4 -R "span[ptile=4]" -o %s python %s "%s" %s'%(logFile, baseRun, nname, yamlFile)
       print cmd
       print "nsubmit ", nsubmit
       nsubmit += 1
       os.system(cmd)
       #exit()


print "totel nsubmit ", nsubmit
