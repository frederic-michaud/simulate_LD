#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 17:03:27 2017

@author: ivan
"""


import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-of","--output_file", help="Name and localisation of the label file to create",required=True)
parser.add_argument('-ps','--population_sizes', nargs='+', help='The size of all population', required=True, type=int)
args = parser.parse_args()


def create_fake_label(filename_labels: str, population_sizes)->None:
    with open(filename_labels, 'w') as f:
        for population_index, population_size in enumerate(population_sizes):
            for _ in range(round(population_size/2)): ##plink expect diploid individual
                f.write(f'1 1 0 0 1 1\n')
create_fake_label(args.output_file,args.population_sizes)