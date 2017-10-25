#!/bin/bash

LINKS=("unsw.edu.au" "unisa.ac.za" "mcgill.ca")
UNI_LIST=(unsw unisa mcgill)
INDEX=1

for link in "${LINKS[@]}"
do
	: 
	echo $INDEX
	echo "$link"
	#traceroute $link
	echo "`date`, google, toupin" >> log.csv
	((INDEX++))
done