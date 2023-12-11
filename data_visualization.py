import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


filename="zara01_normal"

df = pd.read_csv("dataset/"+filename+".csv")
df = pd.DataFrame(df, columns= ['agent_id','pos_x','pos_y','timestamp'])

df=df.sort_values(by=['timestamp','agent_id'])
# print(df.head(20))

# for index, row in df.iterrows():
#     print (row["pos_x"], row["pos_y"], row["timestamp"])

xx=[]
yy=[]

fig, ax = plt.subplots()
ax.set_xlim([-20,30])
ax.set_ylim([-20,30])
scatter = ax.scatter(xx,yy,color='teal')
plt.xlabel('x - axis')
plt.ylabel('y - axis')

totalCount = len(df.index)
aux1_list = []

def get_element(i):
    tempValue=df.loc[df['timestamp'] == i]
    rowId=0;
    for index,row in tempValue.iterrows():
        xx.append(float(row['pos_x']))
        yy.append(float(row['pos_y']))
        # print(int(row['agent_id']),rowId,xx[rowId],yy[rowId])
        aux1 = ax.annotate(int(row['agent_id']), (xx[rowId], yy[rowId]), color = "purple", fontsize = 10)
        aux1_list.append(aux1)
        rowId=rowId+1;

def clear_plot():
  xx.clear()
  yy.clear()
  for ann in aux1_list:
    ann.remove()
  aux1_list.clear()

plt.draw()
for i in df['timestamp'].unique():
    get_element(i)
    plt.title('Timestamp: '+str(i))
    scatter.set_offsets(np.c_[xx,yy])
    fig.canvas.draw_idle()
    plt.pause(0.1)
    clear_plot()

plt.waitforbuttonpress()
