import os
import re
import json

# identify path
base_path = os.path.abspath(os.path.dirname(__file__))
base_path = os.path.join(base_path, "..")

#config_file = open(os.path.join(base_path, "configure", "configure.txt"), "r")
dataset_folder = os.path.join(base_path, "dataset")
output_folder = os.path.join(base_path, "output")

output_trim_galore = os.path.join(output_folder, "trim_galore_output")
output_bowtie2 = os.path.join(output_folder, "bowtie2")

reference_folder = os.path.join(dataset_folder, "reference")

# get userinput
with open("userinput.json") as uinput:
    userinput = json.load(uinput)

# read trimgalore results:
temp_trimresult = []
for (dirpath, dirnames, filenames) in os.walk(output_trim_galore):
    temp_trimresult.extend(filenames)
    break

trimed_list = [i for i in temp_trimresult if re.match(u'.*gz$', i)]


trimed_pair_list = {}
trimed_pair_file_path = {}
if userinput["Pair_end"][0] == "YES":
    pair_n = 1
    for i in range(0, len(trimed_list), 2):
        trimed_pair_list["pair_%s" % pair_n] = "%s %s" % (trimed_list[i], trimed_list[i+1])
        trimed_pair_file_path["pair_%s" % pair_n] = "%s %s" % (os.path.join(output_trim_galore, trimed_list[i]), os.path.join(output_trim_galore, trimed_list[i+1]))
        pair_n += 1

# reference genome info:
rgenome = {}
rgenome["hg18"] = "ftp://ftp.ccb.jhu.edu/pub/data/bowtie2_indexes/hg18.zip"
rgenome["hg19"] = "ftp://ftp.ccb.jhu.edu/pub/data/bowtie2_indexes/hg19.zip"
rgenome["mm9"] = "ftp://ftp.ccb.jhu.edu/pub/data/bowtie2_indexes/mm9.zip"
rgenome["mm10"] = "ftp://ftp.ccb.jhu.edu/pub/data/bowtie2_indexes/mm10.zip"


# check directory
if not os.path.exists(reference_folder):
    os.makedirs(reference_folder)
if not os.path.exists(output_bowtie2):
    os.makedirs(output_bowtie2)

# construct Makefile -- for bowtie2
with open("Makefile", "a") as mk:
    mk.write("reference:\n")
    mk.write("\tcd %s && curl -O %s\n" % (reference_folder, rgenome[userinput["Reference"][0]]))
    mk.write("\tcd %s && unzip %s.zip\n" % (reference_folder, userinput["Reference"][0]))

    mk.write("bowtie2:\n")
    if userinput["Pair_end"][0] == "YES":
        for i in range(1, len(trimed_pair_file_path.keys())+1):
            temp_list = trimed_pair_file_path["pair_%s" % i].split()
            temp_name = trimed_pair_list["pair_%s" % i].split()[0][:-12]
            temp_bowtie2_output_path = os.path.join(output_bowtie2, "%s.sam" % temp_name)

            mk.write("\tcd %s && caffeinate bowtie2 -x %s -1 %s -2 %s -S %s\n" % (reference_folder, userinput["Reference"][0], temp_list[0], temp_list[1], temp_bowtie2_output_path))
    else:
        for i in trimed_list:
            temp_bowtie2_output_path = os.path.join(output_bowtie2, "%s.sam" % i[:-12])
            mk.write("\tcd %s && bowtie2 -x %s -U %s -S %s\n" % (reference_folder, userinput["Reference"][0], i, temp_bowtie2_output_path))
