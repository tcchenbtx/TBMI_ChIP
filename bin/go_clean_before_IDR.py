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

# get userinput
with open("userinput.json") as uinput:
    userinput = json.load(uinput)

# get narrowPeak files
all_macs2_output = []
for (dirpath, dirnames, filenames) in os.walk(output_macs2):
    all_macs2_output.extend(filenames)
    break

narrowPeak_files = []
for i in all_macs2_output:
    narrowPeak_files.extend(re.findall(u'.*\.narrowPeak$', i))

# check directory
if not os.path.exists(output_clean_narrowPeak):
    os.makedirs(output_clean_narrowPeak)


# clean up ChrUn data
with open("Makefile", "a") as mk:
    mk.write("clean_up:\n")
    for i in narrowPeak_files:
        mk.write("\tawk '$$1 ~/chr[0-9]*$$|chrX$$|chrY$$|chrM$$/ { print }' %s > %s\n" % (os.path.join(output_macs2,i), os.path.join(output_clean_narrowPeak, i[:-11] + "_clean.narrowPeak")))