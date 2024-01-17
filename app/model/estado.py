class Estado:

    @staticmethod
    def get_all_estados(db):
        return db.execute("select * from estado order by nome;").fetchall()
    
    @staticmethod
    def format_busca_like(variavel):
        if(len(variavel) > 0):
            return "%" + variavel + "%"
        return variavel

    @staticmethod 
    def get_all_estado_search(db, nome, sigla):

        nome = Estado.format_busca_like(nome)
        sigla = Estado.format_busca_like(sigla)

        if len(nome) == 0 and len(sigla) > 0:
            estado = db.execute("select * from estado where sigla like ? order by nome", [sigla]).fetchall()
        elif len(nome) > 0 and len(sigla) == 0:
            estado = db.execute("select * from estado where nome like ? order by nome", [nome]).fetchall()
        elif len(nome) > 0 and len(sigla) > 0:
            estado = db.execute("select * from estado where nome like ? or sigla like ? order by nome", [nome, sigla]).fetchall()
        else:
            estado = {"estadoId": "", "sigla": "", "nome": ""}

        return estado




    @staticmethod
    def get_basic_info(db, codigo):
        return {
            'info': db.execute("select * from estado where estadoId = ?", [codigo]).fetchone(),
            'paisImportacao': Estado.get_info_top_pais(db, codigo, "import"),
            'paisExportacao': Estado.get_info_top_pais(db, codigo, "export"),
            'atividadeImportacao': Estado.get_info_atividade_economica(db, codigo, "import"),
            'atividadeExportacao': Estado.get_info_atividade_economica(db, codigo, "export"),
            'transporteImportacao': Estado.get_info_forma_transporte(db, codigo, "import"),
            'transporteExportacao': Estado.get_info_forma_transporte(db, codigo, "export")

        }


    @staticmethod
    def get_info_top_pais(db, codigo, tipo):
        return db.execute("""
            select p.paisId as pId, p.nome as pNome, count(*) as qtdMovimentacao, sum(valorFob) as totalFob, count(distinct m.formaTransporte) as qtdFormaTransporte, avg(m.valorFob) as mediaFob from movimentacao m
                inner join pais p
                    on m.paisId = p.paisId
                where m.estadoId = ? and m.tipo = ?
                group by p.paisId
                order by totalFob desc
                limit 10;
        """
        , [codigo, tipo]).fetchall()
    
    @staticmethod
    def get_info_atividade_economica(db, codigo, tipo):
        return db.execute("""
            select a.atividadeEconomicaId as codNcm, a.descricaoNcm as NcmNome, count(*) as qtdMovimentacao, sum(valorFob) as totalFob from movimentacao m
                inner join atividadeEconomica a
                    on m.atividadeEconomicaId = a.atividadeEconomicaId
                where m.estadoId = ? and tipo = ?
            group by m.atividadeEconomicaId
            order by totalFob desc
            limit 10;              
        """,[codigo, tipo]
        ).fetchall()
    
    @staticmethod
    def get_info_forma_transporte(db, codigo, tipo):
        return db.execute("""
            select formaTransporte, count(*) qtdMovimentacao, sum(valorFob) as totalFob from movimentacao
                where estadoId = ? and tipo = ?
                group by formaTransporte
                order by totalFob desc
                limit 5;
        """
        ,[codigo, tipo]
        ).fetchall()