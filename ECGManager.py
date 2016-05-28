#!usr/env/bin/python
#-*-coding:utf-8-*-

from PostGresConnector import *
from ecg_model import *
import datetime
import re

DEBUG = True


class ECGManager(PGConnector):
    schema_sigtd = 'sig_telediagnostico'
    schema_sigtel = 'sigtel'

    def __init__(self, db_name="", config={}):
        super(ECGManager, self).__init__(db_name, config)

    def _buscar_derivacoes_ecg(self, id_conteudo):
        """Busca as derivacoes de acordo com o id_conteudo recebido por
            parametro.
        """
        sql = """SELECT id, amostra, descricao, ganho, id_conteudo_exame_ecg
        FROM {0}.derivacoes_ecg
        where id_conteudo_exame_ecg = {1} order by id """
        result = self.executeQuery(sql
                                   .format(self.schema_sigtd, id_conteudo)
                                   )
        out = []
        for item in result:
            out.append(DerivacaoEcg({
                'id': item[0],
                'amostra': map(int, filter(None, item[1].split(';'))),
                'descricao': item[2],
                'ganho': item[3],
                'id_conteudo_exame_ecg': item[4],
            }))
        return out

    def _buscar_conteudo_ecg(self, id_exame):
        """Busca os conteudos de acordo com o id_exame recebido por parametro,
            retornando a lista de conteudos referente ao exame e a para cada
            conteudo, a lista de derivacoes
        """
        sql = """SELECT id, amplitude, filtro_60_hz, filtro_muscular,
        frequencia_cardiaca, idsync, inclusao, numero,
        quantidade_derivacao, sensibilidade, taxa_amostragem,
        velocidade, id_exame
        FROM {0}.conteudos_exames_ecg where id_exame = {1} order by id ;"""
        result = self.executeQuery(sql
                                   .format(self.schema_sigtd, id_exame)
                                   )
        out = []
        for item in result:
            out.append(ConteudoEcg({
                'id': item[0],
                'amplitude': item[1],
                'filtro_60_hz': item[2],
                'filtro_muscular': item[3],
                'frequencia_cardiaca': item[4],
                'inclusao': item[5],
                'numero': item[6],
                'quantidade_derivacao': item[7],
                'sensibilidade': item[8],
                'taxa_amostragem': item[9],
                'velocidade': item[10],
                'id_exame': item[11],
                'derivacoes': self._buscar_derivacoes_ecg(item[0])
            }))
        return out

    def buscar_exame_completo(self, id):
        """Busca o exame especifico de acordo com o id e
            carrega suas dependecias.
        """
        sql = "select * from {0}.exames where id = {1} order by id"
        ex = self.executeQueryOne(sql.format(self.schema_sigtd, id))
        if not ex:
            return ex
        ecg = Exame(ex)
        ecg.conteudo_ecg = self._buscar_conteudo_ecg(ex['id'])
        return ecg

    def contar_qtd_exames(self):
        """Retorna a quantidade de exames no banco."""
        rs = self.executeQuery("select count(1) from {0}.exames"
                               .format(self.schema_sigtd))
        return rs[0][0]

    def buscar_lista_exames(self, quantidade=1000, pagina=0):
        """Retorna a lista de id(Exame) e id_paciente"""
        sql = "select id, id_paciente from {0}.exames Order by id limit {1}"
        if pagina > 0:
            sql += " offset {0}".format(pagina)
        ex = self.executeQuery(sql.format(self.schema_sigtd, quantidade))
        return ex
