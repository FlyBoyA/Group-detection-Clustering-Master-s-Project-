import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

filename="zara01_normal"

df = pd.read_csv("../dataset/"+filename+".csv")
df = pd.DataFrame(df, columns= ['agent_id','pos_x','pos_y','timestamp'])


def create_clusters(df):
    kmeans = KMeans(n_clusters=5, init='k-means++',max_iter=5000, n_init=10, random_state=0)
    model = kmeans.fit(df)
    predicted_values = kmeans.predict(df)
    # print(predicted_values)
    plt.scatter(df['pos_x'], df['pos_y'], c=predicted_values, s=30, cmap='viridis')
    plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=200, c='black', alpha=0.5)



for i in df['timestamp'].unique():
    if(i == 0.4):
        print("**************")
        tempValue=df.loc[df['timestamp'] == i]
        create_clusters(tempValue)

        

plt.show()