import os
import sys
import glob
def getNameOfFilesInAFolder(folderAddress):
    if not(os.path.isdir(folderAddress)):
            print "the folder with the name " + folderAddress + " (for which you requested to get the files for does not exist" 
            exit()
    else:
        return glob.glob(folderAddress + "/*")




def comeUpWithNewFolderNameAccordingly(folderToCopyTo):
    fileList = getNameOfFilesInAFolder(folderToCopyTo)
    if not(len(fileList) == 0): 
        newestFolder = max(glob.iglob(folderToCopyTo+"/*") , key=os.path.getctime) #getting the newst folder
        if((newestFolder[-3:]).isdigit()):
            suffix = newestFolder[-3:]
        elif((newestFolder[-2:]).isdigit()):
            suffix = newestFolder[-2:]
        elif((newestFolder[-1:]).isdigit()):
            suffix = newestFolder[-1:]
    else:
        suffix = -1 

    newFolderFullAddress = "backup_" + str(int(suffix) + 1)
    return newFolderFullAddress

#print comeUpWithNewFolderNameAccordingly("test_folder")

def main():
    benchmark_name = raw_input("name of the benchmark:  ")
    run_nature = raw_input("run nature: (ref for only reference and complete for a complete run): ")
    print run_nature 
    if (not((run_nature == "ref")or (run_nature == "complete"))):
        print "this run nature is not defined"
        exit()
     
    backup_folder = comeUpWithNewFolderNameAccordingly("res_bu/"+run_nature+"/"+benchmark_name+"/")
    os.system("mkdir  res_bu/"+run_nature+"/"+benchmark_name+"/"+ backup_folder)
    os.system("cp config.txt res_bu/"+run_nature+"/"+benchmark_name+"/"+ backup_folder)
    os.system("cp nohup.out res_bu/"+run_nature+"/"+benchmark_name+"/"+ backup_folder)
    
    if (run_nature == "complete"):
        os.system("cp compare_results.txt res_bu/"+run_nature+"/"+benchmark_name+"/"+ backup_folder)
        os.system("cp pareto_of_heur_flattened res_bu/"+run_nature+"/"+benchmark_name+"/"+ backup_folder)
        os.system("cp all_of_flattned res_bu/"+run_nature+"/"+benchmark_name+"/"+ backup_folder)
        os.system("cp pareto_of_al_of_flattned res_bu/"+run_nature+"/"+benchmark_name+"/"+ backup_folder)
        os.system("cp all_of_s2 res_bu/"+run_nature+"/"+benchmark_name+"/"+ backup_folder)
        os.system("cp all_of_s3 res_bu/"+run_nature+"/"+benchmark_name+"/"+ backup_folder)
        os.system("cp pareto_set_file.txt res_bu/"+run_nature+"/"+benchmark_name+"/"+ backup_folder)
        os.system("cp pareto_of_combined res_bu/"+run_nature+"/"+benchmark_name+"/" + backup_folder)
        os.system("cp all_of_combined res_bu/"+run_nature+"/"+benchmark_name+"/" + backup_folder)

    os.system("cp settings.py res_bu/"+run_nature+"/"+benchmark_name+"/"+ backup_folder)
    os.system("cp inputs.py res_bu/"+run_nature+"/"+benchmark_name+"/"+ backup_folder)
    os.system("cp results.png res_bu/"+run_nature+"/"+benchmark_name+"/"+ backup_folder)
    #os.system("cp ref.png res_bu/"+run_nature+"/"+benchmark_name+"/"+ backup_folder)
    os.system("cp log res_bu/"+run_nature+"/"+benchmark_name+"/"+ backup_folder)
 
main()
