import re
import os
import json
from tools import identify_treatment_groups

# identify path
base_path = os.path.abspath(os.path.dirname(__file__))
base_path = os.path.join(base_path, "..")

dataset_folder = os.path.join(base_path, "dataset")
output_folder = os.path.join(base_path, "output")

output_BAM = os.path.join(output_folder, "sorted_BAM")
output_macs2 = os.path.join(output_folder, "macs2")
output_clean_narrowPeak = os.path.join(output_folder, "macs2", "clean_narrowPeak")
output_IDR = os.path.join(output_folder, "IDR_output")

idr_path = os.path.join(base_path, "software", "idrCode")

# get userinput
with open("userinput.json") as uinput:
    userinput = json.load(uinput)

# get clean narrowPeak files

clean_narrowPeak_files = []
for (dirpath, dirnames, filenames) in os.walk(output_clean_narrowPeak):
    clean_narrowPeak_files.extend(filenames)
    break

# check directory
if not os.path.exists(output_IDR):
    os.makedirs(output_IDR)

# use IDR to get overlapped peaks
with open("Makefile", "a") as mk:
    mk.write("IDR:\n")
    if userinput["Reference"][0] in ["mm9", "mm10", "hg18", "hg19"]:
        mk.write("\tcat %s_genome.txt > ../software/idrCode/genome_table\n" % userinput["Reference"][0])
    else:
        print ("Only the following is supported: mm9, mm10, hg18 and hg19\n")
        print ("To continue, please fix the genome_table.txt under software/idrCode\n")

    exp_pairs = identify_treatment_groups(clean_narrowPeak_files, userinput["Treatment"])
    print exp_pairs

    for i in exp_pairs:
        mk.write("\tcd %s && Rscript batch-consistency-analysis.r %s %s -1 %s 0 F p.value\n" % (idr_path, os.path.join(output_clean_narrowPeak, i[0]), os.path.join(output_clean_narrowPeak, i[1]), os.path.join(output_IDR, "%s_%s_IDR" % (i[0], i[1]))))




