#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 22:14:17 2019

@author: carlosponce
"""

output_filename = 'test output.csv'
input_filename = 'Test input.txt'

f_output = open(output_filename,'w+')
f_input = open(input_filename, 'r')

lines = []

for line in f_input:
    lines.append(line)

for line in lines:
    print(line)
    
f_output.close()
f_input.close()


    
    

    






















