#import grafos.hashmap as hashmap
import math

class custos_etapa:
    def __init__(self,id_rota_origem_destino=0,frete_peso=0,custo_pedagio=0,custo_financeiro=0,custo_seguro=0,custo_perda_carga=0):
        #Caracterizacao
        self.id_rota_origem_destino  = 0
        self.n_rota                  = 0
        self.n_etapa                 = 0
        self.cenario                 = 0
        self.cidade_origem           = None
        self.cidade_destino          = None
        self.modal                   = None
        self.carga                   = None
        self.distancia               = None
        self.frete_peso              = None
        self.custo_pedagio           = 0
        self.custo_financeiro        = None
        self.custo_seguro            = None
        self.custo_perda_carga       = None
        self.custo_transbordo        = 0.0
        self.custo_total             = 0.0
        self.custo_total_rota        = 0.0
        self.capacidade_do_modal     = 0.0

    def get(self):
        vetor = [self.id_rota_origem_destino, self.n_rota, self.cidade_origem, self.cidade_destino, self.modal, self.distancia, self.custo_pedagio]
        return vetor

    def calcula_frete(self):
        if self.modal == 'rodo':
            if self.carga == 'grao' and self.distancia <> None:
                #premissas frete distancia  - 1050 R$/ton
                velocidade = 50.0       #km/h
                a = 0.960649565510911
                b = 0.7180190881
                CDI_dia = 0.000237    #CDI = 9% a.a
                tempo_viagem = ((float(self.distancia)/velocidade)/24)
                numero_eixos = 16.2   #ida 9 volta 7.2 = 16.2
                consignacao = 42.0      #Em toneladas

                #calculos
                self.frete_peso        = a*math.pow(self.distancia,b)
                self.custo_financeiro  = 1050*((math.pow((1+CDI_dia),tempo_viagem))-1)
                self.custo_pedagio     = self.custo_pedagio*numero_eixos/consignacao
                self.custo_seguro      = 1050*0.00133
                self.custo_perda_carga = 1050*0.0029
            else:
                self.frete_peso        = 0
                self.custo_financeiro  = 0
                self.custo_pedagio     = 0
                self.custo_seguro      = 0
                self.custo_perda_carga = 0

        if self.modal == 'ferro':
            if self.carga == 'grao' and self.distancia <> None:
                #premissas frete distancia  - 1050 R$/ton
                velocidade = 15.0       #km/h
                a = 0.5265
                b = 0.7741
                CDI_dia = 0.000237    #CDI = 9% a.a
                tempo_viagem = ((self.distancia/velocidade)/24)
                pedagio = 0.0           #Hidro nao cobra pedagio
                consignacao = 6400.0      #Em toneladas

                #calculos
                self.frete_peso        = a*math.pow(self.distancia,b)
                self.custo_financeiro  = 1050*((math.pow((1+CDI_dia),tempo_viagem))-1)
                self.custo_pedagio     = 0
                self.custo_seguro      = 1050*0.00036
                self.custo_perda_carga = 1050*0.001

            else:
                self.frete_peso        = 0
                self.custo_financeiro  = 0
                self.custo_pedagio     = 0
                self.custo_seguro      = 0
                self.custo_perda_carga = 0

        if self.modal == 'hidro':
            if self.carga == 'grao' and self.distancia <> None:
                #premissas frete distancia  - 1050 R$/ton
                velocidade = 14.0       #km/h
                a = 0.133464770555477
                b = 0.827388669582135
                CDI_dia = 0.000237    #CDI = 9% a.a
                tempo_viagem = ((self.distancia/velocidade)/24)
                pedagio = 0.0           #Hidro nao cobra pedagio
                consignacao = 6000.0      #Em toneladas

                #calculos
                self.frete_peso        = a*math.pow(self.distancia,b)
                self.custo_financeiro  = 1050*((math.pow((1+CDI_dia),tempo_viagem))-1)
                self.custo_pedagio     = 0
                self.custo_seguro      = 1050*0.00025
                self.custo_perda_carga = 1050*0.00198
            else:
                self.frete_peso        = 0
                self.custo_financeiro  = 0
                self.custo_pedagio     = 0
                self.custo_seguro      = 0
                self.custo_perda_carga = 0

    def get_full(self):
        vetor = [self.id_rota_origem_destino,self.n_rota,self.n_etapa,self.cenario,self.cidade_origem,self.cidade_destino,self.modal,self.carga,self.distancia,self.frete_peso,self.custo_pedagio,self.custo_financeiro,self.custo_seguro,self.custo_perda_carga,self.custo_transbordo,self.capacidade_do_modal, self.custo_total,self.custo_total_rota]
        return vetor

    def frete_total(self):
        self.custo_total = self.frete_peso + self.custo_financeiro + self.custo_pedagio + self.custo_perda_carga + self.custo_seguro + self.custo_transbordo

def frete_transbordo(modal_entrada, modal_saida, carga):
    if carga == "grao":
        if modal_entrada == modal_saida:
            return 0.0
        if modal_saida == "rodo":
            return 2.50
        if modal_saida == "hidro":
            #Custo rodo-hidro
            return 8.56
        if modal_saida == "ferro":
            #Custo rodo-hidro
            return 5.99
        return 0
    return 0

'''
def custo_rota(rota):
    custo_total_rota = 0
    for etapa in rota:
        custo_total_rota = custo_total_rota + etapa.frete_total

    return custo_total_rota
'''
#if __name__ == "__main__":
