import os
import sys

#l_of_files = os.listdir(".")
base_dir = sys.argv[1]
l_of_files = os.listdir(base_dir)
for file_name in l_of_files:
    if (file_name[-4:] == ".png"):
        os.system("display " + base_dir + file_name + " &")
