import os
import time as t
import datetime
import json


def add_bee_event(log,bee_ID=-1,event_time=0,dir_out=True):
    if not bee_ID in log.keys():
        log[bee_ID]={'entries':[], 'exits': []} 

    if dir_out:
        log[bee_ID]['entries'].append(event_time)
    else:
        log[bee_ID]['exits'].append(event_time)
        

def analyze(cnt,pre_num_name,num_name,save_prefix,bee_log_dict,start_time,tag):
    print('here')
    BEE_LOG_FILE='BeeLog.json'
    fh_time_log=open(save_prefix+ 'ImgTimes.log','w')
    fh_id_log =  open(save_prefix  + 'ImgID.log'   ,'w')
    fh_time_log.write(num_name +'\t'+ datetime.datetime.today().isoformat() + '\n')
    os.system("./apriltag_demo -f tag36h11 " + save_prefix +"top" + num_name + ".jpg > " + save_prefix + 'var/'+num_name + ".txt & ")   
    print("Running file_analyze:"  + save_prefix + num_name)

    while not (os.path.exists(save_prefix + 'var/'+ num_name + ".txt")) or (os.stat(save_prefix + 'var/' + num_name + ".txt").st_size < 1000) : 
        t.sleep(1)

    f = open(save_prefix + 'var/' + num_name + ".txt", 'r')
    f.readline()
    line = f.readline()
    f.close()

    tag=[-1]
    '''look for tag'''
    
    if "detection" in line : 
        indx  = line.index('-')
        if (line[indx+2]).isdigit() :
            tag[0] = int(line[indx+1:indx+3])
        else : 
            tag[0] = int(line[indx+1])
    
    
        
    fh_id_log.write(num_name + '\t' + str(tag[0]) + '\n')    
    add_bee_event(bee_log_dict,tag[0],t.time()-start_time,'s1' in num_name)
    
     
    with open(save_prefix + BEE_LOG_FILE,'w+') as fh:
            json.dump(bee_log_dict,fh)
    os.system('sync')
    fh_id_log.close()
    fh_time_log.close()
    
    '''check if there's tag in previous image, otherwise delete image'''
    if cnt>1:
        f = open(save_prefix + 'var/' + pre_num_name + ".txt", 'r')
        f.readline()
        line = f.readline()
        f.close()
        pre_tag=[-1]
        if "detection" in line : 
            indx  = line.index('-')
            if (line[indx+2]).isdigit() :
                pre_tag[0] = int(line[indx+1:indx+3])
            else : 
                pre_tag[0] = int(line[indx+1])
        
        
        if pre_tag[0]==-1:
            os.system("sudo rm "+save_prefix+"top" + pre_num_name + ".jpg")
    os.system('sync')
