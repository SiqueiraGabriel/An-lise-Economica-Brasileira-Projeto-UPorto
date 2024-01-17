class Pais:

    @staticmethod
    def get_all_paises(db):
        return db.execute("SELECT * FROM PAIS order by nome;").fetchall()
    
    @staticmethod
    def format_busca_like(variavel):
        if(len(variavel) > 0):
            return "%" + variavel + "%"
        return variavel

    @staticmethod 
    def get_all_paises_search(db, nome, sigla):

        nome = Pais.format_busca_like(nome)
        sigla = Pais.format_busca_like(sigla)

        if len(nome) == 0 and len(sigla) > 0:
            paises = db.execute("select * from pais where sigla like ? order by nome", [sigla]).fetchall()
        elif len(nome) > 0 and len(sigla) == 0:
            paises = db.execute("select * from pais where nome like ? order by nome", [nome]).fetchall()
        elif len(nome) > 0 and len(sigla) > 0:
            paises = db.execute("select * from pais where nome like ? or sigla like ? order by nome", [nome, sigla]).fetchall()
        else:
            paises = {"paisId": "", "sigla": "", "nome": ""}

        return paises


    @staticmethod
    def get_basic_info(db, codigo):
        return {
            "info": db.execute("SELECT * FROM PAIS WHERE paisId = ?;", [codigo]).fetchone(),
            "blocoEconomico": Pais.get_bloco_economico(db, codigo),
            "estadoImportacao": Pais.get_top_estados(db, codigo, "import"),
            "estadoExportacao": Pais.get_top_estados(db, codigo, "export"),
            "atividadeImportacao": Pais.get_info_atividade_economica(db, codigo, "import"),
            "atividadeExportacao": Pais.get_info_atividade_economica(db, codigo, "export"),
            'transporteImportacao': Pais.get_info_forma_transporte(db, codigo, "import"),
            'transporteExportacao': Pais.get_info_forma_transporte(db, codigo, "export")

        }
    
    @staticmethod
    def get_top_estados(db, codigo, tipo):
        return db.execute("""
            select e.estadoId as eId, e.nome as eNome, count(*) as qtdMovimentacao, sum(valorFob) as totalFob, avg(valorFob) as mediaFob, count(distinct m.formaTransporte) as qtdFormaTransporte from movimentacao m
                inner join estado e
                    on m.estadoId = e.estadoId
                where paisId = ? and m.tipo = ?
                group by m.estadoId
                order by totalFob desc
                limit 10;
        """, [codigo, tipo]
        ).fetchall()
    
    @staticmethod
    def get_bloco_economico(db, codigo):
        return db.execute("""
            select e.blocoEconomicoId as beId, e.nome as beNome from paisBlocoEconomico pb
                inner join BlocoEconomico e
                    on e.blocoEconomicoId = pb.blocoEconomicoId
                where paisId = ?
        """, [codigo]
        ).fetchall()
    
    @staticmethod
    def get_info_atividade_economica(db, codigo, tipo):
        return db.execute("""
            select a.atividadeEconomicaId as codNcm, a.descricaoNcm as NcmNome, count(*) as qtdMovimentacao, sum(valorFob) as totalFob from movimentacao m
                inner join atividadeEconomica a
                    on m.atividadeEconomicaId = a.atividadeEconomicaId
                where m.paisId = ? and tipo = ?
            group by m.atividadeEconomicaId
            order by totalFob desc
            limit 10;              
        """,[codigo, tipo]
        ).fetchall()
    
    @staticmethod
    def get_info_forma_transporte(db, codigo, tipo):
        return db.execute("""
            select formaTransporte, count(*) qtdMovimentacao, sum(valorFob) as totalFob from movimentacao
                where paisId = ? and tipo = ?
                group by formaTransporte
                order by totalFob desc
                limit 5;
        """
        ,[codigo, tipo]
        ).fetchall()