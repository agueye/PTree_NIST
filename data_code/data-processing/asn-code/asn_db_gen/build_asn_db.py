from os import listdir
from os.path import isfile, join
import pickle



if 0:
    f_path='../../../../../datafiles/asn_DB/db/asn/'

    files = [f for f in listdir(f_path) if isfile(join(f_path, f))]

    asn_to_cc={}
    for file in files:
        cc=file.split('_')[0]
        cc=cc.upper()
        with open(f_path+file,'r') as f:
            lines=f.readlines()
            for line in lines:
                asn=line[2:]
                asn=asn.strip('\n')
                if asn in asn_to_cc:
                    print("Conflict:\t", asn, cc, asn_to_cc[asn])
                    continue
                asn_to_cc[asn]=cc



    fileobject2=open("../asn_to_cc1.pkl",'wb')
    pickle.dump(asn_to_cc,fileobject2)
    fileobject2.close()

else:
    fileobject1=open("../asn_to_cc.pkl",'rb')
    asn=pickle.load(fileobject1)
    fileobject1.close()
    fileobject2=open("../asn_to_cc1.pkl",'rb')
    asn1=pickle.load(fileobject2)
    fileobject2.close()
    asn_m={**asn,**asn1}

    fileobject3=open("../asn_to_cc_M.pkl",'wb')
    pickle.dump(asn_m,fileobject3)
    fileobject3.close()
