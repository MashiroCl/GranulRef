#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import re

input_file=sys.argv[1]
with open(input_file) as f:
    lines=f.readlines()

cc_file=os.getenv('CC_CLUSTER_INFO')
with open(cc_file) as f2:
    ccStr = f2.read()


with open(input_file,"w+") as f:
    for each in lines:
        if each.startswith("pick"):
            if ccStr.find(re.match(r'pick\s(\w+)\s(.*)',each).group(1))!=-1:
                each=each.replace("pick","squash")
                print(each+"")
        f.writelines(each)






