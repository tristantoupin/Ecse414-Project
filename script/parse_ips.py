import sys, os
import re


'''
EXAMPLE =>
Start time:  Wed 8 Nov 2017 16:09:27 EST
 1  gateway (142.157.26.2)  15.036 ms  13.751 ms  11.963 ms
 2  internet2-vlan687.gw.mcgill.ca (132.216.255.123)  9.366 ms  15.869 ms  11.313 ms
 3  vtelinet-216-66-110-108.vermontel.net (216.66.110.108)  20.936 ms  22.622 ms  21.536 ms
 4  10ge4-13.core1.nyc5.he.net (209.51.172.25)  26.818 ms  25.823 ms  26.794 ms
 5  100ge4-2.core1.nyc4.he.net (184.105.213.217)  34.478 ms  24.703 ms  27.582 ms
 6  100ge4-1.core1.par2.he.net (184.105.81.78)  107.450 ms  97.318 ms  98.604 ms
 7  100ge5-2.core1.fra1.he.net (72.52.92.14)  101.984 ms  109.314 ms  100.620 ms
 8  rostelecom-as-as12389.100gigabitethernet12-2.core1.fra1.he.net (216.66.89.226)  105.200 ms  107.087 ms  110.979 ms
 9  ae4.nvsk-ar1.sib.ip.rostelecom.ru (213.228.109.53)  239.639 ms  292.704 ms  204.999 ms
10  217.65.80.163 (217.65.80.163)  307.942 ms  308.457 ms  304.139 ms
11  host-95-170-130-186.avantel.ru (95.170.130.186)  205.826 ms  408.536 ms  205.105 ms
12  host25.50.237.84.nsu.ru (84.237.50.25)  205.715 ms  203.646 ms  205.695 ms
End time:  Wed 8 Nov 2017 16:09:27 EST
'''

def readFile(fileName):
    try :
        f = open(fileName, 'r')
        text = (f.read())
        return text
    except:
        return None

def getDate(traceRoute): #returns this string "Mon 13 Nov 2017"
    #Start time:  <<Mon 13 Nov 2017>> 20:24:33 EST
    try :
        twoDots = traceRoute.index(":")
        date = traceRoute[twoDots+2:twoDots+18]

        return date
    except:
        return None

def getTime(traceRoute): #returns this string "20:24:33"
    #Start time:  Mon 13 Nov 2017 <20:24:33> EST
    try :
        year = traceRoute.index("2017")
        time = traceRoute[year+5:year+13]
        return time
    except:
        return None

def getTimeOuts(traceRoute): #returns the number of timeouts in a single traceroute command
    try :
        return traceRoute.count('*')
    except:
        return None

def getDest(traceRoute): #returns the destination IP
    try :
        traceRoute = ''.join([traceRoute[len(traceRoute)-i-1] for i,j in enumerate(traceRoute)])
        m = traceRoute[traceRoute.find(")")+1 : traceRoute.find("(")]
        return ''.join([m[len(m)-i-1] for i,j in enumerate(m)])
    except:
        return None

def getSource(traceRoute): #returns the Source IP
    try :
        m = traceRoute[traceRoute.find("(")+1 : traceRoute.find(")")]
        return m
    except:
        return None

def getHops(traceRoute): #returns the number of hops in a single traceroute command
    ls = list()
    for w in traceRoute.split():
        try:
            ls.append(int(w))
        except:
            pass
    try:
        try :
            ls = (ls[2:-2])
            return ls[len(ls)-1]
        except:
            return None

    except:
        return None

def getTotalSucessfulPackets(traceRoute): #returns the number of successful packets in a single traceroute command
    try :
        return ((getHops(traceRoute) * 3) - getTimeOuts(traceRoute))
    except:
        return None

def getAvgTime(traceRoute): #returns the average time for the last tree packet to reach destination
    try :
        result = [i for i in range(len(traceRoute)) if traceRoute.startswith("ms", i)]
        times = [(traceRoute[result[len(result)-1]-8:result[len(result)-1]-1]),(traceRoute[result[len(result)-2]-8:result[len(result)-2]-1]),(traceRoute[result[len(result)-3]-8:result[len(result)-3]-1])]
        return reduce(lambda x, y: float(x) + float(y), times) / len(times)
    except:
        return None

def parseToArrayTraceroute(textFile):
    try :
        return textFile.split("\n\n\n\n")
    except:
        return None

from geoip import geolite2
def geoFromIP(IPname):
    match = geolite2.lookup(IPname)
    match is not None
    return match

import googlemaps
from datetime import datetime
def addressFromCoordinates(lat, lon):
    gmaps = googlemaps.Client(key='AIzaSyBWSSRoyms_3GTfrEr7rpw6t-Ki_sZP43o')
    geocode_result = gmaps.reverse_geocode((lat, lon))
    return geocode_result[0]['formatted_address']


def printHeader():
    print "Date,Time,AvgTime,TotalSuccessfulPackets,Hops,Source,Destination,ExpectedDestination,Timeouts,ReachedDestination,Country,Latitude,Longitude,Address"

# Print to stdout, can be saved to a .csv file by shell redirection
def printToCSVFormat(IPname):
    temp = parseToArrayTraceroute(readFile("../data/IP_" + IPname +".txt"))

    match = geoFromIP(IPname)
    country = match.country
    latitude, longitude = match.location
    address = addressFromCoordinates(latitude, longitude).replace(",", ";").encode('utf-8')

    for t in temp :
        if getDate(t) != None and "Start time" not in getSource(t) and getHops(t) > 2:
            print getDate(t),
            print ",",
            print getTime(t),
            print ",",
            print getAvgTime(t),
            print ",",
            print getTotalSucessfulPackets(t),
            print ",",
            print getHops(t),
            print ",",
            print getSource(t),
            print ",",
            print getDest(t),
            print ",",
            print IPname,
            print ",",
            print getTimeOuts(t),
            print ",",
            print IPname == getDest(t),
            print ",",
            print country,
            print ",",
            print latitude,
            print ",",
            print longitude,
            print ",",
            print address

array_of_ips = ["138.44.176.3", "112.137.142.4", "124.124.195.101", "155.232.32.14", "80.239.135.226", "84.237.50.25", "198.154.248.116", "143.107.249.34", "128.171.213.2", "188.44.50.103", "130.235.52.5", "194.199.156.25", "192.76.32.66", "132.247.70.37", "137.82.123.113", "128.227.9.98", "128.100.96.19", "132.216.177.160"]
printHeader()

for IPname in array_of_ips:
    printToCSVFormat(IPname)
