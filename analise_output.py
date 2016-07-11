import sqlite3 as sql
import pandas as pd

# Base de dados e resultado da simulacao - Roteirizador_v5
conn = sql.connect('20160705_Roteirizacao.db')

# Cria base para pvt resultante do modelo de roteirizacao
#--------------------------------------------------------
#table = conn.execute('''SELECT * FROM custo_origem_destino_municipios;''')
qt_row_table = conn.execute('''SELECT count(*) FROM custo_origem_destino_municipios;''')

# Cria dataframe no pandas
cod_municipios = conn.execute('''SELECT * FROM custo_origem_destino_municipios;''')
cols = ['id_rota_origem_destino', 'n_rota', 'n_etapa', 'cenario', 'cidade_origem', 'cidade_destino', 'modal', 'carga', 'distancia', 'frete_peso', 'custo_pedagio', 'custo_financeiro', 'custo_seguro', 'custo_perda_carga', 'custo_transbordo']
custo_rotas = pd.DataFrame.from_records(data = cod_municipios.fetchall(), columns = cols)

# Cria nova coluna contendo o custo total da etapa
custo_rotas['custo_total'] = custo_rotas.frete_peso + custo_rotas.custo_financeiro + custo_rotas.custo_pedagio + custo_rotas.custo_perda_carga + custo_rotas.custo_seguro + custo_rotas.custo_transbordo
#print custo_rotas[custo_rotas['id_rota_origem_destino']==35670]

# Cria tabela de custo por rotas
id_custos = custo_rotas.groupby(['id_rota_origem_destino'])['custo_total'].sum().reset_index()
#print id_custos[:5]
#Cria tabela contendo etapas 1, 2 e 3 de cada rota
id_etapa_1 = custo_rotas[custo_rotas['n_etapa']==1]
id_etapa_2 = custo_rotas[custo_rotas['n_etapa']==2]
id_etapa_3 = custo_rotas[custo_rotas['n_etapa']==3]

#Escolhe as colunas de interesse
id_etapa_1 = id_etapa_1.loc[:,['id_rota_origem_destino','cenario','n_etapa','cidade_origem','cidade_destino','modal']]
id_etapa_2 = id_etapa_2.loc[:,['id_rota_origem_destino','cenario','n_etapa','cidade_origem','cidade_destino','modal']]
id_etapa_3 = id_etapa_3.loc[:,['id_rota_origem_destino','cenario','n_etapa','cidade_origem','cidade_destino','modal']]

# Unifica as tabelas
result_0_1 = pd.merge(id_custos, id_etapa_1, on='id_rota_origem_destino', how='left')
result_0_1_2 = pd.merge(result_0_1, id_etapa_2, on='id_rota_origem_destino', how='left')
result_0_1_2_3 = pd.merge(result_0_1_2, id_etapa_3, on='id_rota_origem_destino', how='left')

# Salva saida para pvt - fase II da simulacao
result_0_1_2_3.to_csv('pvt_custo_origem.csv')

