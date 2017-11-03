import os
import pickle
import gzip

record_monitors=True
asntocc_filename='../asn_to_cc_M.pkl'

fileobject=open(asntocc_filename,'rb')
asn_to_cc=pickle.load(fileobject)
fileobject.close()
#ccset=set(asn_to_cc.values()) # Set of all observed country codes

base='/scratch/CAIDA/PrivacyTree/datafiles/data-BGPSTRM/'

inputfiles=os.listdir('.')
for record_monitors in [False,True]:
    for year in [2015]:
                
        ccpaths={}
        count=0
        mismatch=0
        linecount=0           
        filepath='./'

        yearfiles=[base+str(year)+'-allpaths-sorted.gz']
        
        #yearfiles=['20151201_IPV4_with_prefix.all-paths_reduced']

        for filename in yearfiles:

            #fileobject=open(filepath+filename,'r')
            fileobject=gzip.open(pathDataFilename,'rt')
            batchsize=40*5000000 # 40 chars per line, 5 million lines
            data=fileobject.readlines(batchsize)

            while data!=[]: # and count<10000:
                for line in data:

                    count=count+1
                    if count % 100000==0: 
                        print(".")
                        if count % 10000000==0:
                            print(" ",count)

                    line=line.strip('\n')
                    linedata=line.split('|')
                    #linedata=linedata[:-1] # 
                    monitor = linedata[-1] 
                    monitorcc='??'

                    prior=''                
                    cclist=[]
                    for x in range(len(linedata)-1):
                        asn=linedata[x]
                        if asn in asn_to_cc:
                            cc=asn_to_cc[asn]
                        else:
                            cc="??"    
                        if cc!=prior:
                            cclist.append(cc) 
                        prior=cc

                    if len(linedata)<2:
                        mismatch+=1
                        continue                  
                    
                    if linedata[0]!=monitorcc:
                        mismatch+=1
                        
                    linecount+=1
                    if record_monitors==True:
                        a=1 #Do nothing
                        cclist.append(monitor) 
                    else:
                        cclist.append('0')
                    if tuple(cclist) not in ccpaths:
                        ccpaths[tuple(cclist)]=1
                    else:
                        ccpaths[tuple(cclist)]+=1
                    #print linedata
                    #print(linecount,mismatch)
                data=fileobject.readlines(batchsize) # get next batch of lines
            fileobject.close()
            #if count>100: break
            
        print("\nWriting processed data for year",year)
        print("Number of distinct paths=",len(ccpaths.keys()))
        print("Number of path instances=",linecount)
        if record_monitors==True:
            monstatus=''
            filepath='./'
        else:
            monstatus='.nomon'
            filepath='./'        
#        filename=filepath+str(year)+'.Geodata'+monstatus+'.pkl'
#        print filename
#        output=open(filename,'wb')
#        pickle.dump(ccpaths,output)
#        output.close()
    
        filename=filepath+str(year)+'.data'+monstatus+'.txt'
        print(filename)
        output=open(filename,'w')
        for path in ccpaths:
            line=""
            for elem in path:
                line=line+elem+'|'
            line=line+str(ccpaths[path])
            output.write(line+'\r\n')
        output.close()