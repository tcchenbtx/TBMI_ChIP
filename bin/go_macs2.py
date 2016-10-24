import os
import re
import json

# identify path
base_path = os.path.abspath(os.path.dirname(__file__))
base_path = os.path.join(base_path, "..")

#config_file = open(os.path.join(base_path, "configure", "configure.txt"), "r")
dataset_folder = os.path.join(base_path, "dataset")
output_folder = os.path.join(base_path, "output")

output_BAM = os.path.join(output_folder, "sorted_BAM")
output_macs2 = os.path.join(output_folder, "macs2")

#reference_folder = os.path.join(dataset_folder, "reference")

# get userinput
with open("userinput.json") as uinput:
    userinput = json.load(uinput)


# check directory
if not os.path.exists(output_macs2):
    os.makedirs(output_macs2)


# use macs2 to call peaks
with open("Makefile", "a") as mk:
    mk.write("macs2:\n")
    for i in userinput["Replicate"]:
        singlet = i.split(":")
        if userinput["Pair_end"][0] == "YES":
            mk.write("\tmacs2 callpeak -c %s -t %s -n %s -f BAMPE -B --SPMR -q 0.05 --call-summits -g %s\n"\
                     % (os.path.join(output_BAM, singlet[0]+".bam"), os.path.join(output_BAM, singlet[1]+".bam"),\
                        os.path.join(output_macs2, singlet[1] + "_macs2"), userinput["Reference"][0][:2]))
        else:
            mk.write("\tmacs2 callpeak -c %s -t %s -n %s -f BAM -B --SPMR -q 0.05 --call-summits -g %s\n"\
                     % (os.path.join(output_BAM, singlet[0]+".bam"), os.path.join(output_BAM, singlet[1]+".bam"),\
                        os.path.join(output_macs2, singlet[1] + "_macs2"), userinput["Reference"][0][:2]))
