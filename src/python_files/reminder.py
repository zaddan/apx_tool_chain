import sys
"""
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
"""    
#note: take a look at this website:
#https://pypi.python.org/pypi/termcolor

from termcolor import colored
def reminder(flag, text, type_rem ="MISC"):
    base = "***REMINDER: " 
    if flag:
        if (type_rem ==  "MOD"): #code modification necessary
            print colored(base + text, 'black', attrs=['bold'])
        if (type_rem == "CODE"):
            print colored(base + text, 'green')
        if (type_rem == "ASSUM"):
            print colored(base + text, 'orange')
        if (type_rem == "MISC"):
            print colored(base + text, 'blue', attrs=['bold'])
        if (type_rem == "URGENT"):
            print colored(base + text, 'red', attrs=['bold'])
