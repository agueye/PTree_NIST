# Get all the monitors belonging to one country

import pickle

filepaths=[]
filepaths.append('../../../../../datafiles/data-ASN/pre-processed')
#filepaths.append('../data-Geolocation')

years=[2015,2016]

for year in years:
    for filepath in filepaths:
        fileobject=open(filepath+"/"+str(year)+".ccmap-paths.txt",'r')
        batchsize=40*5000000 # 40 chars per line, 5 million lines 
        data=fileobject.readlines(batchsize)
        count=0
        cc2mon={}
        while data!=[]: # and count<10000:
            for line in data:
                count=count+1
                if count % 1000000==0:
                    print("."),
                    if count % 20000000==0:
                        print(" ",count)
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

        fileobject2=open(filepath+"/"+str(year)+".mon_to_cc.pkl",'wb')
        pickle.dump(cc2mon,fileobject2)
        fileobject2.close()
