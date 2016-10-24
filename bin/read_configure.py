import os
import re
from sys import platform
from tools import pair_output
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

# # set separator
# separator = "#"*80

# # parse configure file
# config_input = [line[:-1] for line in config_file]
# config_input = [re.sub(r'#.*', "", i) for i in config_input]
# config_input = [i for i in config_input if i != ""]
#
# indexnum = {}
# indexnum["Treatment"] = config_input.index("@Treatment:")
# indexnum["Multi_lane"] = config_input.index("@Multi_Lane:")
# indexnum["Replicate"] = config_input.index("@Replicate:")
# indexnum["Pair_end"] = config_input.index("@Pair_end:")
# indexnum["Reference"] = config_input.index("@Reference:")
#
# userinput = {}
# userinput["Treatment"] = config_input[indexnum["Treatment"]+1: indexnum["Multi_lane"]]
# userinput["Multi_lane"] = config_input[indexnum["Multi_lane"]+1: indexnum["Replicate"]]
# userinput["Replicate"] = config_input[indexnum["Replicate"]+1: indexnum["Pair_end"]]
# userinput["Pair_end"] = config_input[indexnum["Pair_end"]+1:indexnum["Reference"]]
# userinput["Reference"] = config_input[indexnum["Reference"]+1:]

# # get file_list
# file_list = []
# for (dirpath, dirnames, filenames) in os.walk(dataset_folder):
#     file_list.extend(filenames)
#     break


# # files to go through
# file_patten = ""
# for i in userinput["Treatment"]:
#     file_patten = file_patten + ".*" + i + ".*|"
# file_patten = file_patten[:-1]
#
# process_files = [i for i in file_list if re.match(file_patten, i)]
#
# # paired_end files
# pair_list = {}
# pair_file_path = {}
# if userinput["Pair_end"][0] == "YES":
#     pair_n = 1
#     for i in range(0, len(process_files), 2):
#         pair_list["pair_%s" % pair_n] = "%s %s" % (process_files[i], process_files[i+1])
#         pair_file_path["pair_%s" % pair_n] = "%s %s" % (os.path.join(dataset_folder, process_files[i]), os.path.join(dataset_folder, process_files[i+1]))
#         pair_n += 1

# # display userinput
# print (separator)
# print ("Your input:\n")
# inputlist = ["Treatment", "Multi_lane", "Replicate", "Pair_end"]
# for i in inputlist:
#     print ("%10s: %s" % (i, userinput[i]))
#
# print (separator)
# if userinput["Pair_end"][0] == "YES":
#     print ("Your dataset will be read as \"Pair end\" files:\n")
#     for i in range(1, len(pair_list.keys())+1):
#         print ("pair_%s: %s" % (i, pair_output(pair_list["pair_%s" % i])))
# else:
#     print ("Your dataset will be read as \"Single\" files:\n")
#     for i in process_files:
#         print ("%s" % i)
# print (separator)

# get userinput
with open("userinput.json") as uinput:
    userinput = json.load(uinput)

# get path info for all files
with open("process_files.txt", "r") as proF:
    process_files = [i[:-1] for i in proF.readlines()]

# get path info for each pair
with open("pair_file_path.json") as ploutput:
    pair_file_path = json.load(ploutput)


# check directory
if not os.path.exists(output_trim_galore):
    os.makedirs(output_trim_galore)

# construct Makefile -- for TrimGalore
with open("Makefile", "w+") as mk:
    # for TrimGalore
    mk.write("TrimGalore:\n")
    if userinput["Pair_end"][0] == "YES":
        if platform == "darwin":
            for i in pair_file_path.keys():
                mk.write("\tmac_trim_galore --paired --fastqc -o %s %s\n" % (output_trim_galore, pair_file_path[i]))
        else:
            for i in pair_file_path.keys():
                mk.write("\ttrim_galore --paired --fastqc -o %s %s\n" % (output_trim_galore, pair_file_path[i]))

    else:
        if platform == "darwin":
            for i in process_files:
                mk.write("\tmac_trim_galore --fastqc -o %s %s\n" % (output_trim_galore, os.path.join(dataset_folder, i)))
        else:
            for i in process_files:
                mk.write("\ttrim_galore --fastqc -o %s %s\n" % (output_trim_galore, os.path.join(dataset_folder, i)))

    # # for Bowtie2
    # mk.write("Bowtie2\n")
    # mk.write("\tcd %s && wget $s" % (reference_folder, rgenome[userinput["Reference"][0]]))
    #
    # if userinput["Pair_end"][0] == "YES":
    #     for i in range(1, len(trimed_pair_file_path.keys())+1):
    #         temp_list = trimed_pair_file_path["pair_%s" % i].split()
    #         temp_name = temp_list[0][:-12]
    #         mk.write("\tbowtie2 -x %s -1 %s -2 %s -s " % (userinput["Reference"][0], temp_list[0], temp_list[1]))
    #
    #