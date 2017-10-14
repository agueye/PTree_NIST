# COLLECT ALL THE MONITORS THAT BELONG TO A COUNTRY
import pickle

filepaths=[]
#filepaths.append('../Data-ASN')
filepaths.append('../Data-Geolocation')


filenames=[]
for filepath in filepaths:
    fileobject=open(filepath+"/ccmap-paths.txt",'r')
    batchsize=40*5000000 # 40 chars per line, 5 million lines 
    data=fileobject.readlines(batchsize)
    count=0
    cc2mon={}
    while data!=[]: # and count<10000:
        for line in data:
            count=count+1
            if count % 1000000==0:
                print ".",
                if count % 20000000==0:
                    print " ",count
            linedata=line.split('|')  
            cc=linedata[0]
            mon=linedata[-1]
            mon=mon.strip()
            if cc not in cc2mon:
                cc2mon[cc]=set()
            cc2mon[cc].add(mon) 
        #if count>500000:
        #    data=[]
        #else: 
        #    data=fileobject.readlines(batchsize) # get next batch of lines
        data=fileobject.readlines(batchsize) # get next batch of lines
    fileobject.close() 

    fileobject2=open(filepath+"/cc_to_mon.pkl",'w')
    pickle.dump(cc2mon,fileobject2)
    fileobject2.close()
