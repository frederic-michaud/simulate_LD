#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 17:03:27 2018

@author: Frederic
"""

from subprocess import Popen
import os
import numpy as np
import warnings
import pickle

def run_simulation_two_pops(n1: int, n2: int, theta: float, D: float,output_folder):

    current_folder = os.path.dirname(os.path.realpath(__file__))
    script_folder = current_folder

    scrm_result = os.path.join(output_folder,'scrm.txt')
    location_run_scrm = os.path.join(script_folder, "run_scrm.py")
    length_bottleneck = 0.0125
    strenght_bottleneck = 0.01
    scrm_command = f'{n1 + n2} 1 -t {theta} -r 40000 250000000 -I 2 {n1} {n2} -ej {D} 2 1 -en 0 2 1 -en {D - length_bottleneck} 2 {strenght_bottleneck} --print-model -L'
    run_scrm = Popen(['python', location_run_scrm, scrm_command, scrm_result])
    run_scrm.communicate()


    pattern_snp_file = "snip"
    snip_file = os.path.join(output_folder,f'{pattern_snp_file}.tped')
    location_transcode = os.path.join(script_folder, "transcode.py")
    transcode_commande = f'python {location_transcode} {scrm_result} {snip_file} {n1+n2} 100000'
    print(transcode_commande)
    transcode = Popen(transcode_commande.split())
    transcode.communicate()

    location_create_fake_tfam = os.path.join(script_folder, "create_tfam.py")
    label_file = os.path.join(output_folder,'snip.tfam')
    fake_tfam_command = " ".join(['python', location_create_fake_tfam, '-of', label_file, '-ps', str(n1), str(n2)])
    create_label = Popen(fake_tfam_command.split())
    create_label.communicate()


    location_create_fake_label = os.path.join(script_folder, "create_fake_labels.py")
    label_file = os.path.join(output_folder,'fake_labs.txt')
    fake_label_command = " ".join(['python', location_create_fake_label, '-of', label_file, '-ps', str(n1), str(n2)])
    print(fake_label_command)
    create_label = Popen(fake_label_command.split())
    create_label.communicate()


    plink_command = f"plink --indep-pairwise 5 5 0.01 --tfile {pattern_snp_file}"
    print(plink_command)
    get_linkage = Popen(plink_command.split(),cwd = output_folder)
    get_linkage.communicate()

    location_remove_linked_site = os.path.join(script_folder, "remove_linked_site.py")
    snp_file = os.path.join(output_folder, f'{pattern_snp_file}.tped')
    snp_in_file = os.path.join(output_folder, f'plink.prune.in')
    snp_out_file = os.path.join(output_folder, f'{pattern_snp_file}.prune.tped')
    remove_linked_site_command = " ".join(['python',location_remove_linked_site, snp_file,snp_in_file,snp_out_file])
    remove_linked_site = Popen(remove_linked_site_command.split())
    remove_linked_site.communicate()

    med_file = os.path.join(output_folder, f'{pattern_snp_file}.med')
    os.system(f"cut -d ' ' -f 5- {snp_out_file} > {med_file}")


    location_run_medeas = os.path.join(script_folder, "run_medeas.py")


    command = " ".join(['python',location_run_medeas, med_file,label_file,output_folder,str(int(theta/100))])
    print(command)
    medeas = Popen(command.split())
    medeas.communicate()

    output_folder_bis = output_folder + "_without_linkage"
    med_file_bis = os.path.join(output_folder_bis, f'{pattern_snp_file}.med')
    print(f"cut -d ' ' -f 5- {snp_file} > {med_file_bis}")
    os.system(f"cut -d ' ' -f 5- {current_folder}/{snp_file} > {current_folder}/{med_file_bis}")


    location_run_medeas = os.path.join(script_folder, "run_medeas.py")


    command = " ".join(['python',location_run_medeas, med_file_bis,label_file,output_folder_bis,str(int(theta/100))])
    print(command)
    medeas = Popen(command.split())
    medeas.communicate()

n1 = 20
n2 = 20
theta = 50000
D = 0.05
thetas = [100,1000,10000,100000]
nb_replicate = 100
for theta in thetas:
    f =  open (f"theta_{theta}.txt", "w")
    g = open(f"theta_{theta}_without_linkage_removale.txt", "w")
    for replicate_index in range(nb_replicate):
        output_folder = f"result/theta_{theta}_rep_{replicate_index}"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        if not os.path.exists(output_folder+"_without_linkage"):
            os.makedirs(output_folder+"_without_linkage")
        run_simulation_two_pops(n1, n2, theta, D, output_folder)
        all_dist = np.loadtxt(f"{output_folder}/all_extrapolated_distances.txt")
        f.write(str(all_dist[0])+"\n")
        all_dist = np.loadtxt(f"{output_folder}_without_linkage/all_extrapolated_distances.txt")
        g.write(str(all_dist[0])+"\n")
    f.close()
    g.close()
