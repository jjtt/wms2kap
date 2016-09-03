#!/usr/bin/python

import pyproj

p1 = pyproj.Proj(init="epsg:3067")
p2 = pyproj.Proj(init="epsg:4326")


x1 = 346670
y1 = 6655590
x2 = 356670
y2 = 6665590

(wmsx1, wmsy1) = pyproj.transform(p1,p2,x1,y1)
(wmsx2, wmsy2) = pyproj.transform(p1,p2,x2,y2)

# calculate image scale
imagesize = 4096
dpi = 72
dpm = dpi / 0.0254
imagemeters = imagesize / dpm
mapmetersx = (x2 - x1)
mapmetersy = (y2 - y1)
mapmeters = (mapmetersx + mapmetersy) / 2.0
scale = int(1.0 / (imagemeters / mapmeters))


kaptmpl = """!kantvik.kap
VER/2.0
BSB/NA=kantvik
    NU=1,RA=%d,%d,DU=%d
KNP/SC=%d,GD=WGS84,PR=MERCATOR
    PP=60,PI=UNKNOWN,SP=UNKNOWN,SK=0.0,TA=90.0
    UN=METERS,SD=MLSW,DX=000,DY=000
CED/SE=1,RE=1,ED=01/01/2016
OST/1
REF/1,0,4095,60.00889556,24.24978462
REF/2,0,0,60.10220688,24.24978462
REF/3,4095,0,60.10220688,24.42194184
REF/4,4095,4095,60.00889556,24.42194184
PLY/1,60.00889556,24.24978462
PLY/2,60.10220688,24.24978462
PLY/3,60.10220688,24.42194184
PLY/4,60.00889556,24.42194184
DTM/0.00,0.00
CPH/0.0
"""

wmstmpl = "http://kartta.liikennevirasto.fi/meriliikenne/dgds/wms_ip/merikartta?request=GetMap&BBOX=346670,6655590,356670,6665590&width=4096&height=4096&layers=cells&format=image/png&srs=EPSG:3067"

print(kaptmpl % (imagesize, imagesize, dpi, scale))
