import gzip

filename='../../datafiles/data-BGPStream/2015.allpaths.gz'
fileobject=gzip.open(filename,'rt')

#filename='../../datafiles/2015.allpaths.processed.gz'
filename='../../datafiles/data-BGPStream/2015.allpaths.processed.gz'
fileobject2=gzip.open(filename,'wb')

count=0  
paths=0
thrownout=0
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
        #print(type(line))
        linedata=line.split(' ')
        num_as=len(linedata)-2
        outline=""
        while num_as>-1:
            outline+=linedata[num_as]+'|'
            num_as-=1

        outline+=linedata[-1]
        fileobject2.write(','.join(str(x) for x in outline).encode("utf-8"))

        #fileobject2.write(outline)
        
    data=fileobject.readlines(batchsize) 

fileobject.close()    
fileobject2.close()    
