import numpy as np
import matplotlib.pyplot as plt
import os
import collections
import operator
import subprocess
from pylab import *

import csv

def parse(filename):
	

    
    command="find "
    args='{0} -name output* | sort -V'.format(filename)
  
    #print "--- "+str(command+args)
    tmp = os.popen(command+args).read()
    listOfFiles=tmp.split("\n")
    data_dict={}
     
    currentNumNodes=None 
	
    for filename in listOfFiles:
        
	cycleInit=9999
   	cycleEnd=10000
        maxCycles=10000
	numSharedCells=5
	cycles=cycleEnd-cycleInit #end receiving - start receiving		
	if filename != "":
	    
	    print "Filtering: "+str(filename)
	    
            nodes=int(filename.split("/")[1].split("_")[1])
	    print "NODES "+str(nodes)

	    

	    if currentNumNodes==None or nodes!=currentNumNodes:
		currentNumNodes=nodes
		
		OL=[]
		throughput=[]

		PER=[]#not used here
		TXpkt=[]
		RXpkt=[]


		collisionDrops=[]
	        propagationDrops=[]
		joiningTime=[]
		allNodesHaveCellsTime=[]
		allNodesSendingTime=[]
		avgNeighbors=[]
		dropsMAC=[]
		dropsAPP=[]
		delay=[]
		battery=[]
		avgHops=[]
		avgHopsTopo=[]
		rplParentChanges=[]
		avgEffectiveCollided=[]
		numTx=[]
		numRx=[]
		avgRTX=[]#not used here
		usedCells=[]
		reqCells=[]
		randomSelections=[]
		txbroad=[]
		rxbroad=[]
		PERBroad=[]   #not used here
		otf_messages=[]
		avgsixtopdelay=[]
		
	    

            infile = open(filename, 'r')

	    	
	    dropsMAC_values=None
            dropsAPP_values=None
	    delay_values=None
	    rpl_values=None

	    battery_values=[]
	    avgHops_values=None
	    avgHopsTopo_values=None
	    avgEffectiveCollided_values=None
	    usedCells_values=0
            reqCells_values=0
	    randomSelections_values=None
	    txbroad_values=None
	    rxbroad_values=None
	    otf_messages_add=0
	    otf_messages_remove=0
	    otf_messages_values=None

#	    j=0
#	    for line in infile:
#		line=line.replace("\n", "")
#		re=[s for s in line.split(' ') if s]
#		if len(re)>12:		  
#		    if re[12]!='' and re[12]!="collidedTxs" and re[12]!="totalTX":
#			maxCycles=int(re[12])
#		j+=1

#	    maxCyclesIndex=j-1

#	    cycleSimInitIndex=maxCyclesIndex-200
#	    firstCycleIndex=maxCyclesIndex-maxCycles
#	    cycles=maxCyclesIndex-cycleSimInitIndex

#	    print "First cycle 0 is in: "+str(firstCycleIndex)
#	    print "measurements started at cycle: "+str(maxCycles-100)
#	    print "measurements start in index : "+str(cycleSimInitIndex)
#	    print "measurements and simulation ended at cycle: "+str(maxCycles)
#	    print "measurements ended at index: "+str(maxCyclesIndex)
	
	    
	    maxCyclesIndex=100	 

	    columnExperimentInit=0  	
	    rowInitExperiment=0
	    lengthData=0
	    rowInit=0
	    defaultInitExp=0
	    endOfData=False
	    numCyclesPerRun=0	

	    infile = open(filename, 'r')
	    i=0
	    for line in infile:

		line=line.replace("\n", "")
		vals=line.split()

		if len(line.split())<=1:
		    i+=1
		    continue

		firstChar=line.split()[0]
		secondWord=line.split()[1]

		if firstChar=='#':

		    rowInit=i+1		
		    columnExperimentInit=vals.index("zExperimentInit")-1
		    lengthData=columnExperimentInit+1

		   
	        if secondWord=='numMotes':

			numMotes=int(line.split()[3])
			print "motes "+str(numMotes)
			assert numMotes==nodes
			
				

	        if secondWord=='numCyclesPerRun':

			numCyclesPerRun=int(line.split()[3])
			print "numCyclesPerRun "+str(numCyclesPerRun)

		#print str(i)+" "+str(rowInitExperiment+numCyclesPerRun)
		##Parse last values after the dumps
		if rowInitExperiment!=0 and i>=rowInitExperiment+numCyclesPerRun-1:
		    
		    if endOfData==False:
			print "Finish dump!"
			endOfData=True
		    if firstChar=='#PktGen':
			OL.append(float(vals[-1])*128*8/(numMotes-1)/numCyclesPerRun)
		    if firstChar=='#PktReceived':
			throughput.append(float(vals[-1])*128*8/(numMotes-1)/numCyclesPerRun)

		##get the initial value of when the experiment started
		if defaultInitExp==0:
		    if rowInitExperiment==0 and len(vals)==lengthData:            
			defaultInitExp=vals[columnExperimentInit]			      
		
		if not endOfData:
	
			##Parse all the dumps
			if rowInit!=0 and i>=rowInit:	

			    TXpkt.append(vals[0])#pkt gen
			    RXpkt.append(vals[1])#pkt received at root
			    if float(vals[6])!=0.0:
				#print vals[6]
				avgsixtopdelay.append(float(vals[6])*0.01)

		##Parse the dumps of the experiment
		if len(vals) == lengthData and defaultInitExp!=vals[columnExperimentInit]:	
		    if rowInitExperiment==0:
		        rowInitExperiment=i

		    #print vals


		    #print last dump row
		    if i==rowInitExperiment+numCyclesPerRun:
			battery_values.append(float(line.split()[7]))
			   

		

		
		    

		

	
#		if i==maxCyclesIndex:	
#		        #print "2line "+str(i)+"->"+str(line)
#			OL.append(float(line.split(" ")[7])*128*8)
#			val=float(line.split(" ")[9])
#			print str(val*128*8)
#			throughput.append(val*128*8)

#			numTx.append(float(line.split(" ")[13]))
#			numRx.append(float(line.split(" ")[15]))
#			TXpkt.append(int(line.split(" ")[3]))
#			RXpkt.append(int(line.split(" ")[5]))
#			
#			collisionDrops.append(int(line.split(" ")[11]))
#	    		propagationDrops.append(int(line.split(" ")[17]))

#			joiningTime.append(int(line.split(" ")[19]))
#			allNodesHaveCellsTime.append(int(line.split(" ")[21]))
#			allNodesSendingTime.append(int(line.split(" ")[23]))
#			avgNeighbors.append(float(line.split(" ")[25]))
#			#avgRTX.append(float(line.split(" ")[15])/float(line.split(" ")[13]))
#			#PER.append(1-(int(line.split(" ")[5])/float(line.split(" ")[3])))			
#			#collisionDropsPer.append(float(line.split(" ")[11]))

#			
#			
#		#if i>=((35+((maxCycles+6)))-(maxCycles+6)) and i<=((35+((maxCycles+6)))-7):	#all values from cycle 0 to max cycle 
#		if i>=(cycleSimInitIndex) and i<(maxCyclesIndex-1):
#			#print "line "+str(i)+"->"+str(line)	
#			#print "Cycle "+str(int(line.split()[12]))
##			if int(line.split()[64])==numMotes-1:
##				if cycleInit==9999:
##					print "Nodes sending at "+str(int(line.split()[12])+20+numMotes*2/(numSharedCells*numRadios))
##					cycleInit=int(line.split()[12])+20+numMotes*2/(numSharedCells*numRadios)
##					maxCycles=cycleInit+100
##					cycles=maxCycles-cycleInit
#			if rpl_values!=None:	
#				rpl_values=int(line.split()[29])+int(rpl_values)
#			else:
#				rpl_values=int(line.split()[29])
#			#print int(line.split()[13])
#			if dropsMAC_values!= None:
#				dropsMAC_values=int(line.split()[14])+int(dropsMAC_values)
#			else:
#				dropsMAC_values=int(line.split()[14])
#			if dropsAPP_values!= None:
#				dropsAPP_values=int(line.split()[13])+int(dropsAPP_values)
#			else:
#				dropsAPP_values=int(line.split()[13])
#			if txbroad_values!=None:
#				txbroad_values=int(line.split()[40])+int(txbroad_values)
#			else:
#				txbroad_values=int(line.split()[40])
#			if rxbroad_values!=None:
#				rxbroad_values=int(line.split()[34])+int(rxbroad_values)
#				
#			else:
#				rxbroad_values=int(line.split()[34])
#			#print otf_messages_values	
#			if otf_messages_values!=None:
#				otf_messages_add=int(line.split()[25])+int(otf_messages_add)
#				otf_messages_remove=int(line.split()[26])+int(otf_messages_remove)
#				otf_messages_values=otf_messages_add+otf_messages_remove
#			else:
#				otf_messages_add=int(line.split()[25])
#				otf_messages_remove=int(line.split()[26])
#				otf_messages_values=otf_messages_add+otf_messages_remove
##			if randomSelections_values!=None:
##				randomSelections_values=int(line.split()[19])+int(randomSelections_values)
##			else:
##				randomSelections_values=int(line.split()[19])
#			
#			#if i>=((35+cycleInit+((maxCycles+6)))-(maxCycles+6)) and i<=((35+((maxCycles+6)))-7):  #all values from initcycle to endcycle
#			if i>=(firstCycleIndex) and i<(maxCyclesIndex-1):
#				#print "line "+str(i)+"->"+str(line)

#				#print int(line.split()[12])
#				if avgEffectiveCollided_values!=None:	
#					avgEffectiveCollided_values=int(line.split()[18])+int(avgEffectiveCollided_values)
#				else:
#					avgEffectiveCollided_values=int(line.split()[18])
#				if delay_values!=None:	
#					delay_values=float(line.split()[7])+float(delay_values)
#					#print float(line.split()[7])
#				else:
#					delay_values=float(line.split()[7])
#				#print float(line.split()[7])
#				if avgHops_values!=None:	
#					avgHops_values=float(line.split()[5])+float(avgHops_values)
#					#print str(float(line.split()[5]))
#				else:
#					avgHops_values=float(line.split()[5])
#				#print float(line.split()[5])
#				if avgHopsTopo_values!=None:	
#					avgHopsTopo_values=float(line.split()[6])+float(avgHopsTopo_values)
#				else:
#					avgHopsTopo_values=float(line.split()[6])
#				#print str(i)+" PPP "+str(line.split()[5])
#				usedCells_values=float(line.split()[24])+float(usedCells_values)
#				reqCells_values=float(line.split()[20])+float(reqCells_values)
#				#print "cycle "+str(line.split()[12]) + " hops "+str(line.split()[5])
#			if i==(maxCyclesIndex-2):
#				#print str(i)+" BATTERY "+str(float(line.split()[10]))
#				battery_values.append(float(line.split()[10]))
#				randomSelections_values=int(line.split()[19])
#				
#		else:
#			if rpl_values!=None:
#				#print rplParentChanges
#				#print rpl_values
#				#print numMotes
#				rplParentChanges.append(float(rpl_values))
#				#print rplParentChanges
#				rpl_values=None
#			if dropsMAC_values!=None:
#				dropsMAC.append(int(dropsMAC_values))
#				dropsMAC_values=None
#			if dropsAPP_values!=None:	
#				dropsAPP.append(int(dropsAPP_values))
#				dropsAPP_values=None
#			if delay_values!=None:				
#				delay.append(float(0.01*delay_values/cycles))
#				delay_values=None
#			if battery_values!=[]:
#				battery_values=[num for num in battery_values if num ]	
#				battery.append(np.mean(battery_values)/numMotes)
#				battery_values=[]
#			if avgHops_values!=None:
#				if avgHops_values/(cycles) < 1:	
#				    avgHops.append(1)	
#				else:			
#				    avgHops.append(avgHops_values/(cycles))	
#				#print avgHops_values
#				#print (cycles)		
#				avgHops_values=None
#			if avgHopsTopo_values!=None:
#				if avgHopsTopo_values/(cycles) < 1:	
#				    avgHopsTopo.append(1)	
#				else:			
#				    avgHopsTopo.append(avgHopsTopo_values/(cycles)/(numMotes-1))				
#					
#				#print avgHopsTopo_values
#				#print (cycles)	
#				avgHopsTopo_values=None
#			if reqCells_values!=0:
#				reqCells.append(reqCells_values/cycles)		
#				reqCells_values=0
#			if usedCells_values!=0:
#				usedCells.append(usedCells_values/cycles)		
#				usedCells_values=0
#			if txbroad_values!=None:	
#				txbroad.append(int(txbroad_values))
#				txbroad_values=None
#			if rxbroad_values!=None:	
#				rxbroad.append(int(rxbroad_values))
#				rxbroad_values=None
#			if avgEffectiveCollided_values!=None:	
#				avgEffectiveCollided.append(int(avgEffectiveCollided_values/cycles))
#				avgEffectiveCollided_values=None
#			if randomSelections_values!=None:	
#				randomSelections.append(int(randomSelections_values))
#				randomSelections_values=None
#			if otf_messages_values!=None:	 
#				otf_messages.append(int(otf_messages_values))
#				otf_messages_values=None
#				otf_messages_add=0
#				otf_messages_remove=0
		
		if battery_values!=[]:
			battery_values=[num for num in battery_values if num ]	
			battery.append(np.mean(battery_values)/numMotes)
			battery_values=[]		

	        i+=1
	    #data_dict[int(nodes)]=(OL,throughput,PER,TXpkt,RXpkt,(np.mean(collisionDrops)/np.mean(numTx)),(np.mean(propagationDrops)/np.mean(numTx)),dropsMAC,dropsAPP,delay,battery,avgHops,rplParentChanges,avgEffectiveCollided,numTx,numRx,usedCells,reqCells,randomSelections,txbroad,rxbroad)
	    data_dict[int(nodes)]=(OL,throughput,PER,TXpkt,RXpkt,collisionDrops,propagationDrops,dropsMAC,dropsAPP,delay,battery,avgHops,rplParentChanges,avgEffectiveCollided,numTx,numRx,usedCells,reqCells,randomSelections,txbroad,rxbroad,otf_messages,avgHopsTopo,joiningTime,allNodesHaveCellsTime,allNodesSendingTime,avgNeighbors,avgsixtopdelay)    	       	    

#data.append([(nodes,throughput)])


			
    print "End parsing"
    print data_dict

    


    return data_dict
    


def plot_image(parsed_data,filenumber, column):
    
    	print "Ploting Image"
    	
	
        print "There are sets: "+str(len(parsed_data[0][parsed_data[0].keys()[0]][0]))
	
        print "Ploting results of column "+str(column)
   	
#    for i in range(len(parsed_data[0][2])):  ##example first simulation, usually there is always a network with 2 nodes, key=2
#	    print "VAR "+str(i)
        data_to_plot=[]
        yerr=[]


        parameter_translator={1: ['0','OL'], 2: ['1','Throughput'], 3: ['x','PER'], 4: ['3','TXpkts'],5: ['4','RXpkts'],6: ['5','dropsCollisions'],7: ['6','dropsPorpagation'],8: ['7','dropsMAC'],9: ['8','dropsAPP'],10: ['10','battery'],11: ['11','avgHops'],12: ['12','rplChanges'],13: ['13','effectiveCollided'],14: ['14','numTx'],15: ['15','numRx'],16: ['x','RTX'],17: ['16','usedCells'],18: ['17','ReqCells'],19: ['18','RandomSelection'],20: ['19','txbroad'],21: ['20','rxbroad'],22: ['x','PERBroad'],23: ['9','delay'], 24: ['21','otfMessages'], 25: ['x','PERDropColl'], 26: ['x','PERDropProp'],27: ['22','aveHopsTopo'],28: ['23','joiningTime'],29:['24','AllNodesHaveTxCellsTime'],30:['25','AllNodesSendingTime'],31:['26','avgNeighbors'],32:['27','avgsixtopdelay'] }



    
    	
	data_dict=parsed_data[filenumber]
	#print data_dict
	print "There are variables to plot: "+str(len(data_dict))
	print "But I am going to display column: "+str(column)
	print "I am going to display column: "+str(parameter_translator[int(column)])
	#assert False
	#print "I am going to display column: "+str(parameter_translator[column].items()[0])
	data=[]
	

	for value in sorted(data_dict.keys()):
	    data.append((value,data_dict[value]))             
	    #print "For value "+str(value)+" data "+str(data_dict[value])
	
	#for item2 in data:
		#print item2[1][int(parameter_translator[int(column)][0])]

	
	x=[item[0] for item in data]

	if parameter_translator[int(column)][0]!='x':

		lenSets=[len(item3[1][1]) for item3 in data]
		for item2 in data:	
			print "For value data "+str(item2[1][int(parameter_translator[int(10)][0])])
		data_to_plot.append([np.mean(item[1][int(parameter_translator[int(column)][0])]) for item in data])
		
		yerr.append([sqrt(np.var(item[1][int(parameter_translator[int(column)][0])])) for item in data])
		   

		return x, data_to_plot,yerr,parameter_translator[int(column)][1]
	else:
		if parameter_translator[int(column)][1]=='PER':
			per=[]
			for item in data:
				#data_to_plot.append(item[1][5]/item[1][4])
				tx=item[1][int(parameter_translator[int(4)][0])]
				rx=item[1][int(parameter_translator[int(5)][0])]	
				per.append([(1-float(a)/b) for a,b in zip(rx,tx)])


			data_to_plot.append([np.mean(item) for item in per])
			yerr.append([sqrt(np.var(item)) for item in per])
			print len(data_to_plot)
			return x, data_to_plot,yerr,parameter_translator[int(column)][1]
		elif parameter_translator[int(column)][1]=='RTX':
			rtx=[]
			print "RTX"
			for item in data:
				#data_to_plot.append(item[1][5]/item[1][4])
				tx=item[1][int(parameter_translator[int(14)][0])]				
				rx=item[1][int(parameter_translator[int(15)][0])]	
				rtx.append([float(a)/b for a,b in zip(tx,rx)])

				
			data_to_plot.append([np.mean(item) for item in rtx])
			print len(data_to_plot)
			yerr.append([sqrt(np.var(item)) for item in rtx])
			return x, data_to_plot,yerr,parameter_translator[int(column)][1]
		elif parameter_translator[int(column)][1]=='PERBroad':
			perbroad=[]

			for item in data:
				#data_to_plot.append(item[1][5]/item[1][4])
				tx=item[1][int(parameter_translator[int(20)][0])]				
				rx=item[1][int(parameter_translator[int(21)][0])]
				val=[]
				for i in range(len(rx)):
					if rx[i]!=0:
						val.append(rx[i]/tx[i])
					else:
						val.append(0)
				perbroad.append(val)
			
			data_to_plot.append([np.mean(item) for item in perbroad])
			
			yerr.append([sqrt(np.var(item)) for item in perbroad])
			return x, data_to_plot,yerr,parameter_translator[int(column)][1]

		elif parameter_translator[int(column)][1]=='PERDropColl':
			perbroad=[]

			for item in data:
				#data_to_plot.append(item[1][5]/item[1][4])
				tx=item[1][int(parameter_translator[int(14)][0])]
				rx=item[1][int(parameter_translator[int(15)][0])]			
				col=item[1][int(parameter_translator[int(6)][0])]
				
				val=[]
				for i in range(len(col)):
					if col[i]!=0:
						val.append(col[i]/(tx[i]-rx[i]))
					else:
						val.append(0)
				perbroad.append(val)
			
			data_to_plot.append([np.mean(item) for item in perbroad])
			
			yerr.append([sqrt(np.var(item)) for item in perbroad])
			return x, data_to_plot,yerr,parameter_translator[int(column)][1]
		elif parameter_translator[int(column)][1]=='PERDropProp':
			perbroad=[]

			for item in data:
				#data_to_plot.append(item[1][5]/item[1][4])
				tx=item[1][int(parameter_translator[int(14)][0])]
				rx=item[1][int(parameter_translator[int(15)][0])]			
				prop=item[1][int(parameter_translator[int(7)][0])]
				val=[]
				for i in range(len(prop)):
					if prop[i]!=0:
						val.append(prop[i]/(tx[i]-rx[i]))
						
					else:
						val.append(0)
					print val
				perbroad.append(val)
			
			data_to_plot.append([np.mean(item) for item in perbroad])
			
			yerr.append([sqrt(np.var(item)) for item in perbroad])
			return x, data_to_plot,yerr,parameter_translator[int(column)][1]

		else:
			assert False

def write_in_file(namefile,data_dict,fileset):

    data_to_write=[]
    
    print "There are sets: "+str(len(data_dict))
    print "Printing results in file: "+namefile

    data=[]

    for value in sorted(data_dict.keys()):
        data.append((value,data_dict[value]))

    numNodes=([item[0] for item in data]) 

    
       

    data_to_write.append([np.mean(item[1][0]) for item in data]) #OL    
    data_to_write.append([np.mean(item[1][1]) for item in data]) #throughput

    #print data_to_write
    data_to_write.append([(1-np.mean(item[1][4])/np.mean(item[1][3])) for item in data]) # PER
    data_to_write.append([np.mean(item[1][3]) for item in data]) # txpkt
    data_to_write.append([np.mean(item[1][4]) for item in data]) #rxpkt
    data_to_write.append([np.mean(item[1][5]) for item in data]) #drops collision
    data_to_write.append([np.mean(item[1][6]) for item in data]) #drops propagation
    data_to_write.append([np.mean(item[1][7]) for item in data]) # dropsmac
    data_to_write.append([np.mean(item[1][8]) for item in data]) #dropsapp
    data_to_write.append([np.mean(item[1][10]) for item in data]) # battery
    data_to_write.append([np.mean(item[1][11]) for item in data]) # avghops
    data_to_write.append([(np.mean(item[1][12])) for item in data]) # rplChanges
    data_to_write.append([np.mean(item[1][13]) for item in data]) # collided cells
    data_to_write.append([np.mean(item[1][14]) for item in data]) # numtx
    data_to_write.append([np.mean(item[1][15]) for item in data]) # numrx
    data_to_write.append([(np.mean(item[1][14])/np.mean(item[1][15])) for item in data]) # RTX
    data_to_write.append([np.mean(item[1][16]) for item in data]) # usedcells
    data_to_write.append([np.mean(item[1][17]) for item in data]) # reqcells
    data_to_write.append([np.mean(item[1][18]) for item in data]) # random selections
    data_to_write.append([np.mean(item[1][19]) for item in data]) # txbroad
    data_to_write.append([np.mean(item[1][20]) for item in data]) # rxbroad
    
    

    if np.mean(item[1][20])==0:
	data_to_write.append([np.mean(item[1][19]) for item in data])
    else:
    	data_to_write.append([(np.mean(item[1][20])/np.mean(item[1][19])) for item in data]) # PER broad

    data_to_write.append([np.mean(item[1][9]) for item in data]) # delay
    data_to_write.append([np.mean(item[1][21]) for item in data]) # otf messages
    data_to_write.append([np.mean(item[1][22]) for item in data]) # hopstopo
    data_to_write.append([np.mean(item[1][23]) for item in data]) # joining time
    data_to_write.append([np.mean(item[1][24]) for item in data]) # all nodes have cells time
    data_to_write.append([np.mean(item[1][25]) for item in data]) # all nodes sending time
    data_to_write.append([np.mean(item[1][26]) for item in data]) # avg neighbors time

    with open(namefile,'a+') as csvfile:
	
	spamwriter = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
	algth=fileset.split("_")[1].split("-")[0]
	mobi=fileset.split("_")[1].split("-")[1]
	hops=fileset.split("_")[1].split("-")[2]
	brcells=fileset.split("_")[1].split("-")[3]
	text=[algth,mobi,hops,brcells,""]
	spamwriter.writerow(text)
	content=["Nodes","OL","Throughput","PER","TX","RX","DropsCollisions","dropsPropagation","DropsMAC","DropsAPP","battery","avgHops","rplChanges","avgEffectiveCollided","numTx","numRx","avgRTX","usedCells","ReqCells","randomSelections","txbroad","rxbroad","PERBroad","delay","otfmessages","HopsTopo","joiningTime","allNodesHaveCellsTime","allNodesSendingTime","avgNeighbors","avgsixtopdelay"]
	



	spamwriter.writerow(content)
	for i in range(len(numNodes)):
		if data_to_write[2][i]<0:
			data_to_write[2][i]=0
		if data_to_write[15][i]<0:
			data_to_write[15][i]=0
		if data_to_write[20][i]<0:
			data_to_write[20][i]=0

		content=[numNodes[i],data_to_write[0][i],data_to_write[1][i],data_to_write[2][i],data_to_write[3][i],data_to_write[4][i],data_to_write[5][i],data_to_write[6][i],data_to_write[7][i],data_to_write[8][i],data_to_write[9][i],data_to_write[10][i],data_to_write[11][i],data_to_write[12][i],data_to_write[13][i],data_to_write[14][i],data_to_write[15][i],data_to_write[16][i],data_to_write[17][i],data_to_write[18][i],data_to_write[19][i],data_to_write[20][i],data_to_write[21][i],data_to_write[22][i],data_to_write[23][i],data_to_write[24][i],data_to_write[25][i],data_to_write[26][i],data_to_write[27][i],data_to_write[28][i]]
	
		spamwriter.writerow(content)
 
def autolabel(rects):
	for rect in rects:
		height = rect.get_height()
		ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
			'%d' % int(height),
			ha='center',            # vertical alignment
			va='bottom'             # horizontal alignment
			)
   

def print_help():
	print "This program needs arguments, ie:"
	print "To parse: parser.py parse dir1 dir2 dirN"
	print "To plot: parser.py plot parameter_to_plot dir1 dir2 dirN"
	print "To compare two parameter: parser.py comparison parameter1_to_plot parameter2_to_plot dir1"
	print "To plot parameter in bars: parser.py plot-bars parameter_to_plot dir1 dir2 dirN"
	print "To plot parameter in CDF: parser.py cdf parameter_to_plot dir1 dir2 dirN"
	print "The parameters available are:"

	print "OL"
	print "Throughput"

	parameter_translator={1: ['0','OL'], 2: ['1','Throughput'], 3: ['x','PER'], 4: ['3','TXpkts'],5: ['4','RXpkts'],6: ['5','dropsCollisions'],7: ['6','dropsPorpagation'],8: ['7','dropsMAC'],9: ['8','dropsAPP'],10: ['10','battery'],11: ['11','avgHops'],12: ['12','rplChanges'],13: ['13','effectiveCollided'],14: ['14','numTx'],15: ['15','numRx'],16: ['x','RTX'],17: ['16','usedCells'],18: ['17','ReqCells'],19: ['18','RandomSelection'],20: ['19','txbroad'],21: ['20','rxbroad'],22: ['x','PERBroad'],23: ['9','delay'], 24: ['21','otfMessages'], 25: ['x','PERDropColl'], 26: ['x','PERDropProp'],27: ['22','aveHopsTopo'], 28: ['23','joiningTime'],29:['24','AllNodesHaveTxCellsTime'],30:['25','AllNodesSendingTime'],31:['26','avgNeighbors'],32:['27','avgsixtopdelay']}
	#parameter_translator={1: ['0','OL'], 2: ['1','Throughput']}
	for col in parameter_translator.items():
		print str(col[0])+" "+str(col[1][1])

if __name__ == '__main__':

    



    

#    y_values=[e for number in xrange(2)]
#    yerr_values=[e for number in xrange(2)]



    maxYvalue=0
    #colors_dic={0: 'bo', 1: 'ro-',2: 'ko-',3: 'yo-',4: 'b*--',5: 'r*--',6: 'k*--',7: 'y*--',8: 'y*-',9: 'y*-',10: 'y*-',11: 'y*-'}
    colors_dic={0: 'bo-', 1: 'r^-',2: 'bo-',3: 'b^-',4: 'ko-',5: 'k^-',6: 'k*--',7: 'y*--',8: 'y*-',9: 'y*-',10: 'y*-',11: 'y*-'}
    #legend_dic={0: 'OTF-sf0 avgHops=1 (star topology)', 1: 'OTF-sf0 avgHops=3.4 (mesh)'} #1 and 2
    #legend_dic={0: 'Propagation Drops', 1: 'Collision Drops'} #3
    legend_dic={0: '1 Radio Sim', 1: '4 Radios Sim',2: '8 Radios Sim',3: '16 Radios Sim',4: '1 Radio Model',5: '4 Radios Model',6: '8 Radios Model',7: '16 Radios Model',8: 'debras8',9: 'debras9',10: 'debras10',11: 'opt2'} #4 # 5
    #legend_dic={0: 'Centralized', 1: 'Decentralized'} #6
    #legend_dic={0: 'OTF-sf0 Multichannel', 1: 'DeBraS Multichannel NumBr=6',2: 'Quasi-opimal Multichannel',3: 'DeBraS Multichannel NumBr=6'} #3
    legend_dic={0:'Constant SF0',1: 'Constant llsf', 2:'Pareto SF0', 3:'Pareto DeBraS',4:'Bursty SF0',5:'Bursty DeBraS'}
    print sys.argv

    if len(sys.argv) >= 2:


	#PARSE STATS TO A FILE ##################################################################################

	if sys.argv[1] == 'parse': 
		print "Starting to parse..."
		y_values=[e for number in xrange(len(sys.argv)-2)]
   		yerr_values=[e for number in xrange(len(sys.argv)-2)]
		parsed_data=[]
		filesets=[]
		for i in range(len(sys.argv)-2):
			print "Searching in dir: "+sys.argv[i+2];
			if sys.argv[i+2][len(sys.argv[i+2])-1]=='/':  #check no / is in the name
				sys.argv[i+2]=sys.argv[i+2][:-1]
			print "Searching in dir: "+sys.argv[i+2];
			filesets.append(sys.argv[i+2])
			parsed_data.append(parse(sys.argv[i+2]))
		i=0
		for data_dict in parsed_data:
			write_in_file("./results.ods",data_dict,filesets[i])
			i+=1


	#PLOT STATS ##################################################################################

	elif sys.argv[1] == 'plot': 
		print "Starting to plot..."
		y_values=[e for number in xrange(len(sys.argv)-2)]
   		yerr_values=[e for number in xrange(len(sys.argv)-2)]

		print "There are files: "+str(len(sys.argv)-3)
		if len(sys.argv) < 4:
			print_help()
		elif int(sys.argv[2]) == 0 or int(sys.argv[2]) > 33:
			print "Parameter "+str(sys.argv[2])+" not available"
			print_help()
		else:	

			#print sys.argv[3]
			
			parsed_data=[]
		        fig=plt.figure()
			ax=plt.subplot(111)

			for i in range(len(sys.argv)-3):
				print "Reading file: "+sys.argv[i+3];
				parsed_data.append(parse(sys.argv[i+3]))


			nodes=[keys for keys in parsed_data[0].keys()]
			print "Parse done. There are nodes: "+str(max(nodes))	
			#print parsed_data[0][32]
			for i in range(len(sys.argv)-3):	
				[x,y_values[i],yerr_values[i],title]=plot_image(parsed_data,i, sys.argv[2] )		
				print "adding ..."+str(y_values[i])				
	    			plt.errorbar(x, y_values[i][0], yerr=yerr_values[i][0],fmt=colors_dic[i],label=legend_dic[i],markersize=10)
				if maxYvalue<float(max(y_values[i][0])):
					maxYvalue=float(max(y_values[i][0]))
			#plt.title(title)
			plt.xlabel('# nodes',fontsize=18)
			
			#plt.ylabel('MAC Retransmissions (RTX)',fontsize=15)
			plt.ylabel('Throughput per node (bps)',fontsize=20)
			ax.legend(loc='center', bbox_to_anchor=(0.81, 0.25),ncol=1, fancybox=True, shadow=True)
			#ax.legend(loc='upper right',ncol=1, fancybox=True, shadow=True)
			#plt.legend( loc=2, borderaxespad=0.)
			if maxYvalue==0:
				plt.ylim(0, 1)
			else:
				plt.ylim(0, float(maxYvalue)*1.1)
		        #plt.ylim(0, 10)
			#plt.xlim(0, max(nodes))
			plt.xlim(0, 25)
			#plt.xlim(0, 210)
			plt.grid(True)
			plt.show()

	#COMPARISON BETWEEN TWO STATS ##################################################################################

	elif sys.argv[1] == 'comparison': 
		print len(sys.argv)
		if len(sys.argv) == 5:
			y_values=[e for number in xrange(len(sys.argv)-1)]
	  		yerr_values=[e for number in xrange(len(sys.argv)-1)]

			parsed_data=[]
			fig=plt.figure()
			ax=plt.subplot(111)
			print "Reading file: "+sys.argv[4];
			parsed_data.append(parse(sys.argv[4]))
			print "Parse done"
			nodes=[keys for keys in parsed_data[0].keys()]
	
			[x,y_values[0],yerr_values[0],title]=plot_image(parsed_data,0, sys.argv[2] )	
			plt.errorbar(x, y_values[0][0], yerr=yerr_values[0][0],fmt=colors_dic[0],label=legend_dic[0],markersize=10)

			[x,y_values[1],yerr_values[1],title]=plot_image(parsed_data,0, sys.argv[3] ) # number of hops
	
			if maxYvalue<float(max(y_values[1][0])):
				maxYvalue=float(max(y_values[1][0]))
			if maxYvalue<float(max(y_values[0][0])):
				maxYvalue=float(max(y_values[0][0]))

			plt.errorbar(x, y_values[1][0], yerr=yerr_values[1][0],fmt=colors_dic[1],label=legend_dic[1],markersize=10)
		
			#plt.legend( loc=2, borderaxespad=0.)
			ax.legend(loc='center', bbox_to_anchor=(0.5, 1.02),ncol=1, fancybox=True, shadow=True)
			plt.xlabel('# nodes',fontsize=13)
			plt.ylabel('Drops to TXs ratio (%)',fontsize=15)
		    	plt.ylim(0, float(maxYvalue)*1.1)
			plt.xlim(0, 1616)
			
			plt.grid(True)
			plt.show()
		else:
			print_help()


	#BARS##################################################################################


	elif sys.argv[1] == 'plot-bars': 
		print "Starting to plot some bars..."
		y_values=[e for number in xrange(len(sys.argv)-2)]
   		yerr_values=[e for number in xrange(len(sys.argv)-2)]

		listOfYValues=[]
		listOfYErrValues=[]

		print "There are files: "+str(len(sys.argv)-2)
		if len(sys.argv) < 4:
			print_help()
		elif int(sys.argv[2]) == 0 or int(sys.argv[2]) > 27:
			print "Parameter "+str(sys.argv[2])+" not available"
			print_help()
		else:
			parsed_data=[]
		        plt.subplots()
			for i in range(len(sys.argv)-3):
				print "Reading file: "+sys.argv[i+3];
				print i
				parsed_data.append(parse(sys.argv[i+3]))
			nodes=[keys for keys in parsed_data[0].keys()]
			print "Parse done. There are nodes: "+str(max(nodes))	
			#print parsed_data[0][32]
			val=0

			for i in range(len(sys.argv)-3):	
				[x,y_values[i],yerr_values[i],title]=plot_image(parsed_data,i, sys.argv[2] )		
				print "adding ..."+str(y_values[i])
				val=np.mean(y_values[i][0])
				errval=np.mean(yerr_values[i][0])
				listOfYValues.append(val)
				listOfYErrValues.append(errval)				
	    			#plt.errorbar(x, y_values[i][0], yerr=yerr_values[i][0],fmt=colors_dic[i],label=legend_dic[i])

			
			print listOfYValues
			print listOfYErrValues
			print "There are files: "+str(len(sys.argv)-2)
			plt.bar(range(len(sys.argv)-3), listOfYValues, yerr=listOfYErrValues, alpha=0.5, color=['red', 'green', 'blue', 'cyan', 'magenta'],error_kw=dict(ecolor='gray', lw=2, capsize=5, capthick=2), align='center')
				
			plt.margins(0.02)

			plt.ylabel('Throughput per node (bps)',fontsize=30)
			plt.legend( loc=1, borderaxespad=0.)
			plt.xticks([0,1,2,3,4,5], ['RPGM\n SF0', 'RWM\n DeBraS', 'StaticRay\n SF0', 'StaticUni\n DeBraS','Static\n SF0','Bursty\n DeBraS'],fontsize=20)
			#plt.yticks([500,600,700,800,900,1000], ['500', '600', '700', '800','900','1000'],fontsize=16)
			#plt.ylim(, 1000)
			plt.show()

 

	#CDF##################################################################################


	elif sys.argv[1] == 'cdf': 

		#fig, ax = plt.subplots(figsize=(8, 4))
		colors={0: 'blue',1: 'red',2: 'black',3: 'green',4: 'pink',5: 'purple',6: 'orange',}
		print "Starting to plot..."
		y_values=[e for number in xrange(len(sys.argv)-2)]
   		yerr_values=[e for number in xrange(len(sys.argv)-2)]
		print "Parameter "+str(sys.argv[2])+""
		

		print "There are files: "+str(len(sys.argv)-3)
		if len(sys.argv) < 4:
			print_help()
		elif int(sys.argv[2]) == 0 or int(sys.argv[2]) > 28:
			print "Parameter "+str(sys.argv[2])+" not available"
			print_help()
		else:	
			parsed_data=[]
		        fig=plt.figure()
			ax=plt.subplot(111)
			i=0
			for i in range(len(sys.argv)-3):
				print "Reading file: "+sys.argv[i+3];
				#print i
				m=sys.argv[i+3].split('/')
				if m[0]=='modelResults':
					parsed_data.append(parseModel(sys.argv[i+3]))
				else:
					parsed_data.append(parse(sys.argv[i+3]))
			 
				#lengdata=len(sys.argv)-3)			

				
			
				#fig=plt.figure()
				nodes=[keys for keys in parsed_data[i].keys()]
				print "Parse done. There are nodes: "+str(max(nodes))	

				val=int(sys.argv[2])-1
				print "Parameter "+str(val)
				print parsed_data[0][max(nodes)][val]

				#for 868MHz, only 64 for byte size packets
				j=0
				for valu in parsed_data[i][max(nodes)][val]:
					parsed_data[i][max(nodes)][val][j]=valu
					j+=1
				

							
				data = parsed_data[i][max(nodes)][val]
				
				N=len(parsed_data[i][max(nodes)][val])
				print data

				# sort the data:
				data_sorted = np.sort(data)

				# calculate the proportional values of samples
				p = 1. * np.arange(len(data)) / (len(data) - 1)

				# plot the sorted data:
				#values.append(data_sorted)
				#pvalues.append(p)
				#plt.plot(data_sorted,p,c=colors_dict[i],label=legend_dic[i])
				plt.plot(data_sorted,p,colors_dic[i],label=legend_dic[i],markersize=14)
				
			plt.ylim(0, 1)
			#plt.xlim(0, 400000)

			plt.ylabel('CDF',fontsize=50)
			plt.xlabel('Number of drops (pkts)',fontsize=50)
			plt.xticks([0,10000,20000,30000,40000,50000,60000,70000], ['0', '100k', '200k', '300k','400k','500k','600k','700k'],fontsize=30)
			plt.yticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1], ['0', '0.1', '0.2', '0.3','0.4','0.5','0.6','0.7','0.8','0.9','1'],fontsize=25)
			#plt.legend( loc=0, borderaxespad=0.)
			ax.legend(loc='center', bbox_to_anchor=(0.85, 0.2),ncol=1, fancybox=True, shadow=True,prop={'size':30},)
			plt.show()
			
	else:
		
		print_help()
	

    else:
       print_help()
	

