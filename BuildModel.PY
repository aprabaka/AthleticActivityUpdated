#! python3.6





from datetime import datetime

import xml.etree.ElementTree as ET
tree = ET.parse('Afternoon_Run.tcx')
root = tree.getroot()

csvData = [['x', 'y', 'z', 'speed']]

x = 0
lastD = 0
lastT = None
for n in root[0][0][1][7]: #x, y, x

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
    x += 1
    if x == 3:
        break
import csv

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
    if n[1] > yMin:
        yMax = n[1]
    if n[1] < yMax:
        yMin = n[1]

print("Xcord", xMin, xMax)
print("Ycord", yMin, yMax)
