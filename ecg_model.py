#!usr/env/bin/python
#-*-coding:utf-8-*-


def load_dict(obj, _dict_):
    for key in _dict_.keys():
        obj.__setattr__(key, _dict_[key])


class DerivacaoEcg(object):

    def __init__(self, _dict_):
        self.id = None
        self.amostra = None
        self.descricao = None
        self.ganho = None
        self.id_conteudo_exame_ecg = None
        load_dict(self, _dict_)


class ConteudoEcg(object):

    def __init__(self, _dict_):
        self.id = None
        self.amplitude = None
        self.filtro_60_hz = None
        self.filtro_muscular = None
        self.frequencia_cardiaca = None
        self.inclusao = None
        self.numero = None
        self.quantidade_derivacao = None
        self.sensibilidade = None
        self.taxa_amostragem = None
        self.velocidade = None
        self.id_exame = None
        self.derivacoes = []
        load_dict(self, _dict_)


class Exame(object):

    def __init__(self, _dict_):
        self.id = None
        self.id_especialista = None
        self.hash_arquivo = None
        self.idsync = None
        self.link_arquivo = None
        self.observacao = None
        self.realizacao = None
        self.visualizado = None
        self.id_especialidade = None
        self.id_estabelecimento = None
        self.id_paciente = None
        self.id_prioridade_exame = None
        self.id_responsavel = None
        self.id_solicitante = None
        self.id_tipo_exame = None
        self.fila_exame = None
        self.motivo_urgencia = None
        self.conteudo_ecg = []
        load_dict(self, _dict_)
