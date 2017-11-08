#!/bin/sh

#nodesInit=337
#maxNodes=338
nodesInit=2
nodesMax=2
alfa=2

###################default

rpl=10
otf=5
sixtop=5



nodes=$nodesInit

while [ $nodes -le $nodesMax ] 
do
   echo "Simulating with $nodes nodes...: runSimAllCPU.py $nodes $rpl $otf $sixtop" 


   #mkdir simData_sf0_rpl_$rpl\_otf_$otf\_sixtop_$sixtop 2&>/dev/null
   #mkdir simData_sf0_rpl_$rpl\-otf_$otf\-sixtop_$sixtop/simData_numMotes_$nodes 2&>/dev/null
   namedir="simData/journal"
   #namedirsub="simData_sf0_rpl_"$rpl"_otf_"$otf"_sixtop_"$sixtop"/simdata_numMotes_$nodes"
   #echo $namedir
   #echo $namedirsub
   mkdir `echo $namedir` 2> /dev/null
   #mkdir `echo $namedirsub` 2> /dev/null
   #mkdir topology-simData_$scheduler-$mobility\-hops$maxnumhops\-deBrasCells$numBr-numRadios$numRadios\_rpl_$rpl\_otf_$otf\_sixtop_$sixtop\_trafficType_$trafficType
   #mkdir topology-simData_$scheduler-$mobility\-hops$maxnumhops\-deBrasCells$numBr-numRadios$numRadios\_rpl_$rpl\_otf_$otf\_sixtop_$sixtop\_trafficType_$trafficType/maxNumHops_$maxnumhops\_mobilityModel_$mobility\_numDeBraSCells_$numBr\_numMotes_$nodes\_numRadios_$numRadios\_scheduler_$scheduler\_topology_$topo

   #echo "$namedirsub $nodes $rpl $otf $sixtop"
   python runSimAllCPUs.py $namedir $nodes $rpl $otf $sixtop
   python duplicate_cpus.py $namedir
   python runSimAllCPUs.py $namedir $nodes $rpl $otf $sixtop
   python duplicate_cpus.py $namedir
   python runSimAllCPUs.py $namedir $nodes $rpl $otf $sixtop
   python duplicate_cpus.py $namedir
   python runSimAllCPUs.py $namedir $nodes $rpl $otf $sixtop
   python duplicate_cpus.py $namedir
   python runSimAllCPUs.py $namedir $nodes $rpl $otf $sixtop
   python duplicate_cpus.py $namedir

#   python runSimAllCPUs.py $namedir $nodes $rpl $otf $sixtop
#   python duplicate_cpus.py $namedir

#   python runSimAllCPUs.py $namedir $nodes $rpl $otf $sixtop
#   python duplicate_cpus.py $namedir

#   python runSimAllCPUs.py $nodes $scheduler $numBr $rpl $otf $sixtop $topo $maxnumhops $squareSide $mobility $numRadios $trafficType
#   python duplicate_cpus.py simData_$scheduler-$mobility\-hops$maxnumhops\-deBrasCells$numBr-numRadios$numRadios\_rpl_$rpl\_otf_$otf\_sixtop_$sixtop\_trafficType_$trafficType
#   python runSimAllCPUs.py $nodes $scheduler $numBr $rpl $otf $sixtop $topo $maxnumhops $squareSide $mobility $numRadios $trafficType
#   python duplicate_cpus.py simData_$scheduler-$mobility\-hops$maxnumhops\-deBrasCells$numBr-numRadios$numRadios\_rpl_$rpl\_otf_$otf\_sixtop_$sixtop\_trafficType_$trafficType
#   python runSimAllCPUs.py $nodes $scheduler $numBr $rpl $otf $sixtop $topo $maxnumhops $squareSide $mobility $numRadios
#   python duplicate_cpus.py simData_$scheduler-$mobility\-hops$maxnumhops\-brcells$numBr-numRadios$numRadios\_rpl_$rpl\_otf_$otf\_sixtop_$sixtop
#   python runSimAllCPUs.py $nodes $scheduler $numBr $rpl $otf $sixtop $topo $maxnumhops $squareSide $mobility $numRadios
#   python duplicate_cpus.py simData_$scheduler-$mobility\-hops$maxnumhops\-brcells$numBr-numRadios$numRadios\_rpl_$rpl\_otf_$otf\_sixtop_$sixtop
#   python runSimAllCPUs.py $nodes $scheduler $numBr $rpl $otf $sixtop $topo $maxnumhops $squareSide $mobility $numRadios
#   python duplicate_cpus.py simData_$scheduler-$mobility\-hops$maxnumhops\-brcells$numBr-numRadios$numRadios\_rpl_$rpl\_otf_$otf\_sixtop_$sixtop
#   python runSimAllCPUs.py $nodes $scheduler $numBr $rpl $otf $sixtop $topo $maxnumhops $squareSide $mobility $numRadios
#   python duplicate_cpus.py simData_$scheduler-$mobility\-hops$maxnumhops\-brcells$numBr-numRadios$numRadios\_rpl_$rpl\_otf_$otf\_sixtop_$sixtop
#   python runSimAllCPUs.py $nodes $scheduler $numBr $rpl $otf $sixtop $topo $maxnumhops $squareSide $mobility $numRadios
#   python duplicate_cpus.py simData_$scheduler-$mobility\-hops$maxnumhops\-brcells$numBr-numRadios$numRadios\_rpl_$rpl\_otf_$otf\_sixtop_$sixtop
#   python runSimAllCPUs.py $nodes $scheduler $numBr $rpl $otf $sixtop $topo $maxnumhops $squareSide $mobility $numRadios
#   python duplicate_cpus.py simData_$scheduler-$mobility\-hops$maxnumhops\-brcells$numBr-numRadios$numRadios\_rpl_$rpl\_otf_$otf\_sixtop_$sixtop
#   python runSimAllCPUs.py $nodes $scheduler $numBr $rpl $otf $sixtop $topo $maxnumhops $squareSide $mobility $numRadios
#   python duplicate_cpus.py simData_$scheduler-$mobility\-hops$maxnumhops\-brcells$numBr-numRadios$numRadios\_rpl_$rpl\_otf_$otf\_sixtop_$sixtop
#   python runSimAllCPUs.py $nodes $scheduler $numBr $rpl $otf $sixtop $topo $maxnumhops $squareSide $mobility $numRadios
#   python duplicate_cpus.py simData_$scheduler-$mobility\-hops$maxnumhops\-brcells$numBr-numRadios$numRadios\_rpl_$rpl\_otf_$otf\_sixtop_$sixtop

   nodes=`expr $nodes + $alfa `

done
echo "Simulation done"



################################RPL

#rpl=5
#otf=5
#sixtop=1


#nodes=$nodesInit
#while [ $nodes -le $maxNodes ] 
#do
#   echo "Simulating with $nodes nodes...: runSimAllCPU.py $nodes $scheduler $numBr $numOverlap" 
#   mkdir simData_$scheduler\_rpl_$rpl\_otf_$otf\_sixtop_$sixtop
#   mkdir simData_$scheduler\_rpl_$rpl\_otf_$otf\_sixtop_$sixtop/numBroadcastCells_$numBr\_numMotes_$nodes\_overlappingBrCells_$numOverlap\_scheduler_$scheduler
#   python runSimAllCPUs.py $nodes $scheduler $numBr $numOverlap $rpl $otf $sixtop
#   nodes=`expr $nodes + $alfa `
#   
#done
#echo "Simulation done"

#rpl=15
#otf=5
#sixtop=1

#nodes=$nodesInit
#while [ $nodes -le $maxNodes ] 
#do
#   echo "Simulating with $nodes nodes...: runSimAllCPU.py $nodes $scheduler $numBr $numOverlap" 
#   mkdir simData_$scheduler\_rpl_$rpl\_otf_$otf\_sixtop_$sixtop
#   mkdir simData_$scheduler\_rpl_$rpl\_otf_$otf\_sixtop_$sixtop/numBroadcastCells_$numBr\_numMotes_$nodes\_overlappingBrCells_$numOverlap\_scheduler_$scheduler
#   python runSimAllCPUs.py $nodes $scheduler $numBr $numOverlap $rpl $otf $sixtop
#   nodes=`expr $nodes + $alfa `
#   
#done
##mv ./simData_rpl_1_otf_5_6top_1 ./$maxNodes\_$1\_numBr$numBr\_overlap$numOverlap\_$scheduler\_rpl_1_otf_5_6top_1
#echo "Simulation done"


###################otf

#nodes=$nodesInit
#while [ $nodes -le $maxNodes ] 
#do
#   echo "Simulating with $nodes nodes...: runSimAllCPU.py $nodes $scheduler $numBr $numOverlap" 
#   python runSimAllCPUs.py $nodes $scheduler $numBr $numOverlap 1 1 1
#   nodes=`expr $nodes + $alfa `
#done
#mv ./simData ./$maxNodes\_$1\_numBr$numBr\_overlap$numOverlap\_$scheduler\_rpl_1_otf_1_6top_1
#echo "Simulation done"

#nodes=$nodesInit
#while [ $nodes -le $maxNodes ] 
#do
#   echo "Simulating with $nodes nodes...: runSimAllCPU.py $nodes $scheduler $numBr $numOverlap" 
#   python runSimAllCPUs.py $nodes $scheduler $numBr $numOverlap 1 15 1
#   nodes=`expr $nodes + $alfa `
#done
#mv ./simData ./$maxNodes\_$1\_numBr$numBr\_overlap$numOverlap\_$scheduler\_rpl_1_otf_15_6top_1
#echo "Simulation done"



###################6top


#nodes=$nodesInit
#while [ $nodes -le $maxNodes ] 
#do
#   echo "Simulating with $nodes nodes...: runSimAllCPU.py $nodes $scheduler $numBr $numOverlap" 
#   python runSimAllCPUs.py $nodes $scheduler $numBr $numOverlap 1 5 5
#   nodes=`expr $nodes + $alfa `
#done
#mv ./simData ./$maxNodes\_$1\_numBr$numBr\_overlap$numOverlap\_$scheduler\_rpl_1_otf_5_6top_5
#echo "Simulation done"

#nodes=$nodesInit
#while [ $nodes -le $maxNodes ] 
#do
#   echo "Simulating with $nodes nodes...: runSimAllCPU.py $nodes $scheduler $numBr $numOverlap" 
#   python runSimAllCPUs.py $nodes $scheduler $numBr $numOverlap 1 5 15
#   nodes=`expr $nodes + $alfa `
#done
#mv ./simData ./$maxNodes\_$1\_numBr$numBr\_overlap$numOverlap\_$scheduler\_rpl_1_otf_5_6top_15
#echo "Simulation done"


#echo "Preparing results... in"

#ls -t ./$maxNodes\_$1\_numBr$numBr\_overlap$numOverlap | grep mysummary | grep $1  | sort -V | while read name
#do
#	echo "Reading $name"
#	totalol=0
#	totalth=0
#	olmote=0
#	thmote=0
#	nodes=0
#	while read line
#	do
#		
#		mote=`echo "$line" | awk '{print $2}'`
#		if [ $mote != '0' ]; then
#			olmote=`echo "$line" | awk '{print $8}'`
#			
#			totalol=`echo "$olmote+$totalol" | bc`
#			
#			nodes=`expr $nodes + 1`
#			#echo "$totalth"
#		else
#			thmote=`echo "$line" | awk '{print $13}'`
#			totalth=`echo "$thmote+$totalth" | bc`
#		fi
##echo "$name"
#	#node=`cat myresults/$name | awk '{print $8}'`
##echo `cat myresults/$name | awk '{print $8}'`
#	done < ./$maxNodes\_$1\_numBr$numBr\_overlap$numOverlap/$name
#	#echo $nodes
#	#echo $totalth
#	avol=`perl -E "say  $totalol/$nodes"`
#	avth=`perl -E "say  $totalth/$nodes"`
#	echo $nodes" "$avol" "$avth >> ./$maxNodes\_$1\_numBr$numBr\_overlap$numOverlap/results_$1.ods
#	echo "run.sh finished"
#done

#mv ./$maxNodes\_$1\_numBr$numBr\_overlap$numOverlap ./filter/simData$maxNodes
#cd filter
#bash ./gathering_info.sh $maxNodes $alfa $1
#cd ..
#mv ./filter/simData$maxNodes ./$maxNodes\_$1\_numBr$numBr\_overlap$numOverlap
#mv ./filter/data$maxNodes\_$1.ods ./data$maxNodes\_$1\_$numBr\_overlap$numOverlap.ods

#echo "Done"
