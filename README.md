
# ECSE 414

## Data Collection Script

Instructions on how to run the script and save the result in a .csv file.

### Instructions

To save the output of the script to a .csv file, use a pipe command in bash as follows:

```
$ python parse_ips.py > test.csv
```
## Resources

### geoip

We used geoip to retrieve the continent, country and coordinates of IP addresses

```
$ pip install geoip
$ pip install geolite2
```

### googlemaps

We used Google Maps' GeoCoding API to retrieve the physical addresses of IP addresses

```
$ pip install -U googlemaps
```
