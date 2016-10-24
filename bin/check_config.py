import os
import re
from sys import platform
from tools import pair_output
from tools import pattern_in_list
import json
import pickle

# identify path
base_path = os.path.abspath(os.path.dirname(__file__))
base_path = os.path.join(base_path, "..")

config_file = open(os.path.join(base_path, "configure", "configure.txt"), "r")
dataset_folder = os.path.join(base_path, "dataset")
output_folder = os.path.join(base_path, "output")
output_trim_galore = os.path.join(output_folder, "trim_galore_output")
output_bowtie2 = os.path.join(output_folder, "bowtie2")
reference_folder = os.path.join(dataset_folder, "reference")

# set separator
separator = "#"*80

# parse configure file
config_input = [line[:-1] for line in config_file]
config_input = [re.sub(r'#.*', "", i) for i in config_input]
config_input = [i for i in config_input if i != ""]

indexnum = {}
indexnum["Treatment"] = config_input.index("@Treatment:")
indexnum["Multi_lane"] = config_input.index("@Multi_Lane:")
indexnum["Replicate"] = config_input.index("@Replicate:")
indexnum["Pair_end"] = config_input.index("@Pair_end:")
indexnum["Reference"] = config_input.index("@Reference:")

userinput = {}
userinput["Treatment"] = config_input[indexnum["Treatment"]+1: indexnum["Multi_lane"]]
userinput["Multi_lane"] = config_input[indexnum["Multi_lane"]+1: indexnum["Replicate"]]
userinput["Replicate"] = config_input[indexnum["Replicate"]+1: indexnum["Pair_end"]]
userinput["Pair_end"] = config_input[indexnum["Pair_end"]+1:indexnum["Reference"]]
userinput["Reference"] = config_input[indexnum["Reference"]+1:]

# output userinput
with open("userinput.json", "w") as uoutput:
    json.dump(userinput, uoutput, indent=4, sort_keys=True)

# get file_list
file_list = []
for (dirpath, dirnames, filenames) in os.walk(dataset_folder):
    file_list.extend(filenames)
    break
with open("file_list.txt", "w") as fileL:
    for i in file_list:
        fileL.write("%s\n" %i)

# files to go through
file_patten = ""
for i in userinput["Treatment"]:
    file_patten = file_patten + ".*" + i + ".*|"
file_patten = file_patten[:-1]

process_files = [i for i in file_list if re.match(file_patten, i)]

with open("process_files.txt", "w") as proF:
    for i in process_files:
        proF.write("%s\n" %i)


# paired_end files
pair_list = {}
pair_file_path = {}
if userinput["Pair_end"][0] == "YES":
    pair_n = 1
    for i in range(0, len(process_files), 2):
        pair_list["pair_%s" % pair_n] = "%s %s" % (process_files[i], process_files[i+1])
        pair_file_path["pair_%s" % pair_n] = "%s %s" % (os.path.join(dataset_folder, process_files[i]), os.path.join(dataset_folder, process_files[i+1]))
        pair_n += 1

with open("pair_list.json", "w") as poutput:
    json.dump(pair_list, poutput, indent=4, sort_keys=True)

with open("pair_file_path.json", "w") as ploutput:
    json.dump(pair_file_path, ploutput, indent=4, sort_keys=True)

# display analysis plan:
# TrimGalore

print (separator)
print ("Your input:\n")
inputlist = ["Treatment", "Multi_lane", "Replicate", "Pair_end"]
for i in inputlist:
    print ("%10s: %s" % (i, userinput[i]))

print (separator)
print ("The plan for analysis:\n")
print ("1. Use TrimGalore to trim your data, during this process:\n")

if userinput["Pair_end"][0] == "YES":
    print ("Your dataset will be read as \"Pair end\" files:\n")
    for i in range(1, len(pair_list.keys())+1):
        print ("pair_%s: %s" % (i, pair_output(pair_list["pair_%s" % i])))
else:
    print ("Your dataset will be read as \"Single\" files:\n")
    for i in process_files:
        print ("%s" % i)
print ("Trimmed dataset will be stored in TBMI_ChIP/output/trim_galore_output\n")
print (separator)

print ("2. Use FastQC to check the quality of your trimmed dataset\n")
print ("FastQC output will also be stored in TBMI_ChIP/output/trim_galore_output\n")

print (separator)
print ("3. Use Bowtie2 to align your sequencing results:\n")

if userinput["Pair_end"][0] == "YES":
    print ("Your trimmed dataset will be run in Bowtie2 as paired end reads\n")
else:
    print ("Your trimmed dataset will be run in Bowtie2 as unpaired reads\n")

print ("Bowtie2 output will be stored in TBMI_ChIP/output/bowtie2\n")


print (separator)
if userinput["Multi_lane"][0] == "YES":
    print ("4. After Bowtie2, the following dataset will be merged and sorted then converted to BAM files for peak calling:\n")
    singlet = []
    for i in userinput["Replicate"]:
        singlet += i.split(":")
    for i in singlet:
        print ("%s:\n" % i)
        print pattern_in_list(i, file_list)
else:
    print ("4. After Bowtie2, the dataset will be sorted then converted to BAM files for peak calling\n")

print ("The BAM files for peak calling will be stored in TBMI_ChIP/output/sorted_BAM\n")

print (separator)

print ("5. Use MACS2 to call peak based on your setting for control and experiment pairs.\n")
print ("Please check if there is any issues for the splitting:")
num = 1
for i in userinput["Replicate"]:
    con, exp = i.split(":")
    print ("Pair %i:" % num)
    print (" Control:")
    for j in pattern_in_list(con, file_list):
        print (" %s" % j)
    print (" Experiment:")
    for k in pattern_in_list(exp, file_list):
        print (" %s" % k)
    num += 1

print (separator)

