# %%
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import sqlalchemy

con = sqlalchemy.create_engine("sqlite:///../../data/analytics/database.db")

#%%

#SAMPLE - IMPORT DO DADOS
df = pd.read_sql('abt_fiel', con)
df.head()

#%%

# SAMPLE - OOT
df_oot = df[df['dtRef'] == df['dtRef'].max()].reset_index(drop=True)  #Base OOT
df_oot

#%%

# SAMPLE - TEST and TRAIN

target = 'flFiel'  #Nome da variável target 
features = df.columns.tolist()[3:]  #Todas as colunas, exceto as 1as 3 (ID, dtRef, target)

df_train_test = df[df['dtRef'] < df['dtRef'].max()].reset_index(drop=True)      #Base de treino e teste

y = df_train_test[target]       # Isso é um pf.Series (vetor)
X = df_train_test[features]     # Isso é um pf.DataFrame (matriz)

from sklearn import model_selection

X_train, X_test, y_train, y_test = model_selection.train_test_split(
    X, y,               # Dados
    test_size=0.2,      # 20% dos dados para teste
    random_state=42,    # Para reprodutibilidade dos resultados     
    stratify=y          # Mantém a proporção original do target nas bases de treino e teste
)

print(f'Base Treino: {y_train.shape[0]} Unid. | Tx.Target {100*y_train.mean():.2f}%' )  #Imprime qtd. de registros teste e % de target=1
print(f'Base Teste: {y_test.shape[0]} Unid. | Tx.Target {100*y_test.mean():.2f}%' )  #Imprime qtd. de registros treino e % de target=1

#%%

# EXPLORE - MISSING

s_nas = X_train.isna().mean()   #Percentual de missing por variável
# s_nas = (-X_train.isna()).sum()   #Percentual de missing por variável
s_nas = s_nas[s_nas > 0]        #Filtro: manter apenas variável com missing
s_nas

#%%

cat_features = ['descLifeCycleAtual', 'descLifeCycle_D28']  #Lista de variáveis categóricas
num_features = list(set(features) - set(cat_features))  #Lista de variáveis numéricas = features - cat_features

df_train = X_train.copy()           #Copia X_train para df_train
df_train[target] = y_train.copy()   #Adiciona a variável target em df_train

df_train[num_features] = df_train[num_features].astype(float)  #Garante que as variáveis numéricas estão no formato float

bivariada = df_train.groupby(target)[num_features].median().T  #Média das variáveis numéricas por classe do target
bivariada['ratio'] = (bivariada[1] + 0.001) / (bivariada[0] + 0.001)     #Razão entre as medianas das classes do target
bivariada.sort_values('ratio', ascending=False)                         #Ordena pela razão

to_remove = bivariada[bivariada['ratio'] == 1].index.tolist()  #Lista de variáveis para remoção (ratio = 1)

# %% EXPLICAÇÃO
### ANÁLISE BIVARIADA DAS VARIÁVEIS NUMÉRICAS

# AS FEATURES QUE TEM UM RATIO MUITO ALTO OU MUITO BAIXO SÃO AS QUE MAIS SE RELACIONAM COM O TARGET
# EXEMPLO: descLifeCycleAtual TEM RATIO 3.5, OU SEJA, A MEDIANA DO TARGET=1 É 3.5X MAIOR QUE A MEDIANA DO TARGET=0
# ISSO INDICA QUE ESSA VARIÁVEL TEM UMA RELAÇÃO FORTE COM O TARGET
# ESSA ANÁLISE SERÁ USADA PARA SELEÇÃO DE VARIÁVEIS A SEREM USADAS NO MODELO
# SE A DIFERENÇA ENTRE AS MEDIANAS FOR PEQUENA, ESSA VARIÁVEL PODE SER DESCARTADA

# QUANTO MAIOR O RATIO, MAIS RELAÇÃO COM O TARGET. QUANTO MENOR O RATIO, MENOS RELAÇÃO COM O TARGET
# LOGO, QUANTO MAIOR O RATIO MAIS PROVÁVEL DE SER TARGET=1 (FIEL)
# E QUANTO MENOR O RATIO MAIS PROVÁVEL DE SER TARGET=0 (NÃO FIEL)
# OU SEJA, RATIO MUITO ALTO OU MUITO BAIXO SÃO IMPORTANTES. RATIO PRÓXIMO DE 1 PODE SER DESCARTADO


# %%

df_train.groupby('descLifeCycleAtual')[target].mean()   #Média do target por categoria

#%%
df_train.groupby('descLifeCycle_D28')[target].mean()


#%%

# MODIFY - MISSING
# FERRAMENTA: FEATURE SELECTION

from feature_engine import selection

to_remove = bivariada[bivariada['ratio'] == 1].index.tolist()  #Lista de variáveis para remoção (ratio = 1)

drop_features = selection.DropFeatures(to_remove)  #Cria o objeto DropFeatures

# https://youtu.be/FPZxBGRkAo4

# %%
