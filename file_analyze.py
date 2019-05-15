import os
import sys
import time

num_name = sys.argv[1]


if len(sys.argv) > 2:
    save_prefix = sys.argv[2]
    save_prefix += '/'
else:   
    save_prefix=''
    
print("Running file_analyze:"  + save_prefix + num_name)

while not (os.path.exists(save_prefix + 'var/'+ num_name + ".txt")) or (os.stat(save_prefix + 'var/' + num_name + ".txt").st_size < 1000) : 
    time.sleep(1)

f = open(save_prefix + 'var/' + num_name + ".txt", 'r')
f.readline()
line = f.readline()
print(line)
f.close()
entry = False
exit = False
tag = -1

if "detection" in line : 
    indx  = line.index('-')
    if (line[indx+2]).isdigit() :
        tag = int(line[indx+1:indx+3])
    else : 
        tag = int(line[indx+1])

file = open(save_prefix + "var/done_" + num_name + ".txt", "w+")
file.write("TAG: " + str(tag) + "\n")
file.close()
