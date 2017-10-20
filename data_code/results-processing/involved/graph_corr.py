import csv
import pickle
import networkx as nx
import matplotlib.pyplot as plt

g_base='../../../../datafiles/data-ITDK/'


dataset="data-Geolocation/"
dataset="data-ASN/"

if dataset=="data-Geolocation/":
    years=[2015, 2016]
    base = "../../../../resultfiles/Results-Geolocation/involved/"
    ds='2016-09'
elif dataset=="data-ASN/":
    years=[2015]
    base = "../../../../resultfiles/Results-ASN/involved/"
    ds='2015-08'
else:
    print("Unknown Dataset....exiting")
    exit(1)


for year in years:
    fileobject=open(base+str(year)+".involved_data.pkl",'rb')
    data = pickle.load(fileobject)
    fileobject.close()

    G = nx.read_gpickle(g_base+"World.cc."+ds+".gpickle.gz")
    bc=nx.betweenness_centrality(G)
    deg=G.degree()

    g_char='deg'
    g_char=''
    if g_char=='deg':
        hor_vals = deg
    else:
        hor_vals = bc
        
    
    #print(data)

    all_dest = []
    for item in data:
        dests= data[item].keys()
        all_dest+=dests

    all_dest = list(set(all_dest))
    all_dest.sort()

    corr_vals={}
    for item in data:
        tmp=[]
        dests= data[item].keys()
        for dest in all_dest:
            if dest not in dests:
                #tmp.append(0)
                continue
            else:
                tmp.append(data[item][dest])

        
        avr_num = sum(tmp)*1.0/len(tmp)
        if item in hor_vals:
            corr_vals[item]=[hor_vals[item],avr_num]
        else:
            corr_vals[item]=[-1,avr_num]
            
    #print(corr_vals.values())
    x_vals=[k[0] for k in corr_vals.values()]
    y_vals=[k[1] for k in corr_vals.values()]
    plt.plot(x_vals,y_vals,'*')
    plt.show()
        
    if 0:
        print("Done with: ",year)
        res_file = base+str(year)+".involved_data.csv"
        with open(res_file,'w') as f:
            writer=csv.writer(f)
            writer.writerows(dest_mat)
    
