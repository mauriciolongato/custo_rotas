# -*- coding: utf-8 -*-
import csv
import sys

def distancias(address):
    f = open(address,'r')
    try:
        matriz_rotas = []
        for line in f.readlines():
            matriz_rotas.append(line.split(";"))
        f.close()
        #    Transforma em float
        nrows = len(matriz_rotas)
        ncols = len(matriz_rotas[0])
        for row in range(nrows):
            matriz_rotas[row][5] = float(matriz_rotas[row][5].replace(",","."))
            matriz_rotas[row][6] = float(matriz_rotas[row][6].replace(",","."))

    finally:
        f.close()
    return matriz_rotas

def municipios(address):
    f = open(address,'r')
    try:
        m_municipios = []
        for line in f.readlines():
            m_municipios.append(line.split(";"))
        f.close()
        #    Transforma em float
        nrows = len(m_municipios)
        ncols = len(m_municipios[0])
        for row in range(nrows):
            m_municipios[row][1] = m_municipios[row][1].replace(" ","_")
            m_municipios[row][2] = m_municipios[row][2].replace(" ","_")
            m_municipios[row][3] = m_municipios[row][3].replace(" ","_")
            m_municipios[row][6] = m_municipios[row][6].replace(" ","_").replace("\n","")
            m_municipios[row][0] = float(m_municipios[row][0].replace(",","."))
            m_municipios[row][3] = float(m_municipios[row][3].replace(",","."))
            m_municipios[row][5] = float(m_municipios[row][5].replace(",","."))

    finally:
        f.close()

    return m_municipios

def rotas(address):
    f = open(address,'r')
    try:
        rotas = []
        for line in f.readlines():
            rotas.append(line.split(";"))
        f.close()
        #    Transforma em float
        nrows = len(rotas)
        ncols = len(rotas[0])
        for row in range(nrows):
            rotas[row][0] = int(rotas[row][0].replace("' '","").replace("\n",""))
            rotas[row][1] = int(rotas[row][1].replace("' '","").replace("\n",""))
            rotas[row][2] = rotas[row][2].replace("' '","").replace("\n","")
            rotas[row][3] = rotas[row][3].replace("' '","").replace("\n","")
            rotas[row][4] = rotas[row][4].replace("' '","").replace("\n","")
            rotas[row][5] = rotas[row][5].replace("' '","").replace("\n","")

    finally:
        f.close()
    return rotas

