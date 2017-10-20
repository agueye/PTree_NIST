# This code is for importing list(s) of AS paths and converting them into
# country code (cc) paths.

import pickle
import numpy as np
import matplotlib.pyplot as plt

EU_cc= ['BE','BG','CZ','DK','DE','EE','IE','EL','ES','FR','HR','IT','CY','LV','LT','LU','HU','MT','NL','AT','PL','PT','RO','SI','SK','FI','SE','GB','UK']

def import_monitors(filename,thresh=10):
    fileobject=open(filename,'r')
    linecount=0  
    count={}
    monitors=[]
    batchsize=40*5000000 # 40 chars per line, 5 million lines
    data=fileobject.readlines(batchsize)
    while data!=[]: # and count<10000:
        for line in data:
            linecount+=1
            if linecount % 1000000==0:
                print(".")
                if linecount % 20000000==0:
                    print(" ",linecount)      
            linedata=line.split('|')
            cclist,pathcount=cleanline(linedata)
            if len(cclist)<1:
                continue
            src=cclist[0]
            if src not in monitors:
                monitors.append(src)
            if src not in count:
                count[src]=0
            count[src]+=1
        #if count>500000:
        #    data=[]
        #else: 
        #    data=fileobject.readlines(batchsize) # get next batch of lines
        data=fileobject.readlines(batchsize) # get next batch of lines    
    fileobject.close()    
    tmp=monitors[:]
    for mon in tmp:
        if count[mon]<thresh:
            monitors.remove(mon)
    monitors.sort()
    return monitors

def cleanline(linedata):
    pathcount=int(linedata[-1])
    linedata=linedata[0:-3] # strip off pathcount and monitor name 
    cleaned=[]
    prior=0
    for cc in linedata:
        if cc=='UK': 
            cc='GB'
        if cc=='U' or cc=='??' or cc=='A1': # A1 is anonymous proxy
            cleaned=[]
            break
            #continue
        if cc not in cc2name and cc!='AP' and cc!='A2': # approved ISO codes, AP: Asia/Pacific, A2: space
            print("ERROR - UNKOWN COUNTRY CODE",cc)
            cleaned=[]
            break
        if cc in EU_cc:
            cc='EU'
        if cc!=prior:
            cleaned.append(cc)
        prior=cc
    return cleaned,pathcount
    
def import_involved(filename,src,threshold=0):
    fileobject=open(filename,'r')
    uscount=0
    linecount=0  
    involved={}
    cinvolved={}
    dmin={}
    dmean={}
    count={}
    batchsize=40*5000000 # 40 chars per line, 5 million lines
    data=fileobject.readlines(batchsize)
    while data!=[]: # and count<10000:
        for line in data:
            linecount+=1
            if linecount % 1000000==0:
                print(".")
                if linecount % 20000000==0:
                    print(" ",linecount)         
            linedata=line.split('|')
            #assert len(linedata)>=4
            if linedata[0]=='??': continue


            if len(linedata)<4:
                linedata.insert(1,linedata[0])

            cclist,pathcount=cleanline(linedata)
            if len(cclist)==0 or cclist[0]!=src: # cclist has unknowns or doesn't pertain to src
                continue
            dst=cclist[-1]
            #if dst=='US' and len(cclist)==1:
                #print("************")
                #print(cclist,pathcount,linedata)
            #cclist=cclist[:-1] # remove dst
            ccset=set(cclist)
            ccset.remove(src)             
            #if dst in ccset:
            #    ccset.remove(dst) 
            if dst not in count:
                cinvolved[dst]={}
                dmin[dst]=len(ccset)
                dmean[dst]=0
                count[dst]=0          
            #if src==dst: print ccset
            if dmin[dst]>len(ccset):
                dmin[dst]=len(ccset)
            dmean[dst]+=len(ccset)*pathcount
            count[dst]+=pathcount # counts number of data items
            
            if dst=='US' and len(ccset)==0: 
                uscount+=pathcount
            
            for cc in ccset:
                if cc not in cinvolved[dst]:
                    cinvolved[dst][cc]=0
                cinvolved[dst][cc]+=pathcount
                
        #if count>500000:
        #    data=[]
        #else: 
        #    data=fileobject.readlines(batchsize) # get next batch of lines
        data=fileobject.readlines(batchsize) # get next batch of lines    
    fileobject.close()    
    for cc in dmean.keys():
        dmean[cc]=dmean[cc]*1.0/count[cc]
        dmean[cc]=round(dmean[cc],1) # round to tenths digit
    
    if threshold>0:
        for dst in count.keys():
            involved[dst]=set()
            for cc in cinvolved[dst].keys():
                if cinvolved[dst][cc]*1.0/count[dst]>=threshold and dst != cc:
                    involved[dst].add(cc)
    #print(involved['US'],count['US'],cinvolved['US']['EU'],uscount)
    #print(involved,count,cinvolved,uscount)
    return involved,dmin,dmean

# BEGIN MAIN PROCEDURE ************************************************

def plot_involved(src,involved,xvalues,xlabel):
    ymean={}
    count={}
    ymax=0
    for cc in involved.keys():
        xvalue=xvalues[cc]     # Value of dmin or dmean
        yvalue=len(involved[cc]) # Number of countries involved in dest=cc
        #if yvalue==1 and xvalue==1:
        #    print 1,1,cc,cc2name[cc]
        if ymax<yvalue:
            ymax=yvalue
        #print xvalue,yvalue
        plt.scatter(xvalue,yvalue)
        xvalue=round(xvalue)
        if xvalue not in ymean:
            ymean[xvalue]=0
            count[xvalue]=0
        ymean[xvalue]+=yvalue
        count[xvalue]+=1

    xvalues=ymean.keys()
    xvalues=sorted(xvalues)
    yvalues=[]
    for xvalue in xvalues:
        ymean[xvalue]=ymean[xvalue]*1.0/count[xvalue]
        yvalues.append(round(ymean[xvalue]))
    plt.plot(xvalues,yvalues)
    print("xvalues",[int(x) for x in xvalues])
    print("meanvalues",[int(y) for y in yvalues])
    
    # Plot number of countries at each x-value
    yvalues=[]
    for xvalue in xvalues:
        yvalues.append(count[xvalue])
    plt.plot(xvalues,yvalues)
    print("ncountries at each x",yvalues,"sum=",len(involved.keys()),"/",len(cc2name.keys())-len(EU_cc)+1)
        
    plt.ylabel('Involved Countries')
    plt.xlabel(xlabel)
    plt.title(cc2name[src]+" ("+src+")")
    plt.axis([0,max(count.keys()),0,ymax+10])    
    plt.show()  
    
#*********************************************************************

#mode='average_case'
#mode='worst_case'
threshold=.00001
plot_figs=0

filename='../../../datafiles/cc_to_name.pkl'
fileobject=open(filename,'rb')
cc2name=pickle.load(fileobject,encoding='latin1')
fileobject.close()

dataset="data-Geolocation/"
dataset="data-ASN/"

if dataset=="data-Geolocation/":
    years=[2015, 2016]
    resfile = "Results-Geolocation/involved/"
elif dataset=="data-ASN/":
    years=[2015]
    resfile = "Results-ASN/involved/"
else:
    print("Unknown Dataset....exiting")
    exit(1)



for year in years:
    filename="../../../datafiles/"+dataset+"yearlyFilesNoMon/"+str(year)+".data.nomon.txt"
    
    monitors=import_monitors(filename)
    print("monitors=",monitors, len(monitors))


    involved_all={}
    #monitors=['US']
    for target in monitors:
        assert target in monitors
        involved,dmin,dmean=import_involved(filename,target,threshold)
        involved_num={}
        for cc in involved:
            involved_num[cc]=len(involved[cc])
        #print(involved_num)
        involved_all[target]=involved_num
        #print('\n\n')
        print("Done with: ",target,"\t Number of Dest: ",len(involved.keys()))
        #print dmin

        if plot_figs==1:
            plot_involved(target,involved,dmin,'Min Country Distance')
            plot_involved(target,involved,dmean,'Mean Country Distance')



    fileobject2=open("../../../resultfiles/"+resfile+str(year)+".involved_data.pkl",'wb')
    pickle.dump(involved_all,fileobject2)
    fileobject2.close()

    #print(involved_all)
