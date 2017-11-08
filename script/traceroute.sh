#!/bin/bash

LINKS=("130.102.82.61" "138.44.176.3" "112.137.142.4" "124.124.195.101" "155.232.32.14" "80.239.135.226" "84.237.50.25" "198.154.248.116" "143.107.249.34" "128.171.213.2" "188.44.50.103" "130.235.52.5" "194.199.156.25" "192.76.32.66" "132.247.70.37" "137.82.123.113" "128.227.9.98" "128.100.96.19" "132.216.177.160")
MAXHOPS=25
CP_TOBACKUP_INDEX=0
BACKUP_NUMBER=0

while true
do

	for link in "${LINKS[@]}"
	do
		: 
		LOCALCOMMAND="traceroute -m$MAXHOPS $link"
		TEMPTRACEROUTE=`($LOCALCOMMAND)`
		
		#echo "$TEMPTRACEROUTE"
		echo "Start time: " `date` >> IP_$link.txt
		echo "$TEMPTRACEROUTE"  >> IP_$link.txt
		echo "End time: " `date` >> IP_$link.txt
		echo "\n\n" >> IP_$link.txt
		sleep 2s
	done

#	if($CP_TOBACKUP_INDEX -eq 6) #every 12h do a backup of files
#	then
#		`mkdir ../backup_$BACKUP_NUMBER`
#		`cp -r ./ ../backup_$BACKUP_NUMBER`
#		`CP_TOBACKUP_INDEX=0`
#	fi
#	`let CP_TOBACKUP_INDEX++`

	`git add .`
	`git commit -m "backup_$BACKUP_NUMBER"`
	`git push origin master`

	sleep 6600 #sleep 1h50mins
done

