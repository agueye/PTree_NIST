# This code is for importing list(s) of AS paths and converting them into
# country code (cc) paths.

import pickle
import gzip

def getccpaths(wmonitors=False,wsets=False,targetcc=[]):
    fileobject=gzip.open(pathDataFilename,'rt')
    count=0  
    ccmap={} 
    batchsize=40*5000000 # 40 chars per line, 5 million lines
    data=fileobject.readlines(batchsize)
    while data!=[]: # and count<10000:
        for line in data:
            count=count+1
            if count % 1000000==0:
                print(".")
                if count % 20000000==0:
                    print(" ",count)
            
            linedata=line.split('|')                  
            cclist=[]
            monitor=linedata[0]
            prior=None
            for x in range(len(linedata)-1):
                asn=linedata[x]
                if asn in asn_to_cc:
                    cc=asn_to_cc[asn]
                else:
                    cc="U"    
                if cc!=prior:
                    cclist.append(cc) 
                prior=cc
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
        #if count>500000:
        #    data=[]
        #else: 
        #    data=fileobject.readlines(batchsize) # get next batch of lines

        data=fileobject.readlines(batchsize) # get next batch of lines
    fileobject.close()    
    return ccmap

def write_ccmap_to_disk(wmonitors,wsets,ccmap,oneset=False):
    mode="paths"
    if wsets:
        mode="sets"
    if oneset:
        mode="1set"
    mon=""
    if wmonitors==False:
        mon="-0mon"
    filename="../datafiles/ccmap-"+mode+mon+".txt"       
    fileobject=open(filename,'w')
    print("\nWriting ccmap to files",filename)
    sources=ccmap.keys()
    sources.sort()
    for src in sources:
        destinations=ccmap[src].keys()
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

#pathDataFilename='../20151201_IPV4_with_prefix.all-paths_reduced'
pathDataFilename='/scratch/CAIDA/PrivacyTree/datafiles/data-BGPSTRM/2015-allpaths-sorted.gz'
asntocc_filename='../asn_to_cc.pkl'

fileobject=open(asntocc_filename,'rb')
asn_to_cc=pickle.load(fileobject)
fileobject.close()
ccset=set(asn_to_cc.values()) # Set of all observed country codes

print("Generating ccmap")
ccmap=None # Clear memory from past run
cc_to_asn=None
targetcc=[]

wmonitors=False
wsets=True
ccmap=getccpaths(wmonitors,wsets,targetcc)
write_ccmap_to_disk(wmonitors,wsets,ccmap) 
write_ccmap_to_disk(wmonitors,wsets,ccmap,oneset=True) 

wmonitors=False
wsets=False
ccmap=getccpaths(wmonitors,wsets,targetcc)
write_ccmap_to_disk(wmonitors,wsets,ccmap) 

wmonitors=True
wsets=True
ccmap=getccpaths(wmonitors,wsets,targetcc)
write_ccmap_to_disk(wmonitors,wsets,ccmap) 

wmonitors=True
wsets=False
ccmap=getccpaths(wmonitors,wsets,targetcc)
write_ccmap_to_disk(wmonitors,wsets,ccmap) 
