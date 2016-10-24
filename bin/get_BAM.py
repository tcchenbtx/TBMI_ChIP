import os
import re
from sys import platform
from tools import pair_output
from tools import pattern_in_list
import json

# identify path
base_path = os.path.abspath(os.path.dirname(__file__))
base_path = os.path.join(base_path, "..")

config_file = open(os.path.join(base_path, "configure", "configure.txt"), "r")
dataset_folder = os.path.join(base_path, "dataset")
output_folder = os.path.join(base_path, "output")
output_trim_galore = os.path.join(output_folder, "trim_galore_output")
output_bowtie2 = os.path.join(output_folder, "bowtie2")
reference_folder = os.path.join(dataset_folder, "reference")
output_BAM = os.path.join(output_folder, "sorted_BAM")

# get userinput
with open("userinput.json") as uinput:
    userinput = json.load(uinput)

# # genome_symbo
# g_symbo = ""
# if userinput["Reference"][0][:2] == "mm":
#     for i in range(1, 20):
#         g_symbo += ("chr%d" % i + " ")
#     g_symbo += "chrX chrY chrM"
#
# elif userinput["Reference"][0][:2] == "hg":
#     for i in range(1, 22):
#         g_symbo += ("chr%d" % i + " ")
#     g_symbo += "chrX chrY chrM"

# read bowtie2 files
bowtie2F = []
for (dirpath, dirnames, filenames) in os.walk(output_bowtie2):
    bowtie2F.extend(filenames)
    break

# check directory
if not os.path.exists(output_BAM):
    os.makedirs(output_BAM)

# construct Makefiles
with open("Makefile", "a") as mk:
    mk.write("get_BAM:\n")
    for i in bowtie2F:
        target_file = os.path.join(output_bowtie2, i)
        output_file = os.path.join(output_BAM, i[:-4] + ".bam")
        mk.write("\tsamtools view -bS %s > %s\n" % (target_file, output_file))
        mk.write("\tsamtools sort -T temp -o %s %s\n" % (output_file[:-4] + ".sorted.bam", output_file))

    mk.write("merge:\n")
    if userinput["Multi_lane"][0] == 'YES':
        singlet = []
        for i in userinput["Replicate"]:
            singlet += i.split(":")

        print singlet

        for i in singlet:
            sample_for_multi = pattern_in_list(i, bowtie2F)
            command = "\tsamtools merge %s " % (os.path.join(output_BAM, i + ".bam"))
            for j in sample_for_multi:
                target_file = os.path.join(output_BAM, j[:-4] + ".sorted.bam")
                command = command + target_file + " "
            mk.write("%s\n" % command[:-1])

