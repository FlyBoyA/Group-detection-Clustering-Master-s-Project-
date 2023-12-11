from re import A
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


filename="zara01_normal"

df = pd.read_csv("dataset/"+filename+".csv")
df = pd.DataFrame(df, columns= ['agent_id','pos_x','pos_y','timestamp',"frame_id"])

df=df.sort_values(by=['timestamp','agent_id'])
# print(df.head(20))

for index, row in df.iterrows():
    # print (row["agent_id"], row["frame_id"])


 matrixArray=np.zeros((148, 148))


# xx=[]
# yy=[]



 totalCount = len(df.index)
 aux1_list = []
 row_labels=[]
 column_labels=[]

# print("*********************************")

def get_element(i):
    tempValue=df.loc[df['timestamp'] == i]
    for index,row in tempValue.iterrows():    
        # print (row["agent_id"], row["frame_id"])
        # print(len(tempValue.index))
        aux1_list.append(row["agent_id"])
        # print("Upper Element: ",int(row["agent_id"]))
        for idx, x in enumerate(aux1_list):
            if(x!=row["agent_id"]):
                # print("Index: ",idx)
                # print("Value: ",int(x))
                matrixArray[int(row["agent_id"])][int(x)] = (matrixArray[int(row["agent_id"])][int(x)])+1
                matrixArray[int(x)][int(row["agent_id"])] = (matrixArray[int(x)][int(row["agent_id"])])+1
        # print("-------------")
    aux1_list.clear()
    # print("*********************************")




for i in df['timestamp'].unique():
    # print("************TIMESTAMP*********************",i)
    get_element(i)


for i in df['agent_id'].unique():
    row_labels.append(int(i))
    column_labels.append(int(i))

row_labels.sort()
column_labels.sort()


# print("************ ROWS s*********************",row_labels)
# print("************ COLOUMNS s*********************",column_labels)

df = pd.DataFrame(matrixArray, columns=column_labels, index=row_labels)

# print(df)

df.to_csv('co-existance.csv')


# np.set_printoptions(threshold=np.inf)
# print(matrixArray)
  