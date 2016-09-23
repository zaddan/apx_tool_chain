import os
import sys
l_of_files = os.listdir(".")
for file_name in l_of_files:
    if (file_name[-4:] == ".png"):
        os.system("display " + file_name + " &")
