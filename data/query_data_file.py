#!/usr/bin/env python

##
#  Retrieve the latlons form the original data txt file and
#  and retrieve the material properties from binary vp.dat file 
#

#
#-115.88 32.61 0
#-116.5800 33.3200 0
#-116.4 33.33 0
#-115.8800    32.6100      0.000    124.464    542.536       none      0.000      0.000      0.000
#       none      0.000      0.000      0.000       none      0.000      0.000      0.000
# -116.5800    33.3200      0.000   1727.111    710.100      cvlsu   4522.500   2687.262   2465.316
#       none      0.000      0.000      0.000      crust   4522.500   2687.262   2465.316
#-116.4000    33.3300      0.000    264.152    363.585      cvlsu   4524.600   2688.789   2465.608
#       none      0.000      0.000      0.000      crust   4524.600   2688.789   2465.608

import getopt
import sys
import subprocess
import struct
import numpy as np

dimension_x = 101 
dimension_y = 91
dimension_z = 19

lon_origin = -116.7
lat_origin = 33.3

lon_upper = -115.7
lat_upper = 34.2

delta_lon = (lon_upper - lon_origin )/(dimension_x-1)
delta_lat = (lat_upper - lat_origin)/(dimension_y-1)

def usage():
    print("\n./query_data_files.py\n\n")
    sys.exit(0)

def main():

    count =0

    f_lonlat = open("./CV_3D_Model.txt")

    f_vp = open("./cvlsu/vp.dat")

    vp_arr = np.fromfile(f_vp, dtype=np.float32)

    f_vp.close()

    lon_start = lon_origin
    lat_start = lat_origin
    depth_start = 0.0;

    count =0
    for line in f_lonlat:
        arr = line.split()
        lon_v = float(arr[0])
        lat_v = float(arr[1])
        depth_v = float(arr[2])/500
        fvp = arr[3]

        y_pos = int(round((lat_v - lat_origin) / delta_lat))
        x_pos = int(round((lon_v - lon_origin) / delta_lon))
        z_pos = int(depth_v)

        offset=z_pos * (dimension_y * dimension_x) + (y_pos * dimension_x) + x_pos
        vp=vp_arr[offset];

        if((fvp != "NaN") & (count < 10)) :
          count = count + 1
          print ">>offset ",offset
          print "xyz:", x_pos," ",y_pos," ",z_pos," >> ", lon_v, " ",lat_v, " ", float(depth_v) , "-->vp", vp, "->fvp", fvp

        if((float(vp) != -1) & ( (float(vp) > 8000) | (float(vp)<1500))) :
          print lon_v, " ",lat_v, " ", float(depth_v) , "-->vp", vp

    f_lonlat.close()
    print("\nDone!")

if __name__ == "__main__":
    main()


