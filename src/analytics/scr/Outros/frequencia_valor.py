#%%
import pandas as pd
import sqlalchemy

import matplotlib.pyplot as plt

#%%

engine = sqlalchemy.create_engine('sqlite:///../../data/loyalty-system/database.db')


#%%

def import_query(path):
    with open(path) as open_file:
        return open_file.read()
    
query = import_query('frequencia_valor.sql')
# print(query)

#%%

df = pd.read_sql(query, engine)
df.head()

#>>1. Retirar da base o outlier.
df = df[df['qtdePontosPos'] < 4000]
# df.head()

#%%
plt.plot(df['qtdeFrequencia'], df['qtdePontosPos'], 'o')
plt.grid(True)
plt.xlabel('Frequencia')
plt.ylabel('valor')
plt.show()

#%%

## Definindo cluster de dados via machine learn
from sklearn import cluster

from sklearn import preprocessing

#Normalizando o dataset
minMax = preprocessing.MinMaxScaler()
X = minMax.fit_transform(df[['qtdeFrequencia', 'qtdePontosPos']])

#%%
kmean = cluster.KMeans(n_clusters=5, 
                       random_state=42, 
                       max_iter=1000)
kmean.fit(X)

df['cluster_calc'] = kmean.labels_


df.groupby(by='cluster_calc')['idCliente'].count()

# %%
# import seaborn as sns
# kmean = cluster.KMeans(n_clusters=7, 
#                        random_state=42, 
#                        max_iter=1000)
# kmean.fit(X)

# df['cluster_calc'] = kmean.labels_

# sns.scatterplot(data=df, 
#                 x="qtdeFrequencia", 
#                 y="qtdePontosPos", 
#                 hue="cluster_calc", 
#                 palette="deep")
#%%

#Ao plotar, não devemos usar os dados que estão normalizados para que eu possa interpretar
import seaborn as sns
sns.scatterplot(data=df, 
                x="qtdeFrequencia", 
                y="qtdePontosPos", 
                hue="cluster_calc", 
                palette="deep")

plt.hlines(y=1500, xmin=0, xmax=25, colors='black')
plt.hlines(y=750, xmin=0, xmax=25, colors='black')

plt.vlines(x=4, ymin=0, ymax=750, colors='black')
plt.vlines(x=10, ymin=0, ymax=3000, colors='black')

plt.grid()

#%%

# ##Explicando a normalização, destribuição dos dados e valores
# df_X = pd.DataFrame(X, columns=['normFreq', 'normValor'])
# df_X['cluster'] = kmean.labels_

# sns.scatterplot(data=df_X, 
#                 x="normFreq", 
#                 y="normValor", 
#                 hue="cluster", 
#                 palette="deep")

# # plt.hlines(y=1500, xmin=0, xmax=25, colors='black')

# plt.grid()
# %%
sns.scatterplot(data=df, 
                x="qtdeFrequencia", 
                y="qtdePontosPos", 
                hue="cluster", 
                palette="deep")

# %%
