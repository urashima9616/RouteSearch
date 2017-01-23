#!/usr/bin/env python
import sys,os
import Queue
import heapq

#Expanding function----done
def Expand(Connct_link,seed):
    seeds=Connct_link[seed]
    return seeds

#Goal test----done
def Goal_test(Connct_link,SRC_id, DST_id, ALG, seeds, S):
    if ALG=='BFS' or ALG=='DFS':
        for item in seeds :
            if(item[0]==-1) :
                continue
            elif item[0]==DST_id :
                return 1
    elif ALG=='UCS' or ALG=='A*':
        if S[DST_id]==1:
            return 1
        else:
            return 0

    return 0

#Queuing for BFS ----- done
def Queuing_Fn_BFS(seeds,working_que,Expanded_set, Generated_set,parent_list,seed):
    ##print "seeds of %d\n" % seed
    ##print seeds,"\n"
    for item in seeds:
        if item[0]==-1:
            continue
        elif Generated_set[item[0]]==1 or Expanded_set[item[0]]==1 :
            continue
        else:
            working_que.put(item[0:1])
            Generated_set[item[0]] = 1
            parent_list[item[0]] = seed
    return working_que, Generated_set, parent_list

#Queuing for DFS ----- done
def Queuing_Fn_DFS(seeds,working_que,Expanded_set, Generated_set,parent_list,seed):
    ##print "seeds of %d\n" % seed
    ##print seeds,"\n"
    seeds_rev=seeds[::-1]
    for item in seeds_rev:
        if item[0]==-1:
            continue
        elif Generated_set[item[0]]==1 or Expanded_set[item[0]]==1 :
            continue
        else:
            working_que.put(item[0:1])
            Generated_set[item[0]] = 1
            parent_list[item[0]] = seed
    return working_que, Generated_set, parent_list

#Queuing for UCS ----- done
def Queuing_Fn_UCS(seeds,working_que,Expanded_set,seed):
    ##print "seeds of, ",  seed, "\n"
    ##print seeds,"\n"
    #seeds_rev=seeds[::-1]
    for item in seeds:
        if item[0]==-1:
            continue
        #Skip expanded node
        elif Expanded_set[item[0]]==1 :
            continue
        else:
            updated_pathcost=item[1]+seed[0]
            second_priority=item[2]
            node_id=item[0]
            node_parent=seed[2]
            working_que.put([updated_pathcost,second_priority,node_id,node_parent])
    return working_que

def Queuing_Fn_Astar(seeds,working_que,Expanded_set,seed,Sun_cost):
    ##print "seeds of, ",  seed, "\n"
    ##print seeds,"\n"
    #seeds_rev=seeds[::-1]
    for item in seeds:
        if item[0]==-1:
            continue
        #Skip expanded node
        elif Expanded_set[item[0]]==1 :
            continue
        else:
            updated_pathcost=item[1]+seed[4]
            updated_f_cost=Sun_cost[item[0]]+updated_pathcost
            if(updated_f_cost<seed[0]):
                updated_f_cost=seed[0]
            second_priority=item[2]
            node_id=item[0]
            node_parent=seed[2]
            working_que.put([updated_f_cost,second_priority,node_id,node_parent,updated_pathcost])
    return working_que






#Global search function
def General_Search(Connct_link,SRC_id, DST_id, ALG, num_nodes_sun):
#Initialize the working queue
    #print "Initialize working queue based on %s\n" %(ALG)
    if ALG=='BFS':
        working_que=Queue.Queue(num_nodes_sun)
        working_que.put([SRC_id,0])
    elif ALG=='DFS':
        working_que = Queue.LifoQueue(num_nodes_sun)
        working_que.put([SRC_id, 0])
    elif ALG=='A*' :
        working_que = Queue.PriorityQueue(num_nodes_sun)
        working_que.put([0,0,SRC_id,0,0])
    elif ALG=='UCS' :
        working_que = Queue.PriorityQueue(num_nodes_sun)
        working_que.put([0,0,SRC_id,0])
    else :
        working_que = Queue.Queue(num_nodes_sun)
        working_que.put([SRC_id, 0,0])

    Expanded_set=[-1 for x in range(num_nodes_sun)]
    Generated_set=[-1 for x in range(num_nodes_sun)]
    parent_list=[-1 for x in range(num_nodes_sun)]
    parent_list[SRC_id]=0;
    path_list=[]
    #print "Initialization finished\n"


    while(1):
        if working_que.empty():
            return 0
        seed=working_que.get()
        if ALG=='UCS' or ALG=='A*':
            while(Expanded_set[seed[2]]==1 and not working_que.empty() ):
                seed=seed=working_que.get()
            Expanded_set[seed[2]] = 1
        else:
            Expanded_set[seed[0]]=1


        if ALG=='UCS' or ALG=='A*':
            parent_list[seed[2]]=seed[3]
            seeds = Expand(Connct_link, seed[2])
        else:
            seeds=Expand(Connct_link,seed[0])
        Eureka=Goal_test(Connct_link,SRC_id, DST_id, ALG, seeds, Expanded_set)
        if Eureka :
            if ALG=='UCS' or ALG=='A*':
                tracker = parent_list[seed[2]]
                path_list.append(seed[2])
                path_list.append(tracker)
            else:
                tracker=parent_list[seed[0]]
                path_list.append(DST_id)
                path_list.append(seed[0])
                path_list.append(tracker)

            while(tracker!=0):
                tracker=parent_list[tracker]
                path_list.append(tracker)
            #path_list.append(SRC_id)
            return path_list
        elif ALG=='BFS':
            working_que, Generated_set, parent_list=Queuing_Fn_BFS(seeds, working_que, Generated_set,Expanded_set,parent_list, seed[0])
        elif ALG=='DFS':
            working_que, Generated_set, parent_list = Queuing_Fn_DFS(seeds, working_que, Generated_set, Expanded_set,parent_list, seed[0])
        elif ALG=='UCS':
            working_que=Queuing_Fn_UCS(seeds,working_que,Expanded_set,seed)
        elif ALG=='A*':
            working_que = Queuing_Fn_Astar(seeds, working_que, Expanded_set, seed,Sun_cost)
    return 0


#===============Main body===================================
FILE_NAME='input.txt'
#print 'hello world'
try:
    fp=open(FILE_NAME,'r')

except IOError, e:
    print "File can not be open\n", e
#----------------Input file parsing-------------------------
line_ID= 1
node_map= 0
NAME_2_ID= {}
ID_2_NAME={}
check_pt= 0
num_nodes_sun = 0
num_edges_live = 0
#First round to get scale of the graph
for eachline in fp :
    eachline = eachline.strip('\n')
    if line_ID== 1 :
        ALG=eachline
    elif line_ID== 2 :
        SRC=eachline
        NAME_2_ID[SRC] = node_map
        ID_2_NAME[node_map]=SRC
        node_map += 1
    elif line_ID== 3 :
        DST=eachline
        NAME_2_ID[DST] = node_map
        ID_2_NAME[node_map] =DST
        node_map += 1
    elif line_ID== 4 :
        num_edges_live = int(eachline)
        check_pt = num_edges_live+line_ID+1
    elif line_ID== check_pt :
        num_nodes_sun = int(eachline)
        end_pt = line_ID+num_nodes_sun
    elif (line_ID>4 and line_ID <check_pt) :
        eachline = eachline.split()
        if not NAME_2_ID.has_key(eachline[0]):
            NAME_2_ID[eachline[0]] = node_map
            ID_2_NAME[node_map] = eachline[0]
            node_map += 1

        if not NAME_2_ID.has_key(eachline[1]):
            NAME_2_ID[eachline[1]] = node_map
            ID_2_NAME[node_map] = eachline[1]
            node_map += 1
        pass
    line_ID += 1
#print "%d nodes considered\n" %num_nodes_sun
fp.seek(0)
num_nodes_sun=len(NAME_2_ID.keys())
#print "WE HAVE THIS MANY NODES ! %d\n" %num_nodes_sun

Adj_matrix = [[[0,0] for x in range(num_nodes_sun)] for y in range(num_nodes_sun)]
Sun_cost = [ -1 for x in range(num_nodes_sun)]
Connct_link=[[[-1,-1,-1,-1]] for x in range(num_nodes_sun)]
##print "Test for appending list\n"
##print Connct_link[1][1],"\n"

#Second round to create static adjacency matrix
line_ID=1
#print check_pt,"\n"
#print end_pt, "\n"

for eachline in fp :
    ##print line_ID,": ", eachline
    eachline = eachline.strip('\n')
    test = eachline.split()
    if (line_ID>4 and line_ID <check_pt) :
        eachline = eachline.split()
        #print eachline[0],"\n"
        #print eachline[1],"\n"

        #if not NAME_2_ID.has_key(eachline[0]):
        #    NAME_2_ID[eachline[0]]= node_map
        #    ID_2_NAME[node_map] = eachline[0]
        #    node_map += 1

        #if not NAME_2_ID.has_key(eachline[1]):
        #    NAME_2_ID[eachline[1]] = node_map
        #    ID_2_NAME[node_map] = eachline[1]
        #    node_map += 1

        n1 = NAME_2_ID[eachline[0]]
        n2 = NAME_2_ID[eachline[1]]
        Connct_link[n1].append([n2,int(eachline[2]),line_ID])
        Adj_matrix[n1][n2][0] = int(eachline[2])
        Adj_matrix[n1][n2][1] = line_ID
    elif (line_ID>check_pt) :
        eachline = eachline.split()
        n1 = NAME_2_ID[eachline[0]]
        Sun_cost[n1]= int(eachline[1])
    line_ID += 1

#print "Output the Adjacency matrix\n"
#for eachline in Connct_link:
    #print eachline,"\n"
#    for eachrow in range(0,num_nodes_sun):
#        #print Adj_matrix[eachline][eachrow],"\n"

##print "Sun_cost_array\n"
##print Sun_cost

fp.close()

#----------------Search Algorithm-------------------------
SRC_id = NAME_2_ID[SRC]
DST_id = NAME_2_ID[DST]
#print "Search for path between SRC: %s and DST: %s \n" %(SRC,DST)
#print "Try Algorithm %s\n" %ALG
path_list= General_Search(Connct_link,SRC_id, DST_id, ALG, num_nodes_sun)
cost =0
try:
    fp=open("output.txt",'w')

except IOError, e:
    print "File can not be open\n", e


print ALG,"\n"

if ALG=='UCS' or ALG=='A*':
    parent_node=SRC_id;
    for iter in range(len(path_list)):
        child_node=path_list.pop()
        cost += Adj_matrix[parent_node][child_node][0]
        parent_node=child_node;
        #print '%s %d\n' %(ID_2_NAME[child_node],cost)
        fp.write('%s %d\n' %(ID_2_NAME[child_node],cost))
else:
    cost=0
    for iter in range(len(path_list)):
        child_node = path_list.pop()
        #print '%s %d\n' % (ID_2_NAME[child_node], cost)
        fp.write('%s %d\n' % (ID_2_NAME[child_node], cost))
        cost += 1






