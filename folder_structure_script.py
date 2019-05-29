#Script for copying files containing 'nolabels' or 'IAR' from the same folder to two separate folders, one for each type of image.
#Currently there is a minor bug, such that this will not work for both files simultaneously. In order to make lines 25-27 work, lines 22-24 
#need to be commented out and elif in line 25 needs to be replaced with an if.

import shutil
from glob import glob
import ipdb 

extensions = glob('*.jpg') 
string_match_1 = 'nolabels'
string_match_2 = 'IAR'

PATH_1 = 'C:/Users/maran/Desktop/Files Dissertation/training_data/selected_good_days_grayscale_unlabeled_2'
PATH_2 = 'C:/Users/maran/Desktop/Files Dissertation/training_data/selected_good_days_IARsignal_predicted_2'

list_good_days = 'list_good_days.txt'
with open(list_good_days, 'r') as handle:
    for line in handle: #152
        tokens = line.split()
        for filename in extensions:
                if (tokens[0]+'_'+tokens[1]+'_'+tokens[2]) in filename:                                
                    if string_match_1 in filename:
                        shutil.copy2(filename, PATH_1)
                        break
                    elif string_match_2 in filename:
                        shutil.copy2(filename, PATH_2)     
                        break
