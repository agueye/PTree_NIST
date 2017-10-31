import pickle

filename='20170101.as-org2info.txt'

fileobject=open(filename,'r')
asn2org={}
org2country={}
asn2country={}
data=fileobject.readlines()
section=0 # intro explanatory comments
for line in data:
    if line[0]=="#" and section==0: 
        continue
    elif line[0]=="#" and section==1:
        section=2 # as to org mapping section
        continue
    elif section==0:
        section=1 # org to country mapping section

    linedata=line.split('|')    
    if section==1:
        org=linedata[0]
        country=linedata[3]
        if country=='':
            country='??'
        org2country[org]=country
    elif section==2:
        asn=linedata[0]
        org=linedata[3]
        asn2org[asn]=org

for asn in asn2org.keys():
    cc=org2country[asn2org[asn]]
    if cc in ['BE','BG','CZ','DK','DE','EE','IE','EL','ES','FR','HR','IT','CY','LV','LT','LU','HU','MT','NL','AT','PL','PT','RO','SI','SK','FI','SE','GB','UK']: 
# UK isn't an official country code but is same as GB
#    if cc in ['UK']:
#        cc='GB'
#    if cc in ['BE','BG','CZ','DK','DE','EE','IE','EL','ES','FR','HR','IT','CY','LV','LT','LU','HU','MT','NL','AT','PL','PT','RO','SI','SK','FI','SE']: 
        cc='EU'
    asn2country[asn]=cc
    #print asn,asn2country[asn]
fileobject.close()

fileobject2=open("../asn_to_cc.pkl",'wb')
pickle.dump(asn2country,fileobject2)
fileobject2.close()
