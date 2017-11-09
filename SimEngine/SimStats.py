#!/usr/bin/python
'''
\brief Collects and logs statistics about the ongoing simulation.

\author Thomas Watteyne <watteyne@eecs.berkeley.edu>
\author Kazushi Muraoka <k-muraoka@eecs.berkeley.edu>
\author Nicola Accettura <nicola.accettura@eecs.berkeley.edu>
\author Xavier Vilajosana <xvilajosana@eecs.berkeley.edu>
'''

#============================ logging =========================================

import logging
class NullHandler(logging.Handler):
    def emit(self, record):
        pass
log = logging.getLogger('SimStats')
log.setLevel(logging.ERROR)
log.addHandler(NullHandler())

#============================ imports =========================================

import SimEngine
import SimSettings

#============================ defines =========================================

#============================ body ============================================

class SimStats(object):

    #===== start singleton
    _instance      = None
    _init          = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SimStats,cls).__new__(cls, *args, **kwargs)
        return cls._instance
    #===== end singleton

    def __init__(self,runNum):

        #===== start singleton
        if self._init:
            return
        self._init = True
        #===== end singleton

        # store params
        self.runNum                         = runNum

        # local variables
        self.engine                         = SimEngine.SimEngine()
        self.settings                       = SimSettings.SimSettings()

        # stats
        self.stats                          = {}
        self.columnNames                    = []
        self.numCycles                      = 0

        # start file
        if self.runNum==0:
            self._fileWriteHeader()

        # schedule actions
        self.engine.scheduleAtStart(
            cb          = self._actionStart,
        )
        self.engine.scheduleAtAsn(
            asn         = self.engine.getAsn()+self.settings.slotframeLength-1,
            cb          = self._actionEndCycle,
            uniqueTag   = (None,'_actionEndCycle'),
            priority    = 10,
        )
        self.engine.scheduleAtEnd(
            cb          = self._actionEnd,
        )

    def destroy(self):
        # destroy my own instance
        self._instance                      = None
        self._init                          = False

    #======================== private =========================================

    def _actionStart(self):
        '''Called once at beginning of the simulation.'''
	#always pause at the begining by default
	#firstpause=1
        #self.engine.pauseAtAsn(firstpause)
        pass

    def _actionEndCycle(self):
        '''Called at each end of cycle.'''

        cycle = int(self.engine.getAsn()/self.settings.slotframeLength)

	synced = len([mote.id for mote in self.engine.motes if mote.isSync == True])
	joined = len([mote.id for mote in self.engine.motes if mote.isJoined == True])
	bootstrapped = len([mote.id for mote in self.engine.motes if mote.isBootstrapped == True])

        # print
        #if self.settings.cpuID==None:
        print('   cycle: {0}/{1} sync: {2}/{3} join: {4}/{5} bootstrapped: {6}/{7}'.format(cycle,self.settings.numCyclesPerRun-1,synced,self.settings.numMotes,joined,self.settings.numMotes,bootstrapped,self.settings.numMotes))

        # write statistics to output file
        self._fileWriteStats(
            dict(
                {
                    'runNum':              self.runNum,
                    'cycle':               cycle,
                }.items() +
                self._collectSumMoteStats().items()  +
                self._collectScheduleStats().items()
            )
        )

	# temp hack
	if self.engine.removeSharedCells == True:
            for mote in self.engine.motes:
		for ts in range(1,10):
		    mote.schedule.pop(ts)
	    self.engine.removeSharedCells = False

        # schedule next statistics collection
        self.engine.scheduleAtAsn(
            asn         = self.engine.getAsn()+self.settings.slotframeLength,
            cb          = self._actionEndCycle,
            uniqueTag   = (None,'_actionEndCycle'),
            priority    = 10,
        )

    def _actionEnd(self):
        '''Called once at end of the simulation.'''
        self.numCycles = int(self.engine.getAsn()/self.settings.slotframeLength)
        self._fileWriteTopology()

    #=== collecting statistics

    def _collectSumMoteStats(self):
        returnVal = {}

        for mote in self.engine.motes:
            moteStats        = mote.getMoteStats()
            if not returnVal:
                returnVal    = moteStats
            else:
                for k in returnVal.keys():
                    returnVal[k] += moteStats[k]

        return returnVal

    def _collectScheduleStats(self):

        returnVal = {}

        # compute the number of schedule collisions

        # Note that this cannot count past schedule collisions which have been relocated by 6top
        # as this is called at the end of cycle
        scheduleCollisions = 0
        txCells = []
        for mote in self.engine.motes:
            for (ts,cell) in mote.schedule.items():
                (ts,ch) = (ts,cell['ch'])
                if cell['dir']==mote.DIR_TX:
                    if (ts,ch) in txCells:
                        scheduleCollisions += 1
                    else:
                        txCells += [(ts,ch)]

        # collect collided links
        txLinks = {}
        for mote in self.engine.motes:
            for (ts,cell) in mote.schedule.items():
                if cell['dir']==mote.DIR_TX:
                    (ts,ch) = (ts,cell['ch'])
                    (tx,rx) = (mote,cell['neighbor'])
                    if (ts,ch) in txLinks:
                        txLinks[(ts,ch)] += [(tx,rx)]
                    else:
                        txLinks[(ts,ch)]  = [(tx,rx)]

        collidedLinks = [txLinks[(ts,ch)] for (ts,ch) in txLinks if len(txLinks[(ts,ch)])>=2]

        # compute the number of Tx in schedule collision cells
        collidedTxs = 0
        for links in collidedLinks:
            collidedTxs += len(links)

        # compute the number of effective collided Tx
        effectiveCollidedTxs = 0
        insufficientLength   = 0
        for links in collidedLinks:
            for (tx1,rx1) in links:
                for (tx2,rx2) in links:
                    if tx1!=tx2 and rx1!=rx2:
                        # check whether interference from tx1 to rx2 is effective
                        if tx1.getRSSI(rx2) > rx2.minRssi:
                            effectiveCollidedTxs += 1

        # collect shared cell stats for each individual shared cell (by default there is only one)
        for mote in self.engine.motes:
            sharedCellStats        = mote.getSharedCellStats()
            if not returnVal:
                returnVal    = sharedCellStats
            else:
                for k in returnVal.keys():
                    if k in sharedCellStats.keys():
                        returnVal[k] += sharedCellStats[k]
                    else:
                        returnVal[k] += 0

        returnVal.update({'scheduleCollisions':scheduleCollisions, 'collidedTxs': collidedTxs, 'effectiveCollidedTxs': effectiveCollidedTxs})

        return returnVal

    #=== writing to file

    def _fileWriteHeader(self):
        output          = []
        output         += ['## {0} = {1}'.format(k,v) for (k,v) in self.settings.__dict__.items() if not k.startswith('_')]
        output         += ['\n']
        output          = '\n'.join(output)

        with open(self.settings.getOutputFile(),'w') as f:
            f.write(output)

    def _fileWriteStats(self,stats):
        output          = []

        # columnNames
        if not self.columnNames:
            self.columnNames = sorted(stats.keys())
            output     += ['\n# '+' '.join(self.columnNames)]

        # dataline
        formatString    = ' '.join(['{{{0}:>{1}}}'.format(i,len(k)) for (i,k) in enumerate(self.columnNames)])
        formatString   += '\n'

        vals = []
        for k in self.columnNames:
            if k in stats and type(stats[k])==float:
                vals += ['{0:.3f}'.format(stats[k])]
            elif k in stats:
                vals += [stats[k]]
	    else:
		vals += [0]

        output += ['  '+formatString.format(*tuple(vals))]

        # write to file
        with open(self.settings.getOutputFile(),'a') as f:
            f.write('\n'.join(output))

    def _fileWriteTopology(self):
        output  = []
        output += [
            '#pos runNum={0} {1}'.format(
                self.runNum,
                ' '.join(['{0}@({1:.5f},{2:.5f})@{3}'.format(mote.id,mote.x,mote.y,mote.rank) for mote in self.engine.motes])
            )
        ]
        links = {}
        for m in self.engine.motes:
            for n in self.engine.motes:
                if m==n:
                    continue
                if (n,m) in links:
                    continue
                try:
                    links[(m,n)] = (m.getRSSI(n),m.getPDR(n))
                except KeyError:
                    pass
        output += [
            '#links runNum={0} {1}'.format(
                self.runNum,
                ' '.join(['{0}-{1}@{2:.0f}dBm@{3:.3f}'.format(moteA.id,moteB.id,rssi,pdr) for ((moteA,moteB),(rssi,pdr)) in links.items()])
            )
        ]
        output += [
            '#aveChargePerCycle runNum={0} {1}'.format(
                self.runNum,
                ' '.join(['{0}@{1:.2f}'.format(mote.id,(mote.getMoteStats()['chargeConsumed']-self.engine.startCharge[mote.id])/self.settings.numCyclesPerRun) for mote in self.engine.motes])
            )
        ]
	pgen=0
	for mote in self.engine.motes:
		pgen=pgen+mote.getMoteStats()['pktGen']
        output += [
            '#PktGen runNum={0} {1} {2}'.format(
                self.runNum,
                ' '.join(['{0}@{1:.2f}'.format(mote.id,mote.getMoteStats()['pktGen']) for mote in self.engine.motes]),pgen
            )
        ]
	prec=0
	for mote in self.engine.motes:
		prec=prec+mote.getMoteStats()['pktReceived']
        output += [
            '#PktReceived runNum={0} {1} {2}'.format(
                self.runNum,
                ' '.join(['{0}@{1:.2f}'.format(mote.id,mote.getMoteStats()['pktReceived']) for mote in self.engine.motes]),prec
            )
        ]
	pqueued=0
	for mote in self.engine.motes:
		pqueued=pqueued+mote.getMoteStats()['dataQueueFill']
	output += [
            '#PktInQueue runNum={0} {1} {2}'.format(
                self.runNum,
                ' '.join(['{0}@{1:.2f}'.format(mote.id,mote.getMoteStats()['dataQueueFill']) for mote in self.engine.motes]),pqueued
            )
        ]
	pdropqueue=0
	for mote in self.engine.motes:
		pdropqueue=pdropqueue+mote.getMoteStats()['pktDropQueue']
	output += [
            '#PktDropsQueue runNum={0} {1} {2}'.format(
                self.runNum,
                ' '.join(['{0}@{1:.2f}'.format(mote.id,mote.getMoteStats()['pktDropQueue']) for mote in self.engine.motes]),pdropqueue
            )
        ]
	pdropmac=0
	for mote in self.engine.motes:
		pdropmac=pdropmac+mote.getMoteStats()['pktDropMac']
	output += [
            '#PktDropsMac runNum={0} {1} {2}'.format(
                self.runNum,
                ' '.join(['{0}@{1:.2f}'.format(mote.id,mote.getMoteStats()['pktDropMac']) for mote in self.engine.motes]),pdropmac
            )
        ]
	assert pgen == prec + pqueued + pdropqueue + pdropmac
        if self.settings.withJoin:
            output += [
                '#join runNum={0} {1}'.format(
                    self.runNum,
                    ' '.join(['{0}@{1}'.format(mote.id, mote.joinAsn) for mote in self.engine.motes])
                )
            ]
            output += [
                '#firstBeacon runNum={0} {1}'.format(
                    self.runNum,
                    ' '.join(['{0}@{1}'.format(mote.id, mote.firstBeaconAsn) for mote in self.engine.motes])
                )
            ]
	if self.settings.withBootstrap:
	    output += [
                '#firstReady runNum={0} {1}'.format(
                    self.runNum,
                    ' '.join(['{0}@{1}'.format(mote.id, mote.firstIsBootstrapped) for mote in self.engine.motes])
                )
            ]
        output  = '\n'.join(output)

        with open(self.settings.getOutputFile(),'a') as f:
            f.write(output)
