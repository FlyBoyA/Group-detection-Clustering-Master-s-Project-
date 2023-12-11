import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors
import numpy as np

filename="zara01_normal"

df = pd.read_csv("../dataset/"+filename+".csv")
df = pd.DataFrame(df, columns= ['agent_id','pos_x','pos_y','timestamp'])


f = open("db_scan_clusters.txt",'w')


# FOR INDIVIDUAL FRAMES

def get_element(i):
    inputArray = np.empty((0, 2), float)
    tempValue=df.loc[df['timestamp'] == i]
    for index,row in tempValue.iterrows():   
        x = float(row["pos_x"])
        y = float(row["pos_y"])
        inputArray=np.append(inputArray, np.array([[x,y]]), axis=0)
    return inputArray
    

for i in df['timestamp'].unique():
    # if(i == 1.2):

        options = [i] 
        rslt_df = df[df['timestamp'].isin(options)]
        rslt_df = rslt_df.sort_values(['timestamp', 'agent_id'],
              ascending = [True, True])

        outputArray=get_element(i)
        # plt.scatter(outputArray[:,0], outputArray[:,1])
        print("************TIMESTAMP*********************",i, file=f)
        # print(outputArray, file=f)
        print("************Clusters*********************", file=f)

        # Check For Nearest Neighbors and distance between them for Optimal value of Epsilon
        # allNeighbors = NearestNeighbors(n_neighbors=2)
        # neighbors = allNeighbors.fit(outputArray)
        # distances, indices = neighbors.kneighbors(outputArray) 
        # distances=np.sort(distances,axis=0)
        # distances=distances[:,1]
        # print(distances)
        # print(indices)
        # plt.plot(distances)
    
        clustering = DBSCAN(eps=0.7, min_samples=2).fit_predict(outputArray)
        # print(outputArray,clustering)
        # print(clustering, file=f)
        
        rslt_df["cluster"] = clustering; 
        print(rslt_df, file=f)

        print("Number of Clusters: ",len(set(clustering)),file=f)
        if(len(set(clustering))>1):
            print("Score: ",silhouette_score(outputArray,clustering), file=f)
            # print("Score: ",silhouette_score(outputArray,clustering))
        # plt.show()


# # FOR OVERALL FRAMES
# def get_All_Elements():
#     inputArray = np.empty((0, 2), float)
#     for index,row in df.iterrows():   
#         # print(row["pos_x"],row["pos_y"],file=f)
#         x = float(row["pos_x"])
#         y = float(row["pos_y"])
#         inputArray=np.append(inputArray, np.array([[x,y]]), axis=0)
#     return inputArray
    

# outputArray=get_All_Elements()
# print(outputArray.tolist(), file=f)
# clustering = DBSCAN(eps=0.1, min_samples=2).fit_predict(outputArray)
# print(clustering.tolist(), file=f)
        