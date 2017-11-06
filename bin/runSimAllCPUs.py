#!/usr/bin/python
'''
\brief Start batch of simulations concurrently.
Workload is distributed equally among CPU cores.
\author Thomas Watteyne <watteyne@eecs.berkeley.edu>
'''

import os
import time
import math
import multiprocessing

MIN_TOTAL_RUNRUNS = 1

def runOneSim(params):
    (cpuID,numRuns,numMotes,namedir,rpl,otf,sixtop) = params

    command     = []
    command    += ['python runSimOneCPU.py']
    command    += ['--numRuns {0}'.format(numRuns)]

    command    += ['--numMotes {0}'.format(numMotes)] 
    command    += ['--simDataDir {0}'.format(namedir)]
    command    += ['--dioPeriod {0}'.format(rpl)]
    command    += ['--otfHousekeepingPeriod {0}'.format(otf)]
    command    += ['--sixtopHousekeepingPeriod {0}'.format(sixtop)]

    command    += ['--cpuID {0}'.format(cpuID)]
    #command    += ['&']
    command     = ' '.join(command)
    print command
    os.system(command)

def printProgress(num_cpus):
    while True:
        time.sleep(1)
        output     = []
        for cpu in range(num_cpus):
	    
            with open('cpu{0}.templog'.format(cpu),'r') as f:
                output += ['[cpu {0}] {1}'.format(cpu,f.read())]
        allDone = True
        for line in output:
            if line.count('ended')==0:
                allDone = False
        output = '\n'.join(output)
        #os.system('cls' if os.name == 'nt' else 'clear')
        #print output
        if allDone:
            break
    for cpu in range(num_cpus):
        os.remove('cpu{0}.templog'.format(cpu))

if __name__ == '__main__':

    #reading parameters
    namedir=os.sys.argv[1]
    numMotes=os.sys.argv[2]
    rpl=os.sys.argv[3]
    otf=os.sys.argv[4]
    sixtop=os.sys.argv[5]

    multiprocessing.freeze_support()
    #num_cpus = multiprocessing.cpu_count()
    num_cpus = 1
    runsPerCpu = int(math.ceil(float(MIN_TOTAL_RUNRUNS)/float(num_cpus)))
    pool = multiprocessing.Pool(num_cpus)
    pool.map_async(runOneSim,[(i,runsPerCpu,numMotes,namedir,rpl,otf,sixtop) for i in range(num_cpus)])
    printProgress(num_cpus)
    print("Done. Press Enter to close.")
