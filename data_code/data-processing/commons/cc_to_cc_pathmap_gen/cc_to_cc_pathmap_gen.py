# This code is for importing list(s) of AS paths and converting them into
# country code (cc) paths.

import pickle

def getccpaths(wmonitors=False,wsets=False,targetcc=[]):
    fileobject=open(pathDataFilename,'r')
    count=0  
    ccmap={} 
    batchsize=40*5000000 # 40 chars per line, 5 million lines
    data=fileobject.readlines(batchsize)
    while data!=[]: # and count<10000:
        for line in data:
            #print(line)
            count=count+1
            if count % 1000000==0:
                print(".")
                if count % 20000000==0:
                    print(" ",count)
            
            linedata=line.split('|')                  
            cclist=[]
            if len(linedata)==2: #This is the case where the src=dst
                linedata.insert(1,linedata[0])
                
            monitor=linedata[-1]
           
            cclist=linedata[0:-1]
            src=cclist[0]
            dst=cclist[-1]         
            if (src not in targetcc or dst not in targetcc) and len(targetcc)>0:
                continue     
            cclist=cclist[1:-1]
            if wsets: # remove duplicates for each path and sort by cc name
                cclist=set(cclist)
                if src in cclist: 
                    cclist.remove(src)
                if dst in cclist:
                    cclist.remove(dst)
                cclist=list(cclist)
                cclist.sort()
            if src not in ccmap:
                ccmap[src]={}
            if dst not in ccmap[src]:
                ccmap[src][dst]=set()
            if wmonitors:
                cclist.append(monitor)
            ccmap[src][dst].update([tuple(cclist)])         
        
        data=fileobject.readlines(batchsize) # get next batch of lines
    fileobject.close()    
    return ccmap

def write_ccmap_to_disk(wmonitors,wsets,ccmap,year,oneset=False):
    mode="paths"
    if wsets:
        mode="sets"
    if oneset:
        mode="1set"
    mon=""
    if wmonitors==False:
        mon="-0mon"
    filename="../"+str(year)+".ccmap-"+mode+mon+".txt"       
    fileobject=open(filename,'w')
    print("\nWriting ccmap to files",filename)
    sources=list(ccmap.keys())
    sources.sort()
    for src in sources:
        destinations=list(ccmap[src].keys())
        destinations.sort()
        for dst in destinations:
            if oneset==False:
                for path in ccmap[src][dst]:
                    theline=src                           
                    if wmonitors:
                        monitor=path[-1]  
                        for x in range(0,len(path)-1):
                            theline=theline+"|"+path[x]  
                        theline=theline+"|"+dst+"|"+monitor+"\r\n"               
                    else:
                        for x in range(0,len(path)):
                            theline=theline+"|"+path[x]                      
                        theline=theline+"|"+dst+"|"+"0"+"\r\n" 
                    fileobject.write(theline)
            else:
                assert wmonitors==False
                assert wsets==True
                ccset=set()
                for path in ccmap[src][dst]:
                    ccset.update(path) # adds each element of path to set
                ccset=list(ccset)
                ccset.sort()
                theline=src   
                for cc in ccset:
                    theline=theline+"|"+cc
                theline=theline+"|"+dst+"|"+"0"+"\r\n" 
                fileobject.write(theline)                                        
    fileobject.close()
    
# BEGIN MAIN PROCEDURE ************************************************

years=[2015, 2016]

for year in years:
    
    #pathDataFilename='../20151201_IPV4_with_prefix.all-paths_reduced'
    #asntocc_filename='../asn_to_cc.pkl'
    pathDataFilename='../yearlyGeoFiles/'+str(year)+".geodata.txt"
    asntocc_filename='../'+str(year)+'.cc_to_mon.pkl'


    fileobject=open(asntocc_filename,'rb')
    asn_to_cc=pickle.load(fileobject)
    fileobject.close()
    ccset=set(asn_to_cc.keys()) # Set of all observed country codes
    print(ccset)

    print("Generating ccmap for \t", year)
    ccmap=None # Clear memory from past run
    cc_to_asn=None
    targetcc=[]

    wmonitors=False
    wsets=True
    ccmap=getccpaths(wmonitors,wsets,targetcc)
    write_ccmap_to_disk(wmonitors,wsets,ccmap,year) 
    write_ccmap_to_disk(wmonitors,wsets,ccmap,year,oneset=True) 

    wmonitors=False
    wsets=False
    ccmap=getccpaths(wmonitors,wsets,targetcc)
    write_ccmap_to_disk(wmonitors,wsets,ccmap,year) 

    wmonitors=True
    wsets=True
    ccmap=getccpaths(wmonitors,wsets,targetcc)
    write_ccmap_to_disk(wmonitors,wsets,ccmap,year) 

    wmonitors=True
    wsets=False
    ccmap=getccpaths(wmonitors,wsets,targetcc)
    write_ccmap_to_disk(wmonitors,wsets,ccmap,year) 
