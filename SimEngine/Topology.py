#!/usr/bin/python
'''
\brief Wireless network topology creator.

\author Thomas Watteyne <watteyne@eecs.berkeley.edu>
\author Kazushi Muraoka <k-muraoka@eecs.berkeley.edu>
\author Nicola Accettura <nicola.accettura@eecs.berkeley.edu>
\author Xavier Vilajosana <xvilajosana@eecs.berkeley.edu>
'''

#============================ logging =========================================

import logging
import numpy as np
class NullHandler(logging.Handler):
    def emit(self, record):
        pass
log = logging.getLogger('Topology')
log.setLevel(logging.ERROR)
log.addHandler(NullHandler())

#============================ imports =========================================

import random
import math
import scipy.special as sp
import SimSettings

#============================ defines =========================================

#============================ body ============================================

class Topology(object):

    TWO_DOT_FOUR_GHZ         = 2400000000   # Hz
    EIGHT_SIX_EIGHT_MHZ      = 868000000    # Hz
    PISTER_HACK_LOWER_SHIFT  = 40           # -40 dB
    SPEED_OF_LIGHT           = 299792458    # m/s

    ANTENNA_HEIGHT           = 0.2          # m

    STABLE_RSSI_GHz          = -78        # dBm, corresponds to aprox PDR = 0.7 in the 2.4GHz band
    STABLE_RSSI_subGHz       = -83        # dBm, corresponds to aprox PDR = 0.7 in the 868MHz band
    STABLE_NEIGHBORS         = 1
    FULLY_MESHED_SQUARE_SIDE = 0.005        # (hack) small value to speed up the construction of fully-meshed topology

    def __init__(self, motes):
        # store params
        self.motes           = motes

        # local variables
        self.settings        = SimSettings.SimSettings()

        # distance between grid modes (for grid topology only)
        self.distance        = 0.070

        # if fullyMeshed is enabled, create a topology where each node has N-1 stable neighbors
        if self.settings.fullyMeshed:
            self.stable_neighbors = len(self.motes) - 1
            self.squareSide = self.FULLY_MESHED_SQUARE_SIDE
        else:
            self.stable_neighbors = self.STABLE_NEIGHBORS
            self.squareSide = self.settings.squareSide

    #======================== public ==========================================

    def createTopology(self):
        '''
        Create a topology in which all nodes have at least stable_neighbors link
        with enough RSSI.
        If the mote does not have stable_neighbors links with enough RSSI,
        reset the location of the mote.
        '''

        # find DAG root
        dagRoot = None
        for mote in self.motes:
            if mote.id==0:
                mote.role_setDagRoot()
                dagRoot = mote
        assert dagRoot

        # put DAG root at center of area
        dagRoot.setLocation(
            x = self.squareSide/2,
            y = self.squareSide/2
        )

        # reposition each mote until it is connected
        connectedMotes = [dagRoot]
        for mote in self.motes:
            if mote in connectedMotes:
                continue

            connected = False
            while not connected:
                # pick a random location
                mote.setLocation(
                    x = self.squareSide*random.random(),
                    y = self.squareSide*random.random()
                )

                numStableNeighbors = 0

                # count number of neighbors with sufficient RSSI
                for cm in connectedMotes:

                    rssi = self._computeRSSI(mote, cm)
                    mote.setRSSI(cm, rssi)
                    cm.setRSSI(mote, rssi)

                    if SimSettings.SimSettings().subGHz:
                        if rssi>self.STABLE_RSSI_subGHz:
                            numStableNeighbors += 1
                    else:
                        if rssi>self.STABLE_RSSI_GHz:
                            numStableNeighbors += 1

                # make sure it is connected to at least stable_neighbors motes
                # or connected to all the currently deployed motes when the number of deployed motes
                # are smaller than stable_neighbors
                if numStableNeighbors >= self.stable_neighbors or numStableNeighbors == len(connectedMotes):
                    connected = True

            connectedMotes += [mote]

        # for each mote, compute PDR to each neighbors
        for mote in self.motes:
            for m in self.motes:
                if mote==m:
                    continue
                if mote.getRSSI(m)>mote.minRssi:
                    pdr = self._computePDR(mote,m)
                    mote.setPDR(m,pdr)
                    m.setPDR(mote,pdr)

        # print topology information
        '''
        for mote in self.motes:
            for neighbor in self.motes:
                try:
                    distance = self._computeDistance(mote,neighbor)
                    rssi     = mote.getRSSI(neighbor)
                    pdr      = mote.getPDR(neighbor)
                except KeyError:
                    pass
                else:
                    print "mote = {0:>3}, neigh = {1:<3}, dist = {2:>3}m, rssi = {3:>3}dBm, pdr = {4:.3f}%".format(
                        mote.id,
                        neighbor.id,
                        int(distance),
                        int(rssi),
                        100*pdr
                    )
        '''

    def getSquareCoordinates(self, coordinate, distance):
        '''
        Return the coordinates from the square around the given coordinate.
        '''
        coordinates = []
        coordinates.append((coordinate[0] - distance, coordinate[1] + distance)) # top, left
        coordinates.append((coordinate[0], coordinate[1] + distance)) # top, middle
        coordinates.append((coordinate[0] + distance, coordinate[1] + distance)) # top, right
        coordinates.append((coordinate[0] + distance, coordinate[1])) # middle, right
        coordinates.append((coordinate[0] + distance, coordinate[1] - distance)) # bottom, right
        coordinates.append((coordinate[0], coordinate[1] - distance)) # bottom, middle
        coordinates.append((coordinate[0] - distance, coordinate[1] - distance)) # bottom, left
        coordinates.append((coordinate[0] - distance, coordinate[1])) # middle, left
        return coordinates

    def isInCoordinates(self, coordinate, coordinates):
        epsilon = 0.000001
        for coordTmp in coordinates:
            if abs(coordinate[0] - coordTmp[0]) < epsilon and abs(coordinate[1] - coordTmp[1]) < epsilon:
                return True
        return False

    def createTopologyGrid(self):
        '''
        Create a topology in which all nodes have at least STABLE_NEIGHBORS link with enough RSSI.
        If the mote does not have STABLE_NEIGHBORS links with enough RSSI, reset the location of the mote.
        '''

        # find DAG root
        dagRoot = None
        for mote in self.motes:
            if mote.id==0:
                mote.role_setDagRoot()
                dagRoot = mote
        assert dagRoot

        # put DAG root at center of area
        dagRoot.setLocation(
            x = self.squareSide/2,
            y = self.squareSide/2
        )

        # Copy the contents of the list (but keep the originals) and shuffle them.
        shuffledMotes = list(self.motes)
        random.shuffle(shuffledMotes)
        # print shuffledMotes

        #### GRID PREPRATIONS.
        dagRootX, dagRootY = dagRoot.getLocation()
        # determine the number of 'square levels'
        # For example, here there are two square levels
        # m m m m m
        # m m m m m
        # m m R m m
        # m m m m m
        # m m m m m
        numberOfMotes = len(self.motes)
        currentLvl = 0
        sumMotes = 0
        while (sumMotes < numberOfMotes):
            if currentLvl == 0:
                sumMotes += 1
            else:
                sumMotes += currentLvl*8
            currentLvl += 1
        maxLvl = currentLvl - 1

        coordinatesPerLvl = []
        for lvl in range(0, maxLvl + 1):
            coordinatesThisLvl = []
            if lvl == 0:
                coordinatesThisLvl = [(dagRootX, dagRootY)]
            elif lvl == 1:
                coordinatesThisLvl = self.getSquareCoordinates((dagRootX, dagRootY), self.distance)
            elif lvl > 1:
                coordinatesPrevLvl = coordinatesPerLvl[lvl-1]
                coordinatesPrevPrevLvl = coordinatesPerLvl[lvl-2]
                for coordinatePrevLvl in coordinatesPrevLvl:
                    squareCoordinates = self.getSquareCoordinates(coordinatePrevLvl, self.distance)
                    for squareCoordinate in squareCoordinates:
                        if not self.isInCoordinates(squareCoordinate, coordinatesPrevPrevLvl) and not self.isInCoordinates(squareCoordinate, coordinatesPrevLvl) and not self.isInCoordinates(squareCoordinate, coordinatesThisLvl):
                            coordinatesThisLvl.append(squareCoordinate)
            coordinatesPerLvl.append(coordinatesThisLvl)
            # print 'Level %d: # motes = %d' % (lvl, len(coordinatesThisLvl))
            # print coordinatesThisLvl
            assert len(coordinatesThisLvl) == 1 or len(coordinatesThisLvl) == lvl*8

        allCoordinates = [j for i in coordinatesPerLvl for j in i]
        # print allCoordinates

        # reposition each mote until it is connected
        countMote = 1 # root 0 already has coordinates
        connectedMotes = [dagRoot]
        for mote in shuffledMotes:
            if mote in connectedMotes:
                continue

            connected = False
            while not connected:
                # pick a random location
                newX = np.random.normal(allCoordinates[countMote][0], self.distance / 8, 1)[0]
                newY = np.random.normal(allCoordinates[countMote][1], self.distance / 8, 1)[0]

                mote.setLocation(
                    x = newX,
                    y = newY
                )

                numStableNeighbors = 0

                # count number of neighbors with sufficient RSSI
                for cm in connectedMotes:

                    rssi = self._computeRSSI(mote, cm)
                    mote.setRSSI(cm, rssi)
                    cm.setRSSI(mote, rssi)

                    if SimSettings.SimSettings().subGHz:
                        if rssi>self.STABLE_RSSI_subGHz:
                            numStableNeighbors += 1
                    else:
                        print 'Mote %d (RSSI %.4f) - Stable RSSI %.4f - other mote %d (RSSI %.4f)' % (mote.id, rssi, self.STABLE_RSSI_GHz, cm.id, rssi)
                        if rssi>self.STABLE_RSSI_GHz:
                            numStableNeighbors += 1

                # make sure it is connected to at least STABLE_NEIGHBORS motes
                # or connected to all the currently deployed motes when the number of deployed motes
                # are smaller than STABLE_NEIGHBORS
                if numStableNeighbors >= self.STABLE_NEIGHBORS or numStableNeighbors == len(connectedMotes):
                    connected = True

            connectedMotes += [mote]
            countMote += 1

        # for each mote, compute PDR to each neighbors
        for mote in self.motes:
            for m in self.motes:
                if mote==m:
                    continue
                if mote.getRSSI(m)>mote.minRssi:
                    pdr = self._computePDR(mote,m)
                    mote.setPDR(m,pdr)
                    m.setPDR(mote,pdr)

        print 'Done. Made topology!'

    #======================== private =========================================

    def _rssiPister(self, mote, neighbor, distance):
        # sqrt and inverse of the free space path loss
        fspl = (self.SPEED_OF_LIGHT/(4*math.pi*distance*self.TWO_DOT_FOUR_GHZ))

        # simple friis equation in Pr=Pt+Gt+Gr+20log10(c/4piR)
        pr = mote.txPower + mote.antennaGain + neighbor.antennaGain + (20*math.log10(fspl))

        # according to the receiver power (RSSI) we can apply the Pister hack model.
        mu = pr-self.PISTER_HACK_LOWER_SHIFT/2 #chosing the "mean" value

        # the receiver will receive the packet with an rssi uniformly distributed between friis and friis -40
        rssi = mu + random.uniform(-self.PISTER_HACK_LOWER_SHIFT/2, self.PISTER_HACK_LOWER_SHIFT/2)
        return rssi

    def _rssiITUUrbanMicro(self, mote, neighbor, freq, distance, hTransmitter, hBaseStation):
        hEffectBaseStation = hBaseStation - 1.0
        hEffectTransmitter = hTransmitter - 1.0
        freq = freq / 100000000
        breakpointDistance = 2 * math.pi * hEffectBaseStation * hEffectTransmitter * freq / self.SPEED_OF_LIGHT

        pathLoss = None
        if 10 < distance < breakpointDistance:
            pathLoss = 22.0 * math.log10(distance) + 28.0 + 20.0 * math.log10(freq)
            pathLoss += random.gauss(0, 3)
        elif breakpointDistance < distance < 5000:
            pathLoss = 40.0 * math.log10(distance) + 7.8 - 18 * math.log10(hEffectBaseStation) - 18 * math.log10(hEffectTransmitter) + 2.0 * math.log10(freq)
            pathLoss += random.gauss(0, 3)
        else:
            print distance
            assert False

        rssi = mote.txPower + mote.antennaGain + neighbor.antennaGain - pathLoss
        return rssi

    def _rssiITURuralMacro(self, mote, neighbor, freq, distance, hTransmitter, hBaseStation):
        height = 5.0
        distanceBreakpoint = 2 * math.pi * hBaseStation * hTransmitter * freq / self.SPEED_OF_LIGHT
        freq = freq / 1000000000.0
        print freq
        pathLoss = None
        pathLossModel = lambda d : 20.0 * math.log10(40.0 * math.pi * d * freq / 3.0) + min(0.03 * math.pow(height, 1.72), 10.0) * math.log10(d) - min(0.044 * math.pow(height, 1.72), 14.77) + 0.002 * math.log10(height) * d
        if  distance < distanceBreakpoint:
            pathLoss = pathLossModel(distance)
            pathLoss += random.gauss(0, 3) # apply fade margin
        elif distanceBreakpoint < distance < 10000:
            pathLoss = pathLossModel(distanceBreakpoint) + 40 * math.log10(distance / distanceBreakpoint)
            pathLoss += random.gauss(0, 6) # apply fade margin
        else:
	    #print distance
            assert False
	    #pathLoss=1000

        rssi = mote.txPower + mote.antennaGain + neighbor.antennaGain - pathLoss
        print rssi
	#print str(distance)+" - "+str(rssi)
        return rssi

    def _rssiAHPico(self, mote, neighbor, freq, distance):
        corrFunc = 21 * math.log10(freq / 900.0)
        pathLoss = 23.3 + 36.7 * math.log10(distance) + corrFunc
        pathLoss += random.gauss(0, 3.6)

        rssi = mote.txPower + mote.antennaGain + neighbor.antennaGain - pathLoss
        return rssi

    def _computeRSSI(self,mote,neighbor):
        ''' computes RSSI between any two nodes (not only neighbors) according to the Pister-hack model.'''

        rssi = None
        # distance in m
        distance = self._computeDistance(mote,neighbor)

        freq = self.TWO_DOT_FOUR_GHZ
        if SimSettings.SimSettings().subGHz:
            freq = self.EIGHT_SIX_EIGHT_MHZ

        if not SimSettings.SimSettings().subGHz:
            if SimSettings.SimSettings().GHzModel == 'pister':
                rssi = self._rssiPister(mote, neighbor, distance)
            elif SimSettings.SimSettings().GHzModel == 'itu-rural-macro':
                hTransmitter = 2.5
                hBaseStation = 6
                #rssi = self._rssiITUUrbanMicro(mote, neighbor, freq, distance, hTransmitter, hBaseStation)
                rssi = self._rssiITURuralMacro(mote, neighbor, freq, distance, hTransmitter, hBaseStation)
            else:
                assert False
        elif SimSettings.SimSettings().subGHz:
            if SimSettings.SimSettings().subGHzModel == 'itu-rural-macro':
                hTransmitter = 2.5
                hBaseStation = 6
                rssi = self._rssiITURuralMacro(mote, neighbor, freq, distance, hTransmitter, hBaseStation)
            elif SimSettings.SimSettings().subGHzModel == 'ah-pico':
                rssi= self._rssiAHPico(mote, neighbor, freq, distance)
            else:
                assert False
        else:
            assert False

        return rssi

    def _computePDR(self,mote,neighbor):
        ''' computes pdr to neighbor according to RSSI'''

        rssi        = mote.getRSSI(neighbor)
        return self.rssiToPdr(rssi)

    @classmethod
    def rssiToPdr(self,rssi):
        '''
        rssi and pdr relationship obtained by experiment below
        http://wsn.eecs.berkeley.edu/connectivity/?dataset=dust
        '''

	#rate=250kbps
	brate=250
	#bw=500kbps
	bw=500

	if SimSettings.SimSettings().subGHz:
		S=-101.5		#cc1200
		snr = rssi - S
		EBN=snr - 10*math.log10(bw/brate)
		b=0.5 * sp.erfc(math.sqrt(10**((EBN*0.5)/10)))	#2-fsk
	else:
		S=-97			#cc2538
		snr = rssi - S
		EBN=snr - 10*math.log10(bw/brate)
		b=sp.erfc(math.sqrt(10**((EBN*0.5)/10)))	#OQPSK

	#we assume 128byte size packets
	pdr=(1-b)**(128*8)

#        pdr = None
#        if not SimSettings.SimSettings().subGHz:
#            # 2.4GHz
#            rssiPdrTable    = {
#                -97:    0.0000, # this value is not from experiment
#                -96:    0.1494,
#                -95:    0.2340,
#                -94:    0.4071,
#                #<-- 50% PDR is here, at RSSI=-93.6
#                -93:    0.6359,
#                -92:    0.6866,
#                -91:    0.7476,
#                -90:    0.8603,
#                -89:    0.8702,
#                -88:    0.9324,
#                -87:    0.9427,
#                -86:    0.9562,
#                -85:    0.9611,
#                -84:    0.9739,
#                -83:    0.9745,
#                -82:    0.9844,
#                -81:    0.9854,
#                -80:    0.9903,
#                -79:    1.0000, # this value is not from experiment
#            }

#            minRssi         = min(rssiPdrTable.keys())
#            maxRssi         = max(rssiPdrTable.keys())

#            if   rssi<minRssi:
#                pdr         = 0.0
#            elif rssi>maxRssi:
#                pdr         = 1.0
#            else:
#                floorRssi   = int(math.floor(rssi))
#                pdrLow      = rssiPdrTable[floorRssi]
#                pdrHigh     = rssiPdrTable[floorRssi+1]
#                pdr         = (pdrHigh-pdrLow)*(rssi-float(floorRssi))+pdrLow # linear interpolation
#        else:
#            # 868MHz
#            pdr = 1.0

        assert pdr>=0.0
        assert pdr<=1.0

        return pdr

    def _computeDistance(self,mote,neighbor):
        '''
        mote.x and mote.y are in km. This function returns the distance in m.
        '''

        return 1000*math.sqrt(
            (mote.x - neighbor.x)**2 +
            (mote.y - neighbor.y)**2
        )

#============================ main ============================================

def main():
    import Mote
    import SimSettings

    NOTVISITED     = 'notVisited'
    MARKED         = 'marked'
    VISITED        = 'visited'

    allRanks = []
    for _ in range(100):
        print '.',
        # create topology
        settings                           = SimSettings.SimSettings()
        settings.numMotes                  = 50
        settings.pkPeriod                  = 1.0
        settings.otfHousekeepingPeriod     = 1.0
        settings.sixtopPdrThreshold        = None
        settings.sixtopHousekeepingPeriod  = 1.0
        settings.minRssi                   = None
        settings.squareSide                = 2.0
        settings.slotframeLength           = 101
        settings.slotDuration              = 0.010
        settings.sixtopNoHousekeeping      = 0
        settings.numPacketsBurst           = None
        motes                              = [Mote.Mote(id) for id in range(settings.numMotes)]
        topology                           = Topology(motes)
        if settings.topology == 'random':
            print 'Creating a random topology.'
            topology.createTopology()
        elif settings.topology == 'grid':
            print 'Creating a grid topology.'
            topology.createTopologyGrid()

        # print stats
        hopVal    = {}
        moteState = {}
        for mote in motes:
            if mote.id==0:
                hopVal[mote]     = 0
                moteState[mote]  = MARKED
            else:
                hopVal[mote]     = None
                moteState[mote]  = NOTVISITED

        while (NOTVISITED in moteState.values()) or (MARKED in moteState.values()):

            # find marked mote
            for (currentMote,s) in moteState.items():
                if s==MARKED:
                   break
            assert moteState[currentMote]==MARKED

            # mark all of its neighbors with pdr >50%
            for neighbor in motes:
                try:
                    if currentMote.getPDR(neighbor)>0.5:
                        if moteState[neighbor]==NOTVISITED:
                            moteState[neighbor]      = MARKED
                            hopVal[neighbor]         = hopVal[currentMote]+1
                        if moteState[neighbor]==VISITED:
                            if hopVal[currentMote]+1<hopVal[neighbor]:
                                hopVal[neighbor]     = hopVal[currentMote]+1
                except KeyError as err:
                    pass # happens when no a neighbor

            # mark it as visited
            moteState[currentMote]=VISITED

        allRanks += hopVal.values()

    assert len(allRanks)==100*50

    print ''
    print 'average rank: {0}'.format(float(sum(allRanks))/float(len(allRanks)))
    print 'max rank:     {0}'.format(max(allRanks))
    print ''

    raw_input("Script ended. Press Enter to close.")

if __name__=="__main__":
    main()
