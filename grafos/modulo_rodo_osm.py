from bs4 import BeautifulSoup
import json
import requests
import urllib
import ast
import tratamento_string as ts

class Node:
    def __init__(self):
        self.name = None
        self.lat = None
        self.lon = None
        self.status = None
        self.status_message = None

    def get_node_info(self, url):
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html)
        coord = remover_acentos(soup.p.encode('ISO-8859-1').replace("<p>","").replace("</p>","").replace('"',"'"),'ISO-8859-1')
        coord_list = ast.literal_eval(coord)

        self.name                     = coord_list['name']
        self.lat                      = coord_list['mapped_coordinate'][0]
        self.lon                      = coord_list['mapped_coordinate'][1]
        self.status                   = coord_list['status']
        self.status_message           = coord_list['status_message']

    def list_info(self):
        return [self.name, self.mapped_coordinate_lat, self.mapped_coordinate_lon,self.status, self.status_message]

class Municipio:
    def __init__(self):
        self.place_id       = None
        self.osm_id         = None
        self.osm_type       = None
        self.osm_id         = None
        self.boundingbox    = None
        self.lat            = None
        self.lon            = None
        self.display_name   = None
        self.classe         = None
        self.type           = None
        self.importance     = None
        self.address        = None
        self.city           = None
        self.state_district = None
        self.country        = None
        self.county         = None
        self.state          = None
        self.country_code   = None

    def get_municipio_info(self,url):
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html)
        municipio = ts.remover_acentos(soup.p.encode('ISO-8859-1').replace("<p>","").replace("</p>","").replace('"',"'"),'ISO-8859-1')
        municipio_list = ast.literal_eval(municipio)
        municipio_list = municipio_list[0]

        self.place_id       = int(municipio_list['place_id'])
        self.osm_id         = int(municipio_list['osm_id'])
        self.osm_type       = municipio_list['osm_type']
        self.osm_id         = int(municipio_list['osm_id'])
        self.boundingbox    = municipio_list['boundingbox']
        self.lat            = float(municipio_list['lat'])
        self.lon            = float(municipio_list['lon'])
        self.display_name   = municipio_list['display_name']
        self.classe         = municipio_list['class']
        self.type           = municipio_list['type']
        self.importance     = municipio_list['importance']
        self.address        = municipio_list['address']
        self.city           = municipio_list['address']['city']
        self.state_district = municipio_list['address']['state_district']
        self.country        = municipio_list['address']['country']
        self.county         = municipio_list['address']['county']
        self.state          = municipio_list['address']['state']
        self.country_code   = municipio_list['address']['country_code']

    def list_info(self):
        return [self.place_id,self.osm_id,self.osm_type,self.osm_id,self.boundingbox,self.lat,self.lon,self.display_name,self.classe,self.type,self.importance,self.city,self.state_district,self.country,self.county,self.state]

class Rota:
    def __init__(self):
        self.ponto_partida             = None
        self.ponto_chegada             = None
        self.status_message            = None
        self.found_alternative         = None
        self.route_geometry            = None
        self.status                    = None
        self.via_indices               = None
        self.inicio_lat                = None
        self.inicio_lon                = None
        self.destino_lat               = None
        self.destino_lon               = None
        self.alternative_summaries     = None
        self.via_points                = None
        self.route_instructions        = None
        self.route_name                = None
        self.alternative_names         = None
        self.route_summary             = None
        self.alternative_indices       = None
        self.hint_data                 = None
        self.alternative_geometries    = None
        self.alternative_instructions  = None

    def get_rota(self,ponto_partida,ponto_chegada):
        #obtem as informacoes das posicoes para enviar para o servidor
        lat_inicio          = ponto_partida.lat
        lon_inicio          = ponto_partida.lon
        lat_chegada         = ponto_chegada.lat
        lon_chegada         = ponto_chegada.lon
        self.ponto_partida  = ponto_partida
        self.ponto_chegada  = ponto_chegada

        #faz a requisicao e recebe o resultado
        url = 'http://router.project-osrm.org/viaroute?loc='+str(lat_inicio)+','+str(lon_inicio)+'&loc='+str(lat_chegada)+','+str(lon_chegada)+'&instructions=true'
        headers = {'User-Agent': 'Your User-Agent verification'}
        response = requests.get(url, headers=headers)
        data = response.json()

        #atribui a classe rota as informacoes
        self.status_message            = data['status_message']
        self.found_alternative         = data['found_alternative']
        self.route_geometry            = data['route_geometry']
        self.status                    = data['status']
        self.via_indices               = data['via_indices']
        self.inicio_lat                = data['via_points'][0][0]
        self.inicio_lon                = data['via_points'][0][1]
        self.destino_lat               = data['via_points'][1][0]
        self.destino_lon               = data['via_points'][1][1]
        self.alternative_summaries     = data['alternative_summaries'][0]
        self.via_points                = data['via_points']
        self.route_instructions        = data['route_instructions']
        self.route_name                = data['route_name']
        self.alternative_names         = data['alternative_names']
        self.route_summary             = data['route_summary']
        self.alternative_indices       = data['alternative_indices']
        self.hint_data                 = data['hint_data']
        self.alternative_geometries    = data['alternative_geometries']
        self.alternative_instructions  = data['alternative_instructions']

    def get_full(self):
        return [self.status_message,self.found_alternative,self.route_geometry,self.status,self.via_indices,self.inicio_lat,self.inicio_lon,self.destino_lat,self.destino_lon,self.alternative_summaries,self.via_points,self.route_instructions,self.route_name,self.alternative_names,self.route_summary,self.alternative_indices,self.hint_data,self.alternative_geometries,self.alternative_instructions,self.alternative_instructions]




