from re import T
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors
import numpy as np

filename="zara01_normal"
f = open("db_scan_clusters.txt",'w')
clustered_agents = open("clustered_agents.txt",'w')

df = pd.read_csv("../dataset/"+filename+".csv")
df = pd.DataFrame(df, columns= ['agent_id','pos_x','pos_y','timestamp'])


matrixArray=np.zeros((148, 148), int)
np.set_printoptions(precision=0)

row_labels=[]
column_labels=[]
aux1_list = []

def get_labels_for_matrix():
    for i in df['agent_id'].unique():
        row_labels.append(int(i))
        column_labels.append(int(i))
    row_labels.sort()
    column_labels.sort()

# GET INDIVIDUAL FRAME
def get_element(i):
    inputArray = np.empty((0, 2), float)
    tempValue=df.loc[df['timestamp'] == i]
    for index,row in tempValue.iterrows():   
        x = float(row["pos_x"])
        y = float(row["pos_y"])
        inputArray=np.append(inputArray, np.array([[x,y]]), axis=0)
    return inputArray
    
def co_ex(c_df):
    for index,row in c_df.iterrows():  
        # print("Agent: ",int(row["agent_id"]))
        # print("Cluster: ",int(row["cluster"]))
        for idx, x in c_df.iterrows():
            if(x["agent_id"]!=row["agent_id"] and  x["cluster"]==row["cluster"] and row["cluster"]!=-1):
                # print("Agent 1: ",int(row["agent_id"]))
                # print("Cluster: ",int(row["cluster"]))
                # print("************")
                # print("Agent 2: ",int(x["agent_id"]))
                # print("Cluster: ",int(x["cluster"]))
                matrixArray[int(row["agent_id"])][int(x["agent_id"])] = (matrixArray[int(row["agent_id"])][int(x["agent_id"])])+1
        # print("-------------")

def print_clustered_agents(matrixArray):
    rows = matrixArray.shape[0]
    columns = matrixArray.shape[1]
    groups_count=0
    for x in range(0, rows):
        grouped_agents=[]
        check_for_groups=False
        for y in range(0, columns):
            if(matrixArray[x,y]!=0 and matrixArray[x,y]>1):
                if(x+1 not in grouped_agents):
                    grouped_agents.append(x+1)
                grouped_agents.append(y+1)
                # print("Co-Ex of: ", x+1,y+1," is: " ,matrixArray[x,y], file=clustered_agents)
                matrixArray[y,x] = 0
                check_for_groups=True

        for z in grouped_agents:
            if(z-1 != x):
                for p in grouped_agents:
                    matrixArray[z-1,p-1] = 0


        if(check_for_groups == True):
            groups_count = groups_count +1
            print("Agents: ",grouped_agents,file=clustered_agents)            
            print("-------------",file=clustered_agents)

    print("------------***************-------------",file=clustered_agents)
    print("Total Groups: ",groups_count, file=clustered_agents)

get_labels_for_matrix()

for i in df['timestamp'].unique():

        #Creating a resultant data frame to allign it with DB-Scan created clusters
        options = [i] 
        rslt_df = df[df['timestamp'].isin(options)]
        rslt_df = rslt_df.sort_values(['timestamp', 'agent_id'],
              ascending = [True, True])

        outputArray=get_element(i)
        
        print("************TIMESTAMP*********************",i, file=f)
        # print(outputArray, file=f)
        print("************Clusters*********************", file=f)
        
        clustering = DBSCAN(eps=0.78, min_samples=2).fit_predict(outputArray)
        
        rslt_df["cluster"] = clustering; 

        co_ex(rslt_df)

        print(rslt_df, file=f)

        print("Number of Clusters: ",len(set(clustering)),file=f)
        if(len(set(clustering))>1):
            print("Score: ",silhouette_score(outputArray,clustering), file=f)
        

new_matrix_df = pd.DataFrame(matrixArray, columns=column_labels, index=row_labels)
new_matrix_df.to_csv('co-existance-with-clustering.csv')

print_clustered_agents(matrixArray)