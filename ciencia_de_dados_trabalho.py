# -*- coding: utf-8 -*-
"""Ciencia_de_Dados_Trabalho.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uwj8l40IN72AztLwu-c7GDn0NLvDOclg

A idéia deste trabalho é poder analisar um dataset que contém um conjunto de pacotes de rede que foram gerados em uma rede IoT. Esta rede utiliza o protocolo MQTT para que os dispositivos se comuniquem. A partir da análise que for feita nos resgistros desses pacotes, o objetivo principal é poder ver a possibilidade de identificar um ataque do tipo força bruta entre um dispositivo e outro.

O dataset utilizado foi extraído da base de datasets do IEEE-Dataport e o seu nome é "*MQTT Internet of Things Intrusion Detection Dataset*".

Antes de tudo, vamos montar o ponto onde vamos fazer a importação do dataset.
"""

from google.colab import drive

drive.mount('/content/drive')

import pandas as pd

dados = pd.read_csv('/content/drive/My Drive/Mestrado/mqtt_bruteforce.csv')

"""Vamos dar uma olhada nos primeiros registros para vermos como é a sua estrutura."""

dados.head(10)

"""Vamos agora saber quantas linhas e quantas colunas esse dataset possui."""

dados.shape

"""Após verificar os resultados anteiores, percebe-se que este dataset é muito extenso e que possui milhões de registros de tráfego de pacotes. Além disso, ele possui um total de 31 coluncas, ou características. 

Ao fazer análises nas características dos pacotes, percebeu-se que das 31 apenas 9 apresentam relevância para as análises.

Ao ter consciência disto, as próximas análises serão feitas em cima destas características. Primeiro vamos saber quais são os endereços IP que aparecem nos campos de "src_ip" (endereço ip de origem) e "dst_ip" (endereço ip de destino).
"""

dados['dst_ip'].unique()

"""Após encontrar os endereços ip que aparecem dos registros, foram feitos testes para saber a quantidade de vezes que cada um deles aparecem.

Após feitos os testes, percebeu-se que os endereços IP "192.168.2.5" e "192.168.1.7" são os que mais aparecem nos registros. O primeiro enreço no campo "src_ip" e o segundo endereço no campo "dst_ip".
"""

dados.query("src_ip == '192.168.2.5'")

dados.query("dst_ip == '192.168.1.7'")

"""O primeiro endereço aparece 5012000 vezes e o segundo aparece 5010276 vezes.

Ao saber disso, vamos saber o nível de relação que eles possuem.

Para isso vamos saber quantos pacotes exsitem onde o endereço IP de origem seja o "192.168.2.5" e o endreço IP de destino seja o "192.168.1.7".
"""

ip_origem = "src_ip == '192.168.2.5'"
ip_destino = "dst_ip == '192.168.1.7'"

resultado = dados.query(f"{ip_origem} and {ip_destino}")

resultado.head(10)

"""Ao saber do resultado anterior, percebe-se que a quantidade de pacotes que antendem aos quesitos definidos é de 5010276, cerca de metade da quantidade total de registro de pacotes."""

import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

enderecos_ip = pd.crosstab(dados['src_ip'], dados['dst_ip'], normalize="index")
plot_enderecos = sns.lineplot(data=enderecos_ip['192.168.2.1'])

agregado_dados = dados.groupby(['src_ip','dst_ip','protocol']).size()
agregado_dados

teste_dados = pd.crosstab([dados["src_ip"], dados['dst_ip']], dados["protocol"], normalize="index")
teste_dados

teste_dados.describe()

protocolo = teste_dados["MQTT"]
plt.figure(figsize=(9, 6))
plot_it = sns.lineplot(data=protocolo)
plot_it.set(ylim=(0,1))

"""**Primeiro vamos analisar o comportamento dos endereços IP**"""

enderecos_ip = pd.crosstab(dados['src_ip'], dados['dst_ip'], normalize="index")
plt.figure(figsize=(9, 6))
plot_enderecos = sns.lineplot(data=enderecos_ip['192.168.1.7'])
plt.xlabel("Endereço de Origem")
plt.ylabel("Pencentual")
plt.title("Relação dos endereços IPs de Origem com o endereço 192.168.1.7")

enderecos_ip = pd.crosstab(dados['src_ip'], dados['dst_ip'], normalize="index")
plt.figure(figsize=(9, 6))
plot_enderecos = sns.lineplot(data=enderecos_ip['192.168.2.5'])
plt.xlabel("Endereço de Origem")
plt.ylabel("Pencentual")
plt.title("Relação dos endereços IPs de Origem com o endereço 192.168.2.5")

"""**Após isso vamos analisar esses endereços juntamente com o protocolo MQTT**"""

teste_dados = pd.crosstab(dados["src_ip"], dados["protocol"], normalize="index")
plt.figure(figsize=(9, 6))
plot_enderecos = sns.lineplot(data=teste_dados['MQTT'])
plt.xlabel("Endereço de Origem")
plt.ylabel("Pencentual")
plt.title("Percentual de Uso do Protocolo MQTT por cada endereço IP de Origem")

teste_dados = pd.crosstab(dados["dst_ip"], dados["protocol"], normalize="index")
plt.figure(figsize=(9, 6))
plot_enderecos = sns.lineplot(data=teste_dados['MQTT'])
plt.xlabel("Endereço de Origem")
plt.ylabel("Pencentual")
plt.title("Percentual de Uso do Protocolo MQTT por cada endereço IP de Destino")

teste_dados = pd.crosstab(dados["src_ip"], dados["protocol"], normalize="index")
plt.figure(figsize=(9, 6))
plot_enderecos = sns.lineplot(data=teste_dados['TCP'])
plt.xlabel("Endereço de Origem")
plt.ylabel("Pencentual")
plt.title("Percentual de Uso do Protocolo TCP por cada endereço IP de Origem")

teste_dados = pd.crosstab(dados["dst_ip"], dados["protocol"], normalize="index")
plt.figure(figsize=(9, 6))
plot_enderecos = sns.lineplot(data=teste_dados['TCP'])
plt.xlabel("Endereço de Destino")
plt.ylabel("Pencentual")
plt.title("Percentual de Uso do Protocolo TCP por cada endereço IP de Destino")

"""**Agora vamos analisar os pacotes que utilizaram o message type 1 do protocolo MQTT**"""

teste_dados = pd.crosstab(dados["src_ip"], dados["mqtt_messagetype"], normalize="index")
plt.figure(figsize=(9, 6))
plot_enderecos = sns.lineplot(data=teste_dados['1'])
plt.xlabel("Endereço de Origem")
plt.ylabel("Pencentual")
plt.title("Porcentagem de pacotes MQTT do tipo CONNECT enviados por endereço de origem")

teste_dados = pd.crosstab(dados["dst_ip"], dados["mqtt_messagetype"], normalize="index")
plt.figure(figsize=(9, 6))
plot_enderecos = sns.lineplot(data=teste_dados['1'])
plt.xlabel("Endereço de Destino")
plt.ylabel("Pencentual")
plt.title("Porcentagem de pacotes MQTT do tipo CONNECT recebidos por endereço de destino")

teste_dados = pd.crosstab(dados["src_ip"], [dados["mqtt_flag_passwd"], dados["mqtt_flag_uname"]], normalize="index")
plt.figure(figsize=(9, 6))
plot_enderecos = sns.lineplot(data=teste_dados['1'])
plt.xlabel("Endereço de Destino")
plt.ylabel("Pencentual")
plt.title("Porcentagem de pacotes MQTT do tipo CONNECT recebidos por endereço de destino")