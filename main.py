# -*- coding: utf-8 -*-
import in_out
import time
import custos.calculadora_custos as Calc
import grafos.caminhos as caminhos
import grafos.hashmap as hashmap
import sys
import pandas as pd

'''Declara endereco e documentos a serem abertos'''
address_hidro = 'C:\\Users\\mauricio.longato\\workspace\\Roteirizador_v5\\src\\arquivos_entrada\\conexao_custos_hidro_db_v1.csv'
address_rodo = 'C:\\Users\\mauricio.longato\\workspace\\Roteirizador_v5\\src\\arquivos_entrada\\conexao_custos_rodo_db_v1.csv'
address_ferro = 'C:\\Users\\mauricio.longato\\workspace\\Roteirizador_v5\\src\\arquivos_entrada\\conexao_custos_ferro_db_v1.csv'
address_municipios = 'C:\\Users\\mauricio.longato\\workspace\\Roteirizador_v5\\src\\arquivos_entrada\\municipios_mod.csv'
address_rotas = 'C:\\Users\\mauricio.longato\\workspace\\Roteirizador_v5\\src\\arquivos_entrada\\cenarios_rotas.csv'

'''#Abre arquivos de custos e formata dados'''
t_abertura_inicio  = time.time()
conexoes_hidro     = in_out.input.distancias(address_hidro)
conexoes_rodo      = in_out.input.distancias(address_rodo)
conexoes_ferro     = in_out.input.distancias(address_ferro)
municipios         = in_out.input.municipios(address_municipios)
lista_rotas        = in_out.input.rotas(address_rotas)
t_abertura_final_arquivos = time.time()
print "...Arquivos carregados - tempo  : ", str(t_abertura_final_arquivos-t_abertura_inicio)


'''Cria lista das vias e cenarios'''
cenarios     = caminhos.constroi_trechos(municipios, lista_rotas)
malha_rodo   = caminhos.M_malha(conexoes_rodo,"rodo")
malha_hidro  = caminhos.M_malha(conexoes_hidro,"hidro")
malha_ferro  = caminhos.M_malha(conexoes_ferro,"ferro")
t_estruturacao_dados = time.time()
print "...Arquivos estruturados - tempo: ", str(t_estruturacao_dados - t_abertura_final_arquivos)

'''Avaliar se temos as informacoes de cada etapa e mantem somente os validos'''
print "total de cenarios propostos    : ", len(cenarios)
cenarios_validos = []
cenarios_descartados = []
for cenario in cenarios:
    cont = len(cenario)
    for etapa in cenario:
        if etapa.modal == 'rodo':
            rotas = hashmap.get(malha_rodo, etapa.cidade_origem)
            if rotas <> None:
                for rota in rotas:
                    if rota.cidade_destino == etapa.cidade_destino:
                        cont = cont - 1
                        etapa.distancia = rota.get()[5]
                        etapa.custo_pedagio   = rota.get()[6]

        if etapa.modal == 'ferro':
            rotas = hashmap.get(malha_ferro, etapa.cidade_origem)
            if rotas <> None:
                for rota in rotas:
                    if rota.cidade_destino == etapa.cidade_destino:
                        cont = cont - 1
                        etapa.distancia = rota.get()[5]
                        etapa.custo_pedagio   = rota.get()[6]


        if etapa.modal == 'hidro':
            rotas = hashmap.get(malha_hidro, etapa.cidade_origem)
            if rotas <> None:
                for rota in rotas:
                    if rota.cidade_destino == etapa.cidade_destino:
                        cont = cont - 1
                        etapa.distancia = rota.get()[5]
                        etapa.custo_pedagio   = rota.get()[6]

    if cont == 0:
        cenarios_validos.append(cenario)
        for etapa in cenario:
            etapa.calcula_frete()
    else:
        cenarios_descartados.append(cenarios)

print "quantidade de cenarios validos : ", len(cenarios_validos)
t_final_triagem_cenarios = time.time()


'''Calcula transbordo'''
for rota in cenarios_validos:
    modal_inicial = 0
    for etapa in rota:
        modal_final = etapa.modal
        if modal_inicial == 0:
            etapa.custo_transbordo = 0
        if modal_inicial <> 0:
            etapa.custo_transbordo = Calc.frete_transbordo(modal_inicial, modal_final, etapa.carga)
        modal_inicial = modal_final

'''Soma todos os custos'''
# Custo total da etapa
for custo_cenario in cenarios_validos:
    for etapa in custo_cenario:
        etapa.frete_total()

# Custo total da rota
for rota in cenarios_validos:
    custo_total_rota = 0
    for etapa in rota:
        custo_total_rota = custo_total_rota + etapa.custo_total

    for etapa in rota:
        etapa.custo_total_rota = custo_total_rota
        #print etapa.get_full()

#custo_cenarios_total.append(custo_etapa)
t_calculo_final = time.time()

#Formato dados pandas
#columns = ('id_rota_origem_destino','n_rota','n_etapa','cenario','cidade_origem','cidade_destinocidade_destino','modal','carga','distancia','frete_peso','custo_pedagio','custo_financeiro','custo_seguro','custo_perda_carga','custo_transbordo','capacidade_do_modal','custo_total','custo_total_rota','id_rota_origem_destino','n_rota','n_etapa','cenario','cidade_origem','cidade_destino','modal','carga','distancia','frete_peso','custo_pedagio','custo_financeiro','custo_seguro','custo_perda_carga','custo_transbordo','capacidade_do_modal','custo_total','custo_total_rota','id_rota_origem_destino','n_rota','n_etapa','cenario','cidade_origem','cidade_destino','modal','carga','distancia','frete_peso','custo_pedagio','custo_financeiro','custo_seguro','custo_perda_carga','custo_transbordo','capacidade_do_modal','custo_total','custo_total_rota')
#
#for custo_cenario in custo_cenarios:
#    for etapa in custo_cenario:
#        row = etapa.get_full()


in_out.output.saida_custos_db(cenarios_validos, '20160705_Roteirizacao')
in_out.output.saida_custos_csv(cenarios_validos)
in_out.output.saida_relatorio_padrao(cenarios_validos)

print "...Calculos feitos - tempo:",str(t_calculo_final-t_final_triagem_cenarios)


#for rota in cenarios_validos:
#    for etapa in rota:
#        row = etapa.get_full()
#        in_out.output.atualiza_DB_rotas(row)

