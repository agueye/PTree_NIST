import sys, gzip, bz2
import networkx as nx
import pickle
#from networkx.readwrite import json_graph
#import json
#import country_codes as cc

#conts = cc.conts  # Continents


AFR_Codes = ['AO','BJ','CV','KM','ER','LY','DZ','BW','BF','BI','CM','CF','TD','CG','CD','CI','DJ','EG','GQ','ET','GA','GM','GH','GN','GW','KE','LS','LR','MG','MW','ML','MR','MU','MA','MZ','NA','NE','NG','RW','SN','SL','SO','SS','SD','SZ','TG','TN','UG','EH','ZA','ZM','ZW','YT','ST','RE','SC','SH','TZ','EH']

base="../../../../../ITDK/ITDK-"
res="../../../../datafiles/data-ITDK/"

def build_graph(rp,ext=1):
        src = base+rp+"/"
        print("Building graph for ", src)
        # Deal with the different file extensions over the years
        if ext==1:
                n_filename = src+"kapar-midar-iff.nodes.geo.gz"
                nodeinfo = gzip.GzipFile(n_filename, 'r')
                l_filename = src+"kapar-midar-iff.links.gz"
                source = gzip.GzipFile(l_filename, 'r') 
        else:
                n_filename = src+"kapar-midar-iff.nodes.geo.bz2"
                l_filename = src+"kapar-midar-iff.links.bz2"


        
        print("Reading the input file....")
        if 1==0:
                nodeinfo_f = bz2.BZ2File(n_filename, 'rb') 
                nodeinfo=nodeinfo_f.read()
        else: 
                with  bz2.open(n_filename, 'rt',encoding='ISO-8859-1') as nodeinfo_f:
                        nodeinfo=nodeinfo_f.readlines()
        # Extacting the nodes
        print("Done Reading........Number of nodes: ", len(nodeinfo))
        #print(nodeinfo[0:10])
        node_ccs={}
        for line in nodeinfo:
                if line[0]=='#':continue
                #print(line)
                node_ccs[line.split()[1].strip(':')] = line.split()[3]  # Store the country code

        del nodeinfo
        print("Building the graph...")
        g = nx.Graph() 
	# Extacting the links

        with bz2.open(l_filename, 'rt',encoding='ISO-8859-1') as  source_f:
                source=source_f.readlines()

        for line in source:
                if line.strip().startswith('#'):continue
                nl = line.strip().split(" ")[3:]  # Split the line and get the list of nodes connected to this link (ATM, Ethernet, POS, etc..)
                nl = [x.split(":")[0] for x in nl] # Use only the node (the second number after the ':' is the interface
                
                for i in range(len(nl)):              # Create a "link" between any two nodes present in this link
                        for j in range(i+1,len(nl)):
                                try: 
                                        cc1 = node_ccs[nl[i]]
                                except KeyError: cc1 = '??'
                                try:
                                        cc2 = node_ccs[nl[j]]
                                except KeyError: cc2 = '??'

                                if cc1 in AFR_Codes and cc2 in AFR_Codes:
                                        g.add_node(cc1)
                                        g.add_node(cc2)
                                        g.add_edge(cc1,cc2)


        print("Done now...writing the file.")
        nx.write_gpickle(g,res+"Africa.cc."+rp+".gpickle.gz")
        print("Really done now...")


###################################
import sys
rep = sys.argv[1]
mod = int(sys.argv[2])
build_graph(rep,mod)

