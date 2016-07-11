# -*- coding: utf-8 -*-
from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector
import csv
import sys
import io
import time
import sqlite3 as sql
#from grafos import caminhos as caminhos
#import grafos.hashmap as hashmap

def saida_custos_csv(custo_cenarios):
    f = open('custos_cenarios.csv', 'w')
    f.write('id_rota_origem_destino;n_rota;n_etapa;cenario;cidade_origem;cidade_destino;modal;carga;distancia;frete_peso;custo_pedagio;custo_financeiro;custo_seguro;custo_perda_carga;custo_transbordo;capacidade_do_modal;custo_total;custo_total_rota\n')

    for custo_cenario in custo_cenarios:
        custo_total_rodo = 0
        custo_total_hidro = 0
        custo_total_ferro = 0

        for etapa in custo_cenario:
            row = etapa.get_full()
            for cell in row:
                f.write(str(cell).replace(".",",")+";")
            f.write("\n")

    f.close()

def saida_relatorio_padrao(custo_cenarios):
    f = open('custos_cenarios_padrao.csv', 'w')
    f.write('id_rota_origem_destino;n_rota;n_etapa;cenario;cidade_origem;cidade_destino;modal;carga;distancia;frete_peso;custo_pedagio;custo_financeiro;custo_seguro;custo_perda_carga;custo_transbordo;capacidade_do_modal;custo_total;custo_total_rota;id_rota_origem_destino;n_rota;n_etapa;cenario;cidade_origem;cidade_destino;modal;carga;distancia;frete_peso;custo_pedagio;custo_financeiro;custo_seguro;custo_perda_carga;custo_transbordo;capacidade_do_modal;custo_total;custo_total_rota;id_rota_origem_destino;n_rota;n_etapa;cenario;cidade_origem;cidade_destino;modal;carga;distancia;frete_peso;custo_pedagio;custo_financeiro;custo_seguro;custo_perda_carga;custo_transbordo;capacidade_do_modal;custo_total;custo_total_rota;\n')
    for custo_cenario in custo_cenarios:
        for etapa in custo_cenario:
            row = etapa.get_full()
            for cell in row:
                f.write(str(cell).replace(".",",")+";")
        f.write("\n")

    f.close()

def saida_menor_custo(custo_cenarios):

    return 0

def saida_custos_db(custo_cenarios,nome):
    #cria a tabela
    conn = sql.connect(nome+'.db')
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS custo_origem_destino_municipios;")
    cur.execute('''CREATE TABLE custo_origem_destino_municipios(
                         id_rota_origem_destino        MEDIUMINT
                        ,n_rota                        MEDIUMINT
                        ,n_etapa                    MEDIUMINT
                        ,cenario                    MEDIUMINT
                        ,municipio_origem            VARCHAR(100)
                        ,municipio_destino            VARCHAR(100)
                        ,modal                        VARCHAR(100)
                        ,carga                        VARCHAR(100)
                        ,distancia                    FLOAT
                        ,frete_peso                    FLOAT
                        ,custo_pedagio                FLOAT
                        ,custo_financeiro            FLOAT
                        ,custo_seguro                FLOAT
                        ,custo_perda_carga            FLOAT
                        ,custo_transbordo            FLOAT
        );''')

    # Insere valores
    for custo_cenario in custo_cenarios:
        for etapa in custo_cenario:
            row = etapa.get_full()
            cur.execute('''INSERT INTO custo_origem_destino_municipios VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''', (row[0] ,row[1] ,row[2] ,row[3] ,row[4] ,row[5] ,row[6] ,row[7] ,row[8] ,row[9] ,row[10] ,row[11] ,row[12] ,row[13] ,row[14]))

    conn.commit()
    conn.close()

def atualiza_DB_rotas(row):
    cnx = mysql.connector.connect(user='root', password='sCHW31N3R31',
                                  host='127.0.0.1',
                                  database='rodovias')



    cursor = cnx.cursor()
    add_rotas = ("INSERT INTO rodovias.origem_destino_municipios "
                   "(id_rota_origem_destino,n_rota,n_etapa,cenario,municipio_origem,municipio_destino,modal,carga,distancia,frete_peso,custo_pedagio,custo_financeiro,custo_seguro,custo_perda_carga,custo_transbordo,capacidade_do_modal) "
                   "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")

    data_rota = (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],round(row[8],4),round(row[9],4),round(row[10],4),round(row[11],4),round(row[12],4),round(row[13],4),round(row[14],4),round(row[15],4))

    cursor.execute(add_rotas, data_rota)
    # Make sure data is committed to the database
    cnx.commit()
    cursor.close()

    cnx.close()