# -*- coding: utf-8 -*-
import hashmap
import time
import custos.calculadora_custos as C

def M_malha(conexoes, modal):
    malha = hashmap.new()
    for rodovia in conexoes:
        carga                = str(rodovia[4].replace(" ","_"))
        municipio_de         =  str(rodovia[0]+'_'+rodovia[1].replace(" ","_"))
        municipio_para       = str(rodovia[2]+'_'+rodovia[3].replace(" ","_"))
        custo_pedagio        = float(rodovia[6])
        distancia            = float(rodovia[5])

        custo_rota = C.custos_etapa()
        if rodovia[5] > 0:
            #custo_rota.cenario               = None
            custo_rota.modal                 = modal
            custo_rota.carga                 = carga
            custo_rota.distancia             = distancia
            custo_rota.cidade_origem         = municipio_de
            custo_rota.cidade_destino        = municipio_para
            custo_rota.custo_pedagio         = custo_pedagio

            link = hashmap.get(malha,municipio_de)
            if link == None:
                hashmap.set(malha, municipio_de, [custo_rota])

            if link <> None:
                link.append(custo_rota)
                hashmap.set(malha, municipio_de,link)


    return malha

def rotas(malha, distrito_inicial, distrito_final, caminho=[]):
    caminho = caminho + [distrito_inicial]
    #print "Entrada funcao rotas: ", caminho
    if distrito_inicial == distrito_final:
        return caminho
    if hashmap.get(malha, distrito_inicial) == None:
        #print "Considerou que nao tinha opcao saindo de Andradina"
        return None
    for node in hashmap.get(malha, distrito_inicial):
        #print "node: ", node
        if node not in caminho:
            novo_caminho = rotas(malha, node, distrito_final, caminho)
            if novo_caminho: return novo_caminho
    return None

def constroi_trechos(municipios, lista_rotas):
    id_rota_origem_destino = 0
    cenarios = []
    for rota in lista_rotas:
        if rota[2] == 'rodo':
            cenario_rodo_direto = []
            for municipio in municipios:
                custo_rota = C.custos_etapa()
                municipio_de = str(municipio[1]+'_'+municipio[6].replace(" ","_"))

                custo_rota.id_rota_origem_destino  = id_rota_origem_destino
                custo_rota.n_etapa                 = 1
                custo_rota.n_rota                  = rota[0]
                custo_rota.cenario                 = rota[1]
                custo_rota.cidade_origem           = municipio_de
                custo_rota.cidade_destino          = rota[3]
                custo_rota.modal                   = 'rodo'
                custo_rota.carga                   = 'grao'
                #custo_rota.distancia               = 0

                #print custo_rota.get()
                cenarios.append([custo_rota])
                id_rota_origem_destino = id_rota_origem_destino + 1

        if rota[2] == 'rodo-hidro':
            cenario_rodo_hidro = []
            for municipio in municipios:
                #print "entrada: ",rota
                custo_rota1 = C.custos_etapa()
                custo_rota2 = C.custos_etapa()
                municipio_de = str(municipio[1]+'_'+municipio[6].replace(" ","_"))

                custo_rota1.id_rota_origem_destino  = id_rota_origem_destino
                custo_rota1.n_etapa                 = 1
                custo_rota1.n_rota                  = rota[0]
                custo_rota1.cenario                 = rota[1]
                custo_rota1.cidade_origem           = municipio_de
                custo_rota1.cidade_destino          = rota[3]
                custo_rota1.modal                   = 'rodo'
                custo_rota1.carga                   = 'grao'
                #custo_rota1.distancia               = rota[5]

                custo_rota2.id_rota_origem_destino  = id_rota_origem_destino
                custo_rota2.n_etapa                 = 2
                custo_rota2.n_rota                  = rota[0]
                custo_rota2.cenario                 = rota[1]
                custo_rota2.cidade_origem           = rota[3]
                custo_rota2.cidade_destino          = rota[4]
                custo_rota2.modal                   = 'hidro'
                custo_rota2.carga                   = 'grao'
                #custo_rota2.distancia               = rota[5]

                #print custo_rota1.get(),custo_rota2.get()
                cenarios.append([custo_rota1,custo_rota2])
                id_rota_origem_destino = id_rota_origem_destino + 1

        if rota[2] == 'rodo-ferro':
            cenario_rodo_hidro = []
            for municipio in municipios:
                #print "rodo-ferro : ",rota
                custo_rota3 = C.custos_etapa()
                custo_rota4 = C.custos_etapa()
                municipio_de = str(municipio[1]+'_'+municipio[6].replace(" ","_"))

                custo_rota3.id_rota_origem_destino  = id_rota_origem_destino
                custo_rota3.n_etapa                 = 1
                custo_rota3.n_rota                  = rota[0]
                custo_rota3.cenario                 = rota[1]
                custo_rota3.cidade_origem           = municipio_de
                custo_rota3.cidade_destino          = rota[3]
                custo_rota3.modal                   = 'rodo'
                custo_rota3.carga                   = 'grao'
                #custo_rota3.distancia               = rota[5]

                custo_rota4.id_rota_origem_destino  = id_rota_origem_destino
                custo_rota4.n_etapa                 = 2
                custo_rota4.n_rota                  = rota[0]
                custo_rota4.cenario                 = rota[1]
                custo_rota4.cidade_origem           = rota[3]
                custo_rota4.cidade_destino          = rota[4]
                custo_rota4.modal                   = 'ferro'
                custo_rota4.carga                   = 'grao'
                #custo_rota4.distancia               = rota[5]

                #print custo_rota3.get(),custo_rota4.get()
                cenarios.append([custo_rota3,custo_rota4])
                id_rota_origem_destino = id_rota_origem_destino + 1

        if rota[2] == 'rodo-hidro-ferro':
            cenario_rodo_hidro_ferro = []
            for municipio in municipios:
                #print "entradarodo-hidro-ferro : ",rota
                custo_rota5 = C.custos_etapa()
                custo_rota6 = C.custos_etapa()
                custo_rota7 = C.custos_etapa()

                municipio_de = str(municipio[1]+'_'+municipio[6].replace(" ","_"))

                custo_rota5.id_rota_origem_destino  = id_rota_origem_destino
                custo_rota5.n_etapa                 = 1
                custo_rota5.n_rota                  = rota[0]
                custo_rota5.cenario                 = rota[1]
                custo_rota5.cidade_origem           = municipio_de
                custo_rota5.cidade_destino          = rota[3]
                custo_rota5.modal                   = 'rodo'
                custo_rota5.carga                   = 'grao'
                #custo_rota5.distancia               = rota[5]

                custo_rota6.id_rota_origem_destino  = id_rota_origem_destino
                custo_rota6.n_etapa                 = 2
                custo_rota6.n_rota                  = rota[0]
                custo_rota6.cenario                 = rota[1]
                custo_rota6.cidade_origem           = rota[3]
                custo_rota6.cidade_destino          = rota[4]
                custo_rota6.modal                   = 'hidro'
                custo_rota6.carga                   = 'grao'
                #custo_rota6.distancia               = rota[5]

                custo_rota7.id_rota_origem_destino  = id_rota_origem_destino
                custo_rota7.n_etapa                 = 3
                custo_rota7.n_rota                  = rota[0]
                custo_rota7.cenario                 = rota[1]
                custo_rota7.cidade_origem           = rota[4]
                custo_rota7.cidade_destino          = rota[5]
                custo_rota7.modal                   = 'ferro'
                custo_rota7.carga                   = 'grao'
                #custo_rota7.distancia               = rota[5]

                #print custo_rota5.get(),custo_rota6.get(),custo_rota7.get()
                cenarios.append([custo_rota5,custo_rota6,custo_rota7])
                id_rota_origem_destino = id_rota_origem_destino + 1



        if rota[2] == 'rodo-ferro-hidro':
            cenario_rodo_hidro_ferro = []
            for municipio in municipios:
                custo_rota8 = C.custos_etapa()
                custo_rota9 = C.custos_etapa()
                custo_rota10 = C.custos_etapa()

                municipio_de = str(municipio[1]+'_'+municipio[6].replace(" ","_"))

                custo_rota8.id_rota_origem_destino  = id_rota_origem_destino
                custo_rota8.n_etapa                 = 1
                custo_rota8.n_rota                  = rota[0]
                custo_rota8.cenario                 = rota[1]
                custo_rota8.cidade_origem           = municipio_de
                custo_rota8.cidade_destino          = rota[3]
                custo_rota8.modal                   = 'rodo'
                custo_rota8.carga                   = 'grao'
                #custo_rota8.distancia               = rota[5]

                custo_rota9.id_rota_origem_destino  = id_rota_origem_destino
                custo_rota9.n_etapa                 = 2
                custo_rota9.n_rota                  = rota[0]
                custo_rota9.cenario                 = rota[1]
                custo_rota9.cidade_origem           = rota[3]
                custo_rota9.cidade_destino          = rota[4]
                custo_rota9.modal                   = 'ferro'
                custo_rota9.carga                   = 'grao'
                #custo_rota9.distancia               = rota[5]

                custo_rota10.id_rota_origem_destino  = id_rota_origem_destino
                custo_rota10.n_etapa                 = 3
                custo_rota10.n_rota                  = rota[0]
                custo_rota10.cenario                 = rota[1]
                custo_rota10.cidade_origem           = rota[4]
                custo_rota10.cidade_destino          = rota[5]
                custo_rota10.modal                   = 'hidro'
                custo_rota10.carga                   = 'grao'
                #custo_rota10.distancia               = rota[5]

                cenarios.append([custo_rota8,custo_rota9,custo_rota10])
                id_rota_origem_destino = id_rota_origem_destino + 1

    return cenarios

