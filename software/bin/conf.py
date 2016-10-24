# get reauired tools:
from sys import platform
import subprocess

def subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print proc_stdout

if platform == "darwin":
	print("you are using OS X --> install required GNU utils:")
	subprocess.call(["alias", "zcat=gzcat", "sed=gsed"], shell=True)
	#subprocess_cmd("alias zcat=gzcat sed=gsed")
	#subprocess_cmd("brew install coreutils gnu-sed ; alias zcat=gzcat sed=gsed")

else:
	print("your platform is %s" % platform)



