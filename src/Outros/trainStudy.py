# %%
import pandas as pd

from sklearn import model_selection

from feature_engine import selection
from feature_engine import imputation
from feature_engine import encoding


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import sqlalchemy

con = sqlalchemy.create_engine("sqlite:///../../data/analytics/database.db")

#%%

#SAMPLE - IMPORT DO DADOS
df = pd.read_sql('SELECT * FROM abt_fiel', con)
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

cat_features = ['descLifeCycleAtual', 'descLifeCycleD28']  #Lista de variáveis categóricas
num_features = list(set(features) - set(cat_features))  #Lista de variáveis numéricas = features - cat_features

df_train = X_train.copy()           #Copia X_train para df_train
df_train[target] = y_train.copy()   #Adiciona a variável target em df_train

df_train[num_features] = df_train[num_features].astype(float)  #Garante que as variáveis numéricas estão no formato float

bivariada = df_train.groupby(target)[num_features].median().T  #Média das variáveis numéricas por classe do target
bivariada['ratio'] = (bivariada[1] + 0.001) / (bivariada[0] + 0.001)     #Razão entre as medianas das classes do target
bivariada.sort_values(by='ratio', ascending=False)                         #Ordena pela razão
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
df_train.groupby('descLifeCycleD28')[target].mean()

# %%
# MODIFY - DROP
# FERRAMENTA: FEATURE SELECTION

X_train[num_features] = X_train[num_features].astype(float)  #Garante que as variáveis numéricas estão no formato float

to_remove = bivariada[bivariada['ratio'] == 1].index.tolist()  #Lista de variáveis para remoção (ratio = 1)
drop_features = selection.DropFeatures(to_remove)   #Cria o objeto DropFeatures
#%%

# MODIFY - MISSING

fill_0 = ['python2025', 'github2025', 'sql2020']
imput_0 = imputation.ArbitraryNumberImputer(
    arbitrary_number=0, 
    variables=fill_0
            ) #Cria o objeto ArbitraryNumberImputer para preencher com 0

fill_new = ['descLifeCycleD28']
imput_new = imputation.CategoricalImputer(
    fill_value='Nao-Usuario', 
    variables=fill_new
            )  #Cria o objeto CategoricalImputer para preencher com 'Não usuario'

fill_1000 = ['qtdDiasUltiAtividade', 'avgIntervaloDiasVida', 'avgIntervaloDiasD28']
imput_1000 = imputation.ArbitraryNumberImputer(
    arbitrary_number=1000, 
    variables=fill_1000
            ) #Cria o objeto ArbitraryNumberImputer para preencher com 1000

# MODIFY - ONEHOT

onehot = encoding.OneHotEncoder(variables=cat_features)  #Cria o objeto OneHotEncoder

# MODIFY - APLICA TRANSFORMAÇÕES NO DATASET

X_train_transform = drop_features.fit_transform(X_train)
X_train_transform = imput_0.fit_transform(X_train_transform)
X_train_transform = imput_new.fit_transform(X_train_transform)
X_train_transform = imput_1000.fit_transform(X_train_transform)
X_train_transform = onehot.fit_transform(X_train_transform)         #Aplica o OneHot

#%%

## Caso esteja usando muitas categorias, pode ser interessante, em vez de usar o OneHotEncoder padrão, usar o MeanEncoder.
## Isso porque o OneHotEncoder pode criar muitas variáveis, o que pode levar a problemas de dimensionalidade.
## O MeanEncoder cria uma variável numérica para cada categoria, representando a média do target. Por exemplo:
## meanEnconder = encoding.MeanEncoder(variables=[descLifeCycleAtual, descLifeCycleD28], target=target)
## Retornando uma estrutura de colunas como: descLifeCycleAtual_mean, descLifeCycleD28_mean

## ⚠️ Estudar mais essa forma "mean encoding"

#%%

X_train_transform.head()
# %%

# MODEL

from sklearn import tree
from sklearn import ensemble

# %%

# MODEL - DECISION TREE
model = tree.DecisionTreeClassifier(random_state=42, min_samples_leaf=10)        #Cria o modelo DecisionTreeClassifier com o min_samples_leaf que evita overfitting. Ou seja, cada folha terá no mínimo 10 amostras.
model.fit(X_train_transform, y_train)   #Treina o modelo

#%%

# MODEL - FOREST RANDOMICO 
model = ensemble.RandomForestClassifier(random_state=42, 
                                        n_estimators=150,
                                        n_jobs=-1,
                                        min_samples_leaf=60)
model.fit(X_train_transform, y_train)   #Treina o modelo

#%% 

# MODEL - ADA BOOST
model = ensemble.AdaBoostClassifier(random_state=42, 
                                    n_estimators=150, 
                                    learning_rate=0.1)
model.fit(X_train_transform, y_train)   #Treina o modelo

# %%

# ASSESS
from sklearn import metrics

y_pred_train = model.predict(X_train_transform)             #Faz a predição na base de treino
y_proba_train = model.predict_proba(X_train_transform)      #Faz a predição de probabilidade na base de treino

acc_train = metrics.accuracy_score(y_train, y_pred_train)       #Calcula a acurácia na base de treino
auc_train = metrics.roc_auc_score(y_train, y_proba_train[:,1])  #Calcula a AUC na base de treino

print(f'Acurácia Treino: {acc_train:.2f}')
print(f'AUC Treino: {auc_train:.2f}')

# %%

X_test_transform = drop_features.transform(X_test)           
X_test_transform = imput_0.transform(X_test_transform)        
X_test_transform = imput_new.transform(X_test_transform)      
X_test_transform = imput_1000.transform(X_test_transform)     
X_test_transform = onehot.transform(X_test_transform)         

y_pred_test = model.predict(X_test_transform)            #Faz a predição na base de treino
y_proba_test = model.predict_proba(X_test_transform)  #Faz a predição de probabilidade na base de treino

acc_test = metrics.accuracy_score(y_test, y_pred_test)   #Calcula a acurácia na base de treino
auc_test = metrics.roc_auc_score(y_test, y_proba_test[:,1])   #Calcula a AUC na base de treino


print(f'Acurácia Teste: {acc_test}')
print(f'AUC Teste: {auc_test}')

## Acurácia vs AUC
## Acurácia é a proporção de previsões corretas (tanto positivas quanto negativas) em relação ao total de previsões feitas.
## AUC (Área sob a Curva ROC) mede a capacidade do modelo de distinguir entre classes positivas e negativas, independentemente do limiar de decisão.
## Enquanto a acurácia pode ser influenciada pelo desequilíbrio das classes, a AUC fornece uma visão mais robusta do desempenho do modelo em diferentes limiares de classificação.
## Logo, em cenários com classes desbalanceadas, a AUC é frequentemente considerada uma métrica mais confiável do que a acurácia.
## Acurácia, em resumo, avalia a precisão geral do modelo, enquanto a AUC avalia sua capacidade discriminativa.
## Em liguagem simples, acurácia responde "Quantas vezes o modelo acertou?" e AUC responde "Quão bem o modelo separa as classes?".

#%%

y_pred_fodase = pd.Series([0]*y_test.shape[0])            #Faz a predição na base de treino
y_proba_fodase = pd.Series([y_train.mean()]*y_test.shape[0])       #Faz a predição de probabilidade na base de treino de acordo com a taxa de target=1 na base de treino

acc_fodase = metrics.accuracy_score(y_test, y_pred_fodase)   #Calcula a acurácia na base de treino
auc_fodase = metrics.roc_auc_score(y_test, y_proba_fodase)   #Calcula a AUC na base de treino

print(f'Acurácia Fodase: {acc_fodase}')
print(f'AUC Fodase: {auc_fodase}')

#%%
y_proba_fodase = pd.Series([y_train.mean()]*y_test.shape[0]) 
y_proba_fodase

#%%
## O que aconteceu?
## Na base de treino, o meu resultado de acurária e curva rock é 1.0, ou seja, perfeito.
## Na "prova dos nove", o resultado de acurária e curva rock diferenciam, mostrando que talvez a acurácia não seja a melhor métrica para avaliar o modelo.
## Quando jogamos todo mundo na mesma probabilidade (Modelo Fodasse) como se não fosse fiel (target=0), a acurácia é alta (porque a maioria não é fiel).
## Mas a AUC é baixa (porque o modelo não consegue distinguir entre fiéis e não fiéis).
## 0.5 para a auc é o valor de um modelo aleatório. Um modelo que não consegue distinguir entre as classes. Ou seja, o modelo fodasse não tem capacidade preditiva nenhuma.
# %%
features_names = X_train_transform.columns.tolist()

feature_importance = pd.Series(model.feature_importances_, index=features_names)
feature_importance.sort_values(ascending=False)

#%%
## FEATURE IMPORTANCE, O QUE É ISSO?
## FEATURE IMPORTANCE É UMA MÉTRICA QUE INDICA A IMPORTÂNCIA DE CADA VARIÁVEL (FEATURE) NO MODELO.
## ESSA IMPORTÂNCIA É CALCULADA COM BASE NA CONTRIBUIÇÃO DE CADA VARIÁVEL PARA A MELHORIA DO MODELO DURANTE O TREINAMENTO.
## NO CASO DE MODELOS DE ÁRVORES DE DECISÃO (COMO DECISION TREE, RANDOM FOREST, ETC.), A IMPORTÂNCIA DAS FEATURES É DETERMINADA PELA REDUÇÃO DO CRITÉRIO DE DIVISÃO (COMO GINI OU ENTROPIA) QUE CADA FEATURE PROPORCIONA AO SER UTILIZADA PARA DIVIDIR OS NÓS DA ÁRVORE.
## EM OUTRAS PALAVRAS, UMA FEATURE É CONSIDERADA IMPORTANTE SE ELA AJUDA A MELHORAR SIGNIFICATIVAMENTE A CAPACIDADE DO MODELO DE FAZER PREVISÕES PRECISAS.
## GINI É: UMA MÉTRICA USADA PARA AVALIAR A PUREZA DE UM NÓ EM UMA ÁRVORE DE DECISÃO. OU SEJA, QUANTO MAIS PURO FOR O NÓ (MAIOR CONCENTRAÇÃO DE UMA ÚNICA CLASSE), MENOR SERÁ O VALOR DE GINI.
## ENTROPIA: UMA MEDIDA DA INCERTEZA OU IMPUREZA ASSOCIADA A UM CONJUNTO DE DADOS. OU SEJA, QUANTO MAIS MISTURADAS ESTIVEREM AS CLASSES EM UM NÓ, MAIOR SERÁ A ENTROPIA.

# %%

# PREDICT OOT
X_oot = df_oot[features]   #Base OOT sem a variável target
y_oot = df_oot[target]     #Variável target da base OOT

X_oot_transform = drop_features.transform(X_oot)           
X_oot_transform = imput_0.transform(X_oot_transform)        
X_oot_transform = imput_new.transform(X_oot_transform)      
X_oot_transform = imput_1000.transform(X_oot_transform)     
X_oot_transform = onehot.transform(X_oot_transform)         

y_pred_oot = model.predict(X_oot_transform)            #Faz a predição na base de treino
y_proba_oot = model.predict_proba(X_oot_transform)  #Faz a predição de probabilidade na base de treino

acc_oot = metrics.accuracy_score(y_oot, y_pred_oot)   #Calcula a acurácia na base de treino
auc_oot = metrics.roc_auc_score(y_oot, y_proba_oot[:,1])   #Calcula a AUC na base de treino

print(f'Acurácia OOT: {acc_oot}')
print(f'AUC OOT: {auc_oot}')
