import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import numpy as np

filename="zara01_normal"
f = open("outputs/new_db_scan_clusters.txt",'w')
clusters_coexistent = open("outputs/new_clusters_coex.txt",'w')
value_existent = open("outputs/new_value_existent.txt",'w')
final_groups_with_r_value = open("outputs/new_final_groups.txt",'w')
df = pd.read_csv("dataset/"+filename+".csv")
df = pd.DataFrame(df, columns= ['agent_id','pos_x','pos_y','timestamp'])


finalMatrix={}
r_matrix = []
true_group_list = []
r = 0.5

# Checking for Co-Exisiting between groups and saving as a tuple in dictionary
def co_ex(c_df, clustering):
    for x in np.unique(clustering):
        if(x!= -1):
            listt=[]
            for index,row in c_df.iterrows():
                if(row['cluster'] == x):
                    listt.append(int(row['agent_id']))
            q = tuple(listt) 
            finalMatrix[q] = (0 if finalMatrix.get(q)==None  else finalMatrix.get(q)) + 1
            
    
# Checking for Overall Existency for each agent in all the timeframes
def overall_existence(c_df):
    existence = set([])
    for key in finalMatrix:
        for x in key:
            for index,row in c_df.iterrows():
                if(row['agent_id'] == x):
                    existence.add(row['timestamp'])
        print('Key: ',key,' Count: ',len(existence) ,file=value_existent)
        print('Key: ',key,' value: ',finalMatrix[key] ,file=value_existent)
        if(finalMatrix[key]/len(existence) >= r):
            new_list = []
            for k in key:
                new_list.append(k+1)
            r_matrix.append(new_list)
        print('Key: ',key,' r: ',(finalMatrix[key]/len(existence)) ,file=value_existent)
        existence.clear()

        
# GET INDIVIDUAL FRAME
def get_element(i):
    inputArray = np.empty((0, 2), float)
    tempValue=df.loc[df['timestamp'] == i]
    for index,row in tempValue.iterrows():   
        x = float(row["pos_x"])
        y = float(row["pos_y"])
        inputArray=np.append(inputArray, np.array([[x,y]]), axis=0)
    return inputArray

#Calculating IOU
def iou():
    file_name = "groups.txt"
    
    with open(file_name) as f:
        lines = f.readlines()
        for line in lines:
            str_list = line.split()
            num_list=[]
            for i in str_list:
                num_list.append(int(i))    
            true_group_list.append(num_list)

    pred_intersection_true = 0
    pred_union_true = len(r_matrix) + len(true_group_list)

    for true_group in true_group_list:
        if(true_group in r_matrix):
            pred_intersection_true = pred_intersection_true + 1
            pred_union_true = pred_union_true - 1

    # print(pred_intersection_true)
    # print(pred_union_true)
    iou = pred_intersection_true/pred_union_true
    print("IOU is: ", iou)
    return iou


# Main loop to get get all the frames at each timestamp
def iterate_over_frames(epsilon):    
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
        
            clustering = DBSCAN(eps=epsilon, min_samples=2).fit_predict(outputArray)
            rslt_df["cluster"] = clustering; 
            co_ex(rslt_df, clustering)
            print(rslt_df, file=f)
            print("Number of Clusters: ",len(set(clustering)),file=f)
            # if(len(set(clustering))>1):
                # print("Score: ",silhouette_score(outputArray,clustering), file=f)
        

# Run for Multiple Epsilon values to determine the best one which is 1.2
temp_epsilon=[0.7,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5,1.6]
ious=[]

def calculate_multiple_results():    
    for x in temp_epsilon:
        finalMatrix.clear()
        r_matrix.clear()
        true_group_list.clear()
        print("For Epsilon of: ",x)
        iterate_over_frames(x)
        print(finalMatrix, file=clusters_coexistent)
        overall_existence(df)
        ious.append(iou())
        print("************EPSILON*********************",x, file=final_groups_with_r_value)
        print("************Orignal Clusters*********************", file=final_groups_with_r_value)
        print(true_group_list, file=final_groups_with_r_value)

        print("************Formed Clusters*********************", file=final_groups_with_r_value)
        print(r_matrix, file=final_groups_with_r_value)



calculate_multiple_results()
plt.scatter(temp_epsilon, ious)
plt.xlabel('EPSILON')
plt.ylabel('IOU')
plt.xlim(0, 2)
plt.ylim(0, 1)
plt.show()