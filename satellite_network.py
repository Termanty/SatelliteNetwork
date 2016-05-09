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


# Getting data
url = "https://space-fast-track.herokuapp.com/generate"
with urllib.request.urlopen(url) as response:
    data = response.read().decode().split()

# Change to XYZ-coordinate system
earth = 6371
sat_loc = np.array([i.split(',')[1:] for i in data[2:-1]])
print(sat_loc)
sat_loc = sat_loc.astype(float)
z = (earth+sat_loc[:,2]) * np.sin(sat_loc[:,0])
z0_dis = (earth+sat_loc[:,2]) * np.cos(sat_loc[:,0])
x = z0_dis * np.cos(sat_loc[:,1])
y = z0_dis * np.sin(sat_loc[:,1])
sat = np.hstack((x,y,z)).reshape(3,20).T

# Satellite adjency matrix A
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



