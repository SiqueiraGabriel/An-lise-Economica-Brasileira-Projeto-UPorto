import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from flask import render_template, Flask
import logging
import db
from model.estado import Estado
from model.pais import Pais
from model.blocoEconomico import BlocoEconomico
from model.regiao import Regiao
from model.TipoAtividade import TipoAtividade
from model.atividadeEconomica import AtividadeEconomica
from model.movimentacao import Movimentacao
from model.index import Index

mes = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro"]


APP = Flask(__name__)

# Start page
@APP.route('/')
def index():
    # TODO
    return render_template('index.html', info = Index.get_basic_info(db), select = Index.get_info_select_form(db, mes))


@APP.route("/estados/")
def listar_estados(): 
    return render_template('listar_estados.html', estados = Estado.get_all_estados(db))

@APP.route("/estados/<int:codigo>/")
def mostrar_estado(codigo):
    return render_template("estado.html", 
                           estado = Estado.get_basic_info(db, codigo),
                        )

@APP.route("/search/estados/<expressao>")
def busca_estado(expressao):
    valores = expressao.split("&")
    nome = valores[0].split("=")[1]
    sigla = valores[1].split("=")[1]

    return render_template("listar_estados.html", estados = Estado.get_all_estado_search(db, nome, sigla))


@APP.route("/paises/")
def listar_paises():
    return render_template("listar_paises.html", paises = Pais.get_all_paises(db))

@APP.route("/paises/<int:codigo>/")
def mostrar_pais(codigo):
    return render_template("pais.html", pais = Pais.get_basic_info(db, codigo))

@APP.route("/search/paises/<expressao>")
def busca_pais(expressao):
    valores = expressao.split("&")
    nome = valores[0].split("=")[1]
    sigla = valores[1].split("=")[1]

    return render_template("listar_paises.html", paises = Pais.get_all_paises_search(db, nome, sigla))


@APP.route("/bloco_economico/")
def listar_bloco():
    return render_template("listar_bloco_economicos.html", blocos = BlocoEconomico.get_all_bloco_economico(db))

@APP.route("/bloco_economico/<int:codigo>")
def bloco_economico(codigo):
    return render_template("bloco_economico.html", bloco = BlocoEconomico.get_info_bloco_economico(db, codigo))

@APP.route("/tipo_atividade/")
def listar_atividades():
    return render_template("listar_tipoAtividade.html", atividade = TipoAtividade.get_all_tipoAtividade(db))

@APP.route("/tipo_atividade/<int:codigo>")
def tipo_atividade(codigo):
    return render_template("tipo_atividade.html", atividade = TipoAtividade.get_basic_info(db, codigo))


@APP.route("/regiao/")
def listar_regiao():
    return render_template("listar_regiao.html", regiao = Regiao.get_all_regiao(db))


@APP.route("/regiao/<regiao>")
def regiao(regiao):
    return render_template("regiao.html", regiao = Regiao.get_basic_info(db, regiao))

@APP.route("/ncm/")
def listar_ncm():
    return render_template("listar_Ncm.html", ncm = AtividadeEconomica.get_all_ncm(db))

@APP.route("/ncm/<int:codigo>/")
def ncm(codigo):
    return render_template("ncm.html", ncm = AtividadeEconomica.get_info_ncm(db, codigo))

@APP.route("/search/ncm/<expressao>")
def buscar_ncm(expressao):
    valores = expressao.split("&")
    codigo = valores[0].split("=")[1]
    descricao = valores[1].split("=")[1]

    return render_template("listar_ncm.html", ncm = AtividadeEconomica.get_all_ncm_search(db, codigo, descricao))



@APP.route("/movimentacao/")
def listar_movimentacao():
    return render_template("listar_movimentacao.html", mes = mes)


@APP.route("/movimentacao/<int:codigo>")
def movimentacao(codigo):
    return render_template("movimentacao.html", movimentacao = Movimentacao.get_all_info(db, codigo, mes))

@APP.route("/movimentacao/search/<exp>")
def buscar_movimentacao(exp):
    valores = exp.split("&")

    dados = {
        "tipo": valores[0].split("=")[1],
        "pais": valores[1].split("=")[1],
        "estado": valores[2].split("=")[1],
        "mes": valores[3].split("=")[1],
        "tipoAtividade": valores[4].split("=")[1]
    }
    

    return render_template("search_movimentacao.html", dados = Movimentacao.advanced_search(db, dados), mes = mes, info = Movimentacao.info_search(db, dados, mes))

