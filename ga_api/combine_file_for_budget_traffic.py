import glob
import os

os.chdir("/Users/jilv/scripts/ga_data")
read_files = glob.glob("*_vst_uv_platform_device_categ_src_pagetype_mth*csv")
filename='vst_uv_platform_device_categ_src_pagetype_mth.all'
try:
    os.remove(filename)
except OSError:
    pass



with open(filename, "wb") as outfile:
    for f in read_files:
        with open(f, "rb") as infile:
            print f
            outfile.write(infile.read())
