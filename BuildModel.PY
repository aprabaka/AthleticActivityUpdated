#! python3.6

import csv
from datetime import datetime

import xml.etree.ElementTree as ET
tree = ET.parse('Afternoon_Run.tcx')
root = tree.getroot()

csvData = [['x', 'y', 'z', 'speed']]

x = 0
lastD = 0
lastT = None
for n in root[0][0][1][7]: #x, y, z, speed

    if lastT == None:
        csvData.append([n[1][0].text, n[1][1].text, n[2].text, '0'])
        lastT = datetime.strptime(n[0].text, '%Y-%m-%dT%H:%M:%SZ')
    else:
        DDif = float(n[3].text) - lastD
        lastD = float(n[3].text)

        date_time_obj = datetime.strptime(n[0].text, '%Y-%m-%dT%H:%M:%SZ')
        TDif = date_time_obj - lastT
        TDif = TDif.total_seconds()
        lastT = date_time_obj
        
        speed = round(DDif / TDif, 2)
        csvData.append([n[1][0].text, n[1][1].text, n[2].text, str(speed)])

with open('route.csv', 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(csvData)
csvFile.close()

xMax = csvData[1][0]
xMin = csvData[1][0]
yMax = csvData[1][1]
yMin = csvData[1][1]
for n in csvData[1:]:
    if n[0] > xMax:
        xMax = n[0]
    if n[0] < xMin:
        xMin = n[0]
    if n[1] > yMax:
        yMax = n[1]
    if n[1] < yMin:
        yMin = n[1]

xMin = float(xMin)
yMin = float(yMin)
xMax = float(xMax)
yMax = float(yMax)

if xMax - xMin > (yMax - yMin) * 4:
    add = ((xMax - xMin)-(yMax - yMin) * 4)/2
    yMax += add
    yMin -= add
elif yMax - yMin > (xMax - xMin) * 4:
    add = ((yMax - yMin)-(xMax - xMin) * 4)/2
    xMax += add
    xMin -= add

###################################################33
import json
import urllib.request
import math

def elevation(lat1, lng1, lat2, lng2, smpls):
    global elevation_matrix
    apikey = "AIzaSyDjTjrZdOAQ2hZ4fTo-jyqO5wXs1FqptBY" 
    url = "https://maps.googleapis.com/maps/api/elevation/json" 
    request = urllib.request.urlopen(url+"?path="+str(lat1)+","+str(lng1)+"|"+str(lat1)+","+str(lng2)+"&samples="+str(smpls)+"&key="+apikey) 
    results = json.load(request).get('results') 
    for i in range(0, smpls): 
        if 0 < len(results): 
            elevation_matrix.append([lat1, lng1+i*((lng2-lng1)/smpls), results[i].get('elevation')])

def elevation_path(lat1, lng1, lat2, lng2, smpls): 
    global elevation_matrix
    int_dist = abs(lng2 - lng1) / smpls
    smpls_2 = math.ceil(abs(lat2 - lat1) / int_dist)
    elevation_matrix = [] 
    for i in range(smpls_2): 
        elevation(lat1+i*int_dist, lng1, lat2+i*int_dist, lng2, smpls)


elevation_path(xMin, yMin, xMax, yMax, 20)
###################################################33

with open('terrain.csv', 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(elevation_matrix)
csvFile.close()


