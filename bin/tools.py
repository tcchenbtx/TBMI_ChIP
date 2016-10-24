import re
import os

def pair_output(Pairinput):
    split_result = Pairinput.split()
    return ("%s\n        %s" % (split_result[0], split_result[1]))


def pattern_in_list(Pattern, Mylist):
    result = []
    for i in Mylist:
        if re.match(Pattern, i):
            result.append(i)
    return result

def identify_treatment_groups (Filelist, Treatmentlist):
    result = []
    for i in Treatmentlist:
        treat_group = []
        for j in Filelist:
            if re.match(u'.*%s.*' % i, j):
                treat_group.append(j)
        result.append(treat_group)
        result = filter(None, result)
    return result

def Pair_up_IDR (Idr_input, Output):
    if len(Idr_input) > 2:
        Output += zip([Idr_input[0]]*(len(Idr_input)-1), Idr_input[1:])
        Idr_input = Idr_input[1:]
        myfunc(Idr_input, Output)
    else:
        Output.append(tuple(Idr_input))
    return Output

def Pure_fa (Reference_path):
    list_files = []
    for (dirpath, dirnames, filenames) in os.walk(Reference_path):
        list_files.extend(filenames)
        break
    target_data = []

    for i in list_files:
        if re.match(u'^chr[0-9]+.fa$', i):
            target_data.append(i)
    target_data.sort(key=lambda x: int(x[3:-3]))

    all_str = ""
    for i in target_data:
        all_str += (i + " ")
    all_str += "chrX.fa chrY.fa chrM.fa"

    return all_str
