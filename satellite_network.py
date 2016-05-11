#########################################
#
# Reaktor Orbital Challenge
#
# Tero Mäntylä
# termanty@cs.helsinki.fi
#

import numpy as np
from numpy.linalg import norm
import urllib.request

R = 6371

# Getting data
url = "https://space-fast-track.herokuapp.com/generate"
with urllib.request.urlopen(url) as response:
    data = response.read().decode().split()
print('SEED: ' + data[1])

# Extracting locations data
satellites = np.array([i.split(',')[1:] for i in data[2:-1]])
start = np.append(data[-1].split(',')[1:3], ['0'])
end = np.append(data[-1].split(',')[3:], ['0'])
locations = np.vstack((satellites, start, end))
locations = locations.astype(float)

# Change alltitude to distance from the R center
locations[:,2] = locations[:,2] + R

# Degrees to radians
locations[:,:2] = np.radians(locations[:,:2])

# Change to XYZ-coordinate system
zplane = locations[:,2] * np.cos(locations[:,0])
x = zplane * np.cos(locations[:,1])
y = zplane * np.sin(locations[:,1])
z = locations[:,2] * np.sin(locations[:,0])
xyz_locations = np.vstack((x,y,z)).T

# Projection of a point to the 3D-line
def projectpoint2line(p, a, b):
    ab = b - a
    ap = p - a
    return a + np.dot(ap,ab)/np.dot(ab,ab)*ab

# Checks if two satellites are able to communicate
def hassat2satconnection(satA, satB):
    closest2Rcenter = projectpoint2line(0, satA, satB)
    return norm(closest2Rcenter) > R

# Checks if ground locations can connect to satellite
def hasconnection2sat(ground, sat):
    proj = projectpoint2line(sat, 0, ground) 
    return norm(proj) > R and norm(sat - ground) < R

# Satellite adjency matrix A
sats = xyz_locations[:-2]
A = np.zeros((20,20), dtype='int')
for i in range(20):
    for j in range(20):
        if not(i==j) and hassat2satconnection(sats[i],sats[j]):
            A[i][j] = 1

# Satellites visible to starting and ending locations
start = xyz_locations[-2]
end = xyz_locations[-1]
visible_start = [i for i in range(20) if hasconnection2sat(start, sats[i])]
visible_end = [i for i in range(20) if hasconnection2sat(end, sats[i])]

# Lists all satellites which are able to communicate with this satellite
def connections(sat):
    return [i for i in range(20) if A[sat,i]]

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

