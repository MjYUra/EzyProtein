###This script contains the function pair_search that require input of a protein 
###and returns all its interacting partners


    
#print(l[0][0])
import glob
import os

	
def pair_search(p1,f):

    f.seek(0, 0)
    f.readline() #to skip the first row (which are titles)
    r=[]
    for line in f:
        split_column = line.split("\t"); #\t for tab 
        y = split_column[3];
        x = split_column[1];
        #y = y[:-1];
        if(p1==y and p1 not in r):
            r.append(x);
        elif(p1==x and p1 not in r):
            r.append(y);
        else:
            continue;	
    #f.close();
    return r
	
def pairs_search(p,d,r,c,n,e,f):
	#prev.append(p["name"]);
    tmp = pair_search(p,f);
    if not tmp:
        return '';

    r["nodes"].append({ "id": c, "label": p});
    n[p]=c;

    for x in tmp:
        if(d!=0 and x not in n):
            e.add(frozenset({c,len(r["nodes"])+1}));
            r["edges"].append({"from":c,"to":len(r["nodes"])+1});
            pairs_search(x,d-1,r,len(r["nodes"])+1,n,e,f);
        elif(x in n):
            if({c,n[x]} in e):
                continue;
            else:
                e.add(frozenset({c,n[x]}));
                r["edges"].append({"from":c,"to":n[x]});
	
    """
    if(d!=0):
        tmp = pair_search(p["name"]);
        if not tmp:
            return '';

        for x in tmp:
            child = {
				"name":x,
				"children":[]
			}
            p["children"].append(child);
        for x in p["children"]:
            pairs_search(x,d-1);
    """
		
    return r;
	
def getModel(p1,p2):
    with open("human_structural_interactome.txt","r") as model:
        model.readline() #to skip the first row (which are titles)
        for line in model:
            split_column = line.split("\t"); #\t for tab 
            y = split_column[3];
            x = split_column[1];
            
        #y = y[:-1];
            if((p1==y and p2==x) or (p1==x and p2==y)):
                r="pdb"+split_column[6]+".pdb";
                try:
                    m = open("./models/"+r,"r");
                    m.close();
                    return r;
                    
    # Do something with the file
                except FileNotFoundError:
                    continue;
                
                
            else:
                continue;	
    #f.close();
    return 0;
	
def calculateg (model, mutation):
    
    result=0
    path=os.path.abspath(os.path.dirname(__file__))
    
    r=open (path+"/config/repair.cfg",'w+')
    r.write('command=RepairPDB' + '\n' + 'pdb-dir=./models' + '\n' + 'output-dir=./tem'+ '\n' +'pdb='+model)
    r.close()
    command='cd %s' % path
    os.system(command)
    os.system('foldx -f ./config/repair.cfg')
    with open (path+"/config/pssm.cfg",'w+') as p:
        p.write('command=Pssm' + '\n' + 'pdb-dir=./tem' + '\n' + 'output-dir=./re' + '\n' +'pdb='+model[:-4]+'_Repair.pdb' + '\n' + 'positions='+mutation + '\n' + 'aminoacids='+mutation[-1])
    os.system(command)
    os.system('foldx -f ./config/pssm.cfg')
	
    with open (path+'/re/PSSM_'+model[:-4]+'_Repair.txt','r') as re:
        re.readline()
        lines=re.readline(10000)
        result=lines.split("\t")[1]
    tmp=glob.glob(path+'/tem/*')
    for f in tmp:
        os.remove(f)
    
    re=glob.glob(path+'/re/*')
    for x in re:
        os.remove(x)	
    return result;
	
#result = "AAMP";
#prev=[];
#a=pairs_search(result,2,{"nodes":[],"edges":[]},1,{},set());
#a=pair_search("Q13685");
#b=pair_search1("Q13685");

#a=getModel("DDX19B","MIF4GD");
#print(a);


#print(a);
#print(b);
                

