import sys, gzip, bz2
import networkx as nx
import pickle
import matplotlib.pyplot as plt


#############
## Check how the properties of the graph are correlated to the privacy

base='../../../../datafiles/data-ITDK/'
ds=['2015-08','2016-03','2016-09']

for d in ds:
    G = nx.read_gpickle(base+"Africa.cc."+d+".gpickle.gz")
    bc=nx.betweenness_centrality(G)
    print("Dataset: ",d)
    print(nx.info(G))
    #print(bc)
    print("\n")
    #print(G.nodes())

    nx.draw(G,with_labels = True)
    plt.show()
