import json
import urllib.request
import math

def elevation_path(lat1, lng1, lat2, lng2, smpls): 
    apikey = "AIzaSyDjTjrZdOAQ2hZ4fTo-jyqO5wXs1FqptBY" 
    url = "https://maps.googleapis.com/maps/api/elevation/json" 
    request = urllib.request.urlopen(url+"?path="+str(lat1)+","+str(lng1)+"|"+str(lat1)+","+str(lng2)+"&samples="+str(smpls)+"&key="+apikey) 
    results = json.load(request).get('results') 
    elevation_path = [] 
    for i in range(0, smpls): 
        if 0 < len(results): 
            elevation_path.append(results[i].get('elevation'))
    return elevation_path 

def elevation_matrix(lat1, lng1, lat2, lng2, smpls): 
    int_dist = abs(lng2 - lng1) / smpls
    smpls_2 = math.ceil(abs(lat2 - lat1) / int_dist)
    print(smpls_2)
    print(smpls)
    elevation_matrix = [] 
    for i in range(smpls_2): 
        elevation_matrix.append(elevation_path(lat1+i*int_dist, lng1, lat2+i*int_dist, lng2, smpls)) 
    return elevation_matrix

print(elevation_matrix(44.3063580, -78.3397630, 44.3142140, -78.3457930, 20))
