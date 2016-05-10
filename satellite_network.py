#########################################
#
# Reaktor Orbital Challenge
#
# @Tero Mäntylä
# termanty@cs.helsinki.fi
#

import numpy as np
from numpy.linalg import norm
import math
import urllib.request

R = 6371

# Getting data
url = "https://space-fast-track.herokuapp.com/generate"
with urllib.request.urlopen(url) as response:
    data = response.read().decode().split()
print('SEED: ' + str(data[1]))

# Extracting location data
satellites = np.array([i.split(',')[1:] for i in data[2:-1]])
start = np.append(data[-1].split(',')[1:3], ['0'])
end = np.append(data[-1].split(',')[3:], ['0'])
location = np.vstack((satellites, start, end))
location = location.astype(float)

# Change alltitude to distance from the R center
location[:,2] = location[:,2] + R

# Degrees to radians
location[:,:2] = np.radians(location[:,:2])

# Change to XYZ-coordinate system
zplane = location[:,2] * np.cos(location[:,0])
x = zplane * np.cos(location[:,1])
y = zplane * np.sin(location[:,1])
z = location[:,2] * np.sin(location[:,0])
xyz_location = np.vstack((x,y,z)).T

# Projection of a point to 3D-line
def projectpoint2line(point, linep_a, linep_b):
    ab = linep_b - linep_a
    ap = point - linep_a
    return linep_a + np.dot(ap,ab)/np.dot(ab,ab)*ab

# Checks if two satellites are able to communicate
def has_sat2sat_connection(satA, satB):
    closest2Rcenter = projectpoint2line(0, satA, satB)
    return norm(closest2Rcenter) > R

# Checks if ground location can connect to satellite
def hasconnection2sat(ground, sat):
    satttt = projectpoint2line(sat, 0, ground) 
    distance = norm(satttt)
    return distance > R and norm(sat - ground) < R

# Satellite adjency matrix A
sat = xyz_location[:-2]
A = np.zeros((20,20), dtype='int')
for i in range(20):
    for j in range(20):
        if not(i==j) and has_sat2sat_connection(sat[i],sat[j]):
            A[i][j] = 1

# Satellites visible to starting and ending locations
start = xyz_location[-2]
end = xyz_location[-1]
visible_start = [i for i in range(20) if hasconnection2sat(start, sat[i])]
visible_end = [i for i in range(20) if hasconnection2sat(end, sat[i])]

# Lists all satellites which are able to communicate with this satellite
def connections(satellite):
    return [i for i in range(20) if A[satellite,i]]

# Breadth first search for path finding
def search(start, end):
    queue = [(start, [start])]
    while queue:
        (satellite, path) = queue.pop(0)
        for next in set(connections(satellite)) - set(path):
            if next in end:
                return path + [next]
            else:
                queue.append((next, path + [next]))

# Finding solution
if not visible_start or not visible_end:
    print('warning! no path excist!')
else:
    paths = [search(i, visible_end) for i in visible_start]
    print('shortest path:')
    print(min(paths, key=len))

