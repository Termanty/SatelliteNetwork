#########################################
#
# Reaktor Orbital Challenge
#
# @Tero Mäntylä
# termanty@cs.helsinki.fi
#

import numpy as np
import math
import urllib.request


earth = 6371


# Getting data
url = "https://space-fast-track.herokuapp.com/generate"
with urllib.request.urlopen(url) as response:
    data = response.read().decode().split()


# Extracting location data
location = np.array([i.split(',')[1:] for i in data[2:-1]])
start = np.append(data[-1].split(',')[1:3], ['0'])
end = np.append(data[-1].split(',')[3:], ['0'])
location = np.vstack((location, start, end))
location = location.astype(float)

print(location)

# Change alltitude to distance from the earth center
location[:,2] = location[:,2] + earth

# Change to XYZ-coordinate system
zplane = location[:,2] * np.cos(location[:,0])
x = zplane * np.cos(location[:,1])
y = zplane * np.sin(location[:,1])
z = location[:,2] * np.sin(location[:,0])
xyz_location = np.vstack((x,y,z)).T

# Satellite adjency matrix A
sat = xyz_location[:-2]
A = np.zeros((20,20), dtype='int')
for i in range(20):
    for j in range(20):
        if i != j:
            ab = sat[j] - sat[i]
            a0 = 0 - sat[i]
            point = sat[i] + np.dot(a0,ab)/np.dot(ab,ab) * ab
            if np.linalg.norm(point) > earth:
                A[i][j] = 1

print(A)

# finding starting satelites
start = np.array(data[-1].split(',')[1:3]).astype(float)



# finding ending satelites
end = np.array(data[-1].split(',')[3:]).astype(float)



# searching shortest route



