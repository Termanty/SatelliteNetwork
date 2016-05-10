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


earth = 6371


# Getting data
url = "https://space-fast-track.herokuapp.com/generate"
with urllib.request.urlopen(url) as response:
    data = response.read().decode().split()

print(data[1])

# Extracting location data
satellites = np.array([i.split(',')[1:] for i in data[2:-1]])
start = np.append(data[-1].split(',')[1:3], ['0'])
end = np.append(data[-1].split(',')[3:], ['0'])
location = np.vstack((satellites, start, end))
location = location.astype(float)

#print(location)


# Change alltitude to distance from the earth center
location[:,2] = location[:,2] + earth

# Degrees to radians
location[:,:2] = np.radians(location[:,:2])

# Change to XYZ-coordinate system
zplane = location[:,2] * np.cos(location[:,0])
x = zplane * np.cos(location[:,1])
y = zplane * np.sin(location[:,1])
z = location[:,2] * np.sin(location[:,0])
xyz_location = np.vstack((x,y,z)).T

#print(xyz_location)


# Projection of a point to 3D-line
def p2line(point, linep_a, linep_b):
    ab = linep_b - linep_a
    ap = point - linep_a
    proj = linep_a + np.dot(ap,ab)/np.dot(ab,ab)*ab
    dis = norm(proj)
    if isinstance(point, np.ndarray):
        if norm(linep_b - point) > earth:
            return False
    return dis > earth 


# Satellite adjency matrix A
sat = xyz_location[:-2]
A = np.zeros((20,20), dtype='int')
for i in range(20):
    for j in range(20):
        if not(i==j) and p2line(0,sat[i],sat[j]):
            A[i][j] = 1

print(A)


# Satellites visible to starting and ending locations
start = xyz_location[-2]
end = xyz_location[-1]
visible_start = [i for i in range(20) if p2line(sat[i],0,start)]
visible_end = [i for i in range(20) if p2line(sat[i],0,end)]


# searching shortest route
print(visible_start)
print(visible_end)

def connections(satellite):
    return [i for i in range(20) if A[satellite,i]]

def search(start, end):
    queue = [(start, [start])]
    while queue:
        (satellite, path) = queue.pop(0)
        for next in set(connections(satellite)) - set(path):
            if next in end:
                return path + [next]
            else:
                queue.append((next, path + [next]))

if not visible_start or not visible_end:
    print('no path')
elif set(visible_start) == set(visible_end):
    print('common satellite')
    print(set(visible_start).intersection(visible_end))
else:
    print('path search')
    print(list(search(visible_start[0], visible_end)))


