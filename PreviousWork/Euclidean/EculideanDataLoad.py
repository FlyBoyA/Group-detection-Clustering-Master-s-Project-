from tkinter import Frame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import EuclideanDistance
from scipy.spatial import distance


filename="zara01_normal"

df = pd.read_csv("../dataset/"+filename+".csv")
df = pd.DataFrame(df, columns= ['agent_id','pos_x','pos_y','timestamp'])

df=df.sort_values(by=['timestamp','agent_id'])


totalCount = len(df.index)

FrameDistanceMatrixList = []


def get_element(i):
    tempValue=df.loc[df['timestamp'] == i]
    len = tempValue.size
    rowId=0;
    print("*"*10,"timestamp ",i,"*"*10)
    for index,row in tempValue.iterrows():
        frame = EuclideanDistance.FrameDistanceMatrix()
        new_row_id = 0
        for new_index,new_row in tempValue.iterrows():
          if(new_row_id > rowId):
            ed = EuclideanDistance.EuclideanDistance()
            ed.agentId1 = int(row['agent_id'])
            ed.agentId2 = int(new_row['agent_id'])
            point1 = (float(row['pos_x']), float(new_row['pos_x']))
            point2 = (float(row['pos_y']), float(new_row['pos_y'])) 
            ed.distance = distance.euclidean(point1,point2)
            frame.listOfDistances.append(ed)
            print(ed.agentId1,ed.agentId2,ed.distance)
          new_row_id = new_row_id + 1
        rowId=rowId+1;

for i in df['timestamp'].unique():
    get_element(i)
    


