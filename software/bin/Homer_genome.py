import json
import os

# identify path
base_path = os.path.abspath(os.path.dirname(__file__))
base_path = os.path.join(base_path, "..", "..")
main_bin_path = os.path.join(base_path, "bin")
target_make_file = os.path.join(base_path, "software", "Makefile")

# get userinput
with open(os.path.join(main_bin_path, "userinput.json")) as uinput:
    userinput = json.load(uinput)

#
with open(target_make_file, "a") as mk:
    mk.write("configure_Homer_genome:\n")
    mk.write("\tcd Homer && perl configureHomer.pl -install %s\n" % (userinput["Reference"][0]))


