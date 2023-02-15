# -*- coding: utf-8 -*-
"""classificacao_binaria.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FXA0ZfXlkHlq2x2q2dXPKaEn8tdT1D0j

**Importar bibliotecas**
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
# ROC: receiver operating characteristic curve, AUC: area under the ROC curve
from sklearn.metrics import roc_auc_score

from google.colab import drive

"""**Problema:**

Os clientes estão fechando a conta em um banco, então precisamos usar os dados para saber de antemão quais estão insatisfeitos para entender e mitigar o que está acontecendo.


**Variáveis:**

*  Custormerid: identificador único do cliente
*  Surname: sobrenome do cliente
*  CreditScore: score de crédito
*  Geography: paíz de origem do cliente
*  Gender: homem (male) ou mulher (female)
*  Age: idade
*  Tenure: tempo de relacionamento do cliente com o banco
*  Balance: valor na conta corrente
*  NumOfProducts: quantidade de produtos bancários contratados pelo cliente
*  HasCrCard: tem cartão de crédito? (sim/não)
*  IsActiveMember: movimenta a conta frequentemente?
*  EstimatedSalary: renda estimada

**Variável resposta:**
*  Exited: fecha a conta nos próximos meses (sim/não)
"""

drive.mount('/content/drive')

PATH='drive/My Drive/FLAI/00_fundamentos/01_classificacao/'
df=pd.read_csv(PATH+'Churn_Modelling.csv', sep=',')
df = df.drop('RowNumber', axis='columns') # jogar fora a coluna 'RowNumber'

#Como cada cliente possui um identificador único (CostumerId), vamos utilizá-lo como índice.
df = df.set_index('CustomerId')

df

"""**Transformar as variáveis de texto em dummies**

Como trabalhar com texto é complicado, transformamos os dados em números.

Note que as variáveis antes preenchidas por texto sumiram e foram criadas variáveis únicas. Por exemplo:
*  "Surname_Zubarev": apenas quem tem Surname=Zubarev terá o valor preenchido por 1, enquanto quem não tem estará com 0;
*  "Geography_Germany": apenas quem tem Geography=Germany terá o valor preenchido por 1, enquanto quem não tem estará com 0.
"""

df_d = pd.get_dummies(df)
df_d

"""**Separar variáveis**
*  Dados do cliente (idade, gênero, localização, etc);
*  Variável para resposta que buscamos: vai fechar a conta?

**Proporção de classes:** ver a média ou quantidade de clientes que fecharão a conta.
*  Y.mean()
*  Y.value_counts()
"""

X = df_d.drop('Exited', axis='columns') # joga fora a variável resposta
Y = df_d.Exited # pega só a coluna da variável resposta

print('Média de clientes que fecharão a conta [valor entre 0 e 1]:', Y.mean()) # tira a média de quantos clientes vão fechar a conta
print('\n0: qtd de clientes que não fecharão a conta\n1: qtd de clientes que fecharão a conta\n')
print(Y.value_counts())
print('\nMédia [valor entre 0 e 1]:')
Y.value_counts()/Y.shape[0]

"""**Dividir dados e treinar modelo**
*  Conjunto de treinamento: 70% dos dados
*  Conjunto de teste: 30% dos dados

Documentação: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
"""

X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=0.3, random_state=61658)

#treinar modelo: random forest classifier
rf = RandomForestClassifier(n_estimators=500, max_depth=10, random_state=61658, n_jobs=-1)

rf.fit(X_train, Y_train)

"""**Testar modelo e mostrar resultados**"""

resultados=rf.predict_proba(X_test) # mostra a propensão de cada cliente fechar a conta

# criar dataframe
pd.DataFrame(resultados, columns=['não', 'sim'])

"""**Separar apenas o que é necessário e avaliar**

Vamos refazer o que está no trecho anterior, mas apenas com o que precisamos.

A função roc_auc_score avalia a taxa de acerto (compara resultados obtidos pelo modelo e respostas do "gabarito").
"""

pred = rf.predict_proba(X_test)[:,1] # testa o modelo e guarda em 'pred' apenas a coluna 1 (sim)

print('Taxa de acerto:', roc_auc_score(Y_test, pred))
df_pred = pd.DataFrame()
df_pred.loc[:, 'vai fechar a conta?'] = pred
df_pred

"""**Histograma**"""

plt.figure(figsize=(15,5))
plt.title('Não vai fechar a conta')
plt.hist(pred[Y_test==0], bins=np.linspace(0,0.5,50), density=True) # quem ficou no banco

plt.figure(figsize=(15,5))
plt.title('Vai fechar a conta')
plt.hist(pred[Y_test==1], bins=np.linspace(0,0.5,50), density=True); # quem fechou a conta


plt.figure(figsize=(15,5))
plt.title('Tudo no mesmo gráfico')
plt.hist(pred[Y_test==0], bins=np.linspace(0,0.5,50), density=True, color='g', alpha=0.3, label='mantém') # quem ficou no banco
plt.hist(pred[Y_test==1], bins=np.linspace(0,0.5,50), density=True, color='r', alpha=0.3, label='fecha') # quem fechou a conta
plt.legend();

"""**Refinar a aparência do gráfico e analisar**

Podemos ver quem mantém a conta (verde) e quem fecha a conta (vermelho).

Há sobreposição, então o modelo não separou tão bem os clientes.

Para resultados acima de 30%, temos certeza de que o cliente vai sair.

Acima de 25%, há bastante chance de o cliente sair.

A faixa entre 18% e 25% é um grupo misturado.

Abaixo de 18%, é bastante provável que o cliente mantenha a conta.

A partir desses resultados, o banco pode criar estratégias para manter quem quer sair.
"""

plt.figure(figsize=(15,5))
plt.title('Vai fechar a conta?')
plt.hist(pred[Y_test==0], bins=np.linspace(0,0.5,50), density=True, color='g', alpha=0.3, rwidth=0.8, label='não') # quem ficou no banco
plt.hist(pred[Y_test==1], bins=np.linspace(0,0.5,50), density=True, color='r', alpha=0.3, rwidth=0.8, label='sim') # quem fechou a conta

plt.xticks(np.arange(0,0.501,0.05), fontsize=15)
plt.yticks([])
plt.legend(fontsize=15)
plt.grid();