import os
import re
import json


# identify path
base_path = os.path.abspath(os.path.dirname(__file__))
base_path = os.path.join(base_path, "..")

dataset_folder = os.path.join(base_path, "dataset")
reference_folder = os.path.join(dataset_folder, "reference")
output_folder = os.path.join(base_path, "output")

output_BAM = os.path.join(output_folder, "sorted_BAM")
output_macs2 = os.path.join(output_folder, "macs2")
output_IDR = os.path.join(output_folder, "IDR_output")
output_IDR_forMEME = os.path.join(output_IDR, "forMEME")
output_meme = os.path.join(output_folder, "MEME_output")
output_IDR_forHomer = os.path.join(output_IDR, "forHomer")
output_Homer_annotation = os.path.join(output_folder, "Homer_annotation")

idr_path = os.path.join(base_path, "software", "idrCode")
meme_path = os.path.join(base_path, "software", "meme")

# get userinput
with open("userinput.json") as uinput:
    userinput = json.load(uinput)

# check directory
if not os.path.exists(output_IDR_forHomer):
    os.makedirs(output_IDR_forHomer)

if not os.path.exists(output_Homer_annotation):
    os.makedirs(output_Homer_annotation)

# get overlap files
all_idr_output = []
for (dirpath, dirnames, filenames) in os.walk(output_IDR):
    all_idr_output.extend(filenames)
    break

print (all_idr_output)

overlap_files = []
for i in all_idr_output:
    overlap_files.extend(re.findall(u'.*\-overlapped-peaks.txt$', i))
print (overlap_files)

# construct makefile
with open("Makefile", "a") as mk:
    mk.write("Homer_annotation:\n")
    for i in overlap_files:
        target_file = i[:-4]
        file_name_forhomer_temp = os.path.join(output_IDR_forMEME, "%s_MEME.bed" % i[:-4])
        file_name_forhomer = os.path.join(output_IDR_forHomer, "%s_forHomer.bed" % i[:-4])
        mk.write("\t" + """sed 's/"//g' """ + "%s > %s\n" % (file_name_forhomer_temp, file_name_forhomer))
        mk.write("\tannotatePeaks.pl %s %s > %s_annotation.txt\n" % (file_name_forhomer, userinput["Reference"][0], os.path.join(output_Homer_annotation, i[:-4])))
