#!/usr/bin/python

import pyproj

p1 = pyproj.Proj(init="epsg:3067")
p2 = pyproj.Proj(init="epsg:4326")


x1 = 346670
y1 = 6655590
x2 = 356670
y2 = 6665590

print(pyproj.transform(p1,p2,x1,y1))
print(pyproj.transform(p1,p2,x2,y2))
