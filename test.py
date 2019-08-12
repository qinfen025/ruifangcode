# -*- coding: utf-8 -*-
import re

filename = 'b.txt'
with open(filename,'rb') as f:
    data = f.read().decode('gbk',errors='ignore')
    pattern = re.compile(r'data-mid="(.*?)"',re.S)
    res = pattern.findall(data)

    for r in res:
        print(r)
    print(len(res))