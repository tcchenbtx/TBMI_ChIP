# -*- coding: utf-8 -*-

import os
import re
import json
from tools import identify_treatment_groups
from tools import Pure_fa

# genome reference files for:
genome_ref = {}
genome_ref["mm10"] = "http://hgdownload.soe.ucsc.edu/goldenPath/mm10/bigZips/chromFa.tar.gz"
genome_ref["mm9"] = "http://hgdownload.soe.ucsc.edu/goldenPath/mm9/bigZips/chromFa.tar.gz"
genome_ref["hg18"] = "http://hgdownload.soe.ucsc.edu/goldenPath/hg18/bigZips/chromFa.zip"
genome_ref["hg19"] = "http://hgdownload.soe.ucsc.edu/goldenPath/hg19/bigZips/chromFa.tar.gz"


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

idr_path = os.path.join(base_path, "software", "idrCode")
meme_path = os.path.join(base_path, "software", "meme")

# MEME_databse setting:
MEME_database = os.path.join(meme_path, "db", "motif_databases", "JASPAR", "JASPAR_CORE_2014_vertebrates.meme")



# get userinput
with open("userinput.json") as uinput:
    userinput = json.load(uinput)


# get overlap files
all_idr_output = []
for (dirpath, dirnames, filenames) in os.walk(output_IDR):
    all_idr_output.extend(filenames)
    break

overlap_files = []
for i in all_idr_output:
    overlap_files.extend(re.findall(u'.*\-overlapped-peaks.txt$', i))

# default database:
meme_db = os.path.join(base_path, "software", "meme", "db", "motif_databases", "JASPAR", "JASPAR_CORE_2014_vertebrates.meme")

# check directory
if not os.path.exists(output_IDR_forMEME):
    os.makedirs(output_IDR_forMEME)

# run meme with overlap peaks
with open("Makefile", "a") as mk:
    mk.write("meme_1:\n")
    mk.write("\t#prepare input files for MEME\n")
    mk.write("\tcd %s && wget %s\n" % (reference_folder, genome_ref["%s" % userinput["Reference"][0]]))
    mk.write("\tcd %s && %s\n" % (reference_folder, "unzip chromFa.zip" if (userinput["Reference"][0] == "hg18") else "tar -xvzf chromFa.tar.gz"))

    mk.write("meme_2:\n")
    faidx_ref = os.path.join(reference_folder, "reference.fastq")
    mk.write("\tcd %s && cat %s > %s\n" % (reference_folder, Pure_fa(reference_folder), faidx_ref))
    for i in overlap_files:
        temp_for_meme = os.path.join(output_IDR_forMEME, "temp_%s.bed" % i[:-4])
        file_for_meme = os.path.join(output_IDR_forMEME, "%s_MEME.bed" % i[:-4])
        file_for_meme_final = os.path.join(output_IDR_forMEME, "%s_MEME.fastq" % i[:-4])
        mk.write("\tcd %s && " % (output_IDR) + r"""awk 'NR>=2 {printf "%s\t%10i\t%10i\t%10i\n",$$2,$$3,$$4,($$3+$$4)/2}' """ + "%s > %s\n" % (os.path.join(output_IDR, i), temp_for_meme))
        mk.write("\tcd %s && " % (output_IDR_forMEME) + r"""awk '{print $$1 "\t" $$4-50 "\t" $$4+50}' """ + "%s > %s\n" % (temp_for_meme, file_for_meme))
        mk.write("\tcd %s && " % (output_IDR_forMEME) + r"""awk '{print $$1 ":" $$2 "-" $$3}' """ + "%s | xargs samtools faidx %s > %s\n" % (file_for_meme, faidx_ref, file_for_meme_final))
    mk.write("\tcd %s && rm temp*\n" % output_IDR_forMEME)

    mk.write("meme_3:\n")
    for i in overlap_files:
        file_for_meme_final = os.path.join(output_IDR_forMEME, "%s_MEME.fastq" % i[:-4])
        mk.write("\tmeme-chip -oc %s -index-name %s -time 300 -order 1 -db %s -meme-mod zoops -meme-minw 6 -meme-maxw 30 -meme-nmotifs 3 -dreme-e 0.05 -centrimo-score 5.0 -centrimo-ethresh 10.0 %s" \
                 %(output_meme, i + "_meme.html", meme_db, file_for_meme_final))


    


