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
sat_sat = np.array([i.split(',')[1:] for i in data[2:-1]])
sat_sat = sat_sat.astype(float)
print(sat_sat)
z = (earth+sat_sat[:,2]) * np.sin(sat_sat[:,0])
z0_dis = (earth+sat_sat[:,2]) * np.cos(sat_sat[:,0])
x = z0_dis * np.cos(sat_sat[:,1])
y = z0_dis * np.sin(sat_sat[:,1])
sat = np.hstack((x,y,z)).reshape(3,20).T

# Satellite adjency matrix A
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



# finding ending satelites



# searching shortest route



