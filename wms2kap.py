#!/usr/bin/python

import pyproj
import urllib
import tempfile
import subprocess

p1 = pyproj.Proj(init="epsg:3067")
p2 = pyproj.Proj(init="epsg:4326")


x1 = 346670
y1 = 6655590
x2 = 356670
y2 = 6665590

(wgsx1, wgsy1) = pyproj.transform(p1,p2,x1,y1)
(wgsx2, wgsy2) = pyproj.transform(p1,p2,x2,y2)

# calculate image scale
imagesize = 4096
imagesize = 1024
dpi = 72
dpm = dpi / 0.0254
imagemeters = imagesize / dpm
mapmetersx = (x2 - x1)
mapmetersy = (y2 - y1)
mapmeters = (mapmetersx + mapmetersy) / 2.0
scale = int(1.0 / (imagemeters / mapmeters))

averagelatitude = (wgsy1 + wgsy2) / 2.0

kaptmpl = """!kantvik.kap
VER/2.0
BSB/NA=kantvik
    NU=1,RA=%d,%d,DU=%d
KNP/SC=%d,GD=WGS84,PR=MERCATOR
    PP=%.2f,PI=UNKNOWN,SP=UNKNOWN,SK=0.0,TA=90.0
    UN=METERS,SD=MLSW,DX=000,DY=000
CED/SE=1,RE=1,ED=01/01/2016
OST/1
REF/1,%d,%d,%.8f,%.8f
REF/2,%d,%d,%.8f,%.8f
REF/3,%d,%d,%.8f,%.8f
REF/4,%d,%d,%.8f,%.8f
PLY/1,%.8f,%.8f
PLY/2,%.8f,%.8f
PLY/3,%.8f,%.8f
PLY/4,%.8f,%.8f
DTM/0.00,0.00
CPH/0.0
"""

wmstmpl = "http://kartta.liikennevirasto.fi/meriliikenne/dgds/wms_ip/merikartta?request=GetMap&BBOX=%d,%d,%d,%d&width=%d&height=%d&layers=cells&format=image/png&srs=EPSG:3067"

print(kaptmpl % (imagesize, imagesize, dpi, scale, averagelatitude,
  0,imagesize-1, wgsy1, wgsx1,
  0,0, wgsy2, wgsx1,
  imagesize-1,0, wgsy2, wgsx2,
  imagesize-1,imagesize-1, wgsy1, wgsx2,
  wgsy1, wgsx1,
  wgsy2, wgsx1,
  wgsy2, wgsx2,
  wgsy1, wgsx2))

kapfile = tempfile.NamedTemporaryFile(suffix=".kap")
kapfile.write(kaptmpl % (imagesize, imagesize, dpi, scale, averagelatitude,
  0,imagesize-1, wgsy1, wgsx1,
  0,0, wgsy2, wgsx1,
  imagesize-1,0, wgsy2, wgsx2,
  imagesize-1,imagesize-1, wgsy1, wgsx2,
  wgsy1, wgsx1,
  wgsy2, wgsx1,
  wgsy2, wgsx2,
  wgsy1, wgsx2))
kapfile.flush()
print(kapfile.name)

print(wmstmpl % (x1,y1,x2,y2,imagesize,imagesize))

(imagefilename, headers) = urllib.urlretrieve(wmstmpl % (x1,y1,x2,y2,imagesize,imagesize))
print(imagefilename)


subprocess.call(["/home/jtorma/src/imgkap/imgkap", imagefilename, kapfile.name, "/tmp/out.kap"])
