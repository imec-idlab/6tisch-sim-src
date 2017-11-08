
#import numpy as np
#import matplotlib.pyplot as plt
import os
import collections
import operator
import subprocess
#from pylab import *
import random
import csv
import sys

def parse(filename):
	

    
    command="find "
    args='{0} -name output* | sort -V'.format(filename)

    tmp = os.popen(command+args).read()
    listOfFiles=tmp.split("\n")

    #print listOfFiles
    for filename in listOfFiles:
	if len(filename)!=0:
		
		fa=filename.split('cpu')[0]
		fb=filename.split('cpu')[1]

		fc=fb.split(".")[0]
		fd=fb.split(".")[1]
		num=random.randint(100,900000)
		newname=fa+"cpu"+str(num)+"."+fd
		command="mv "
    		args='{0} {1}'.format(filename,newname)
		os.popen(command+args)
		print newname

if __name__ == '__main__':
	parse(sys.argv[1])
