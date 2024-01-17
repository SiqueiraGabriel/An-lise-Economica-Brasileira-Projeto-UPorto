class Index:

    @staticmethod
    def get_basic_info(db):
        return {
            'qtdAtividadeEconomica': db.execute("select count(*) as qtd from AtividadeEconomica;").fetchone(),
            'qtdBlocoEconomico': db.execute("select count(*) as qtd from BlocoEconomico;").fetchone(),
            'qtdEstado': db.execute("select count(*) as qtd from Estado;").fetchone(),
            'qtdMovimentacao': db.execute("select count(*) as qtd from movimentacao;").fetchone(),
            'qtdPais': db.execute("select count(*) as qtd from pais;").fetchone(),
            'qtdPaisBlocoEconomico': db.execute("select count(*) as qtd from paisBlocoEconomico;").fetchone(),
            'qtdTipoAtividade': db.execute("select count(*) as qtd from tipoAtividade;").fetchone(),
        }

    @staticmethod
    def get_info_select_form(db, mes):
        return {
            'pais': db.execute("SELECT * FROM Pais order by nome").fetchall(),
            'estado': db.execute("SELECT * FROM Estado order by nome").fetchall(),
            'mes': mes,
            'tipoAtividade': db.execute("SELECT * FROM tipoAtividade order by descricao;").fetchall()
        }