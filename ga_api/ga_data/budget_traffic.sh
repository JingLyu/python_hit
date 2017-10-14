cd /Users/jilv/scripts
python combine_file_for_budget_traffic.py
cd ga_data
awk  'BEGIN{FS=","}{OFS=","}{$2=substr($2,1,4)"-"substr($2,5,2)"-01"; print}' vst_uv_platform_device_categ_src_pagetype_mth.all > budget_traffic.csv 


