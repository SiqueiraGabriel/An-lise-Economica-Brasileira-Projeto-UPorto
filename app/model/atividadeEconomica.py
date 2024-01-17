class AtividadeEconomica:

    @staticmethod
    def get_all_ncm(db):
        return {
            'grupoA': AtividadeEconomica.get_all_ncm_tipo(db, 4),
            'grupoB': AtividadeEconomica.get_all_ncm_tipo(db, 3),
            'grupoC': AtividadeEconomica.get_all_ncm_tipo(db, 2),
            'grupoD': AtividadeEconomica.get_all_ncm_tipo(db, 1),
        }
    
    @staticmethod
    def get_all_ncm_search(db, codigo, descricao):
        return {
            'grupoA': AtividadeEconomica.get_all_ncm_search_tipo(db, 4,codigo, descricao),
            'grupoB': AtividadeEconomica.get_all_ncm_search_tipo(db, 3,codigo, descricao),
            'grupoC': AtividadeEconomica.get_all_ncm_search_tipo(db, 2,codigo, descricao),
            'grupoD': AtividadeEconomica.get_all_ncm_search_tipo(db, 1, codigo, descricao),
        }


    @staticmethod
    def format_busca_like(variavel):
        if(len(variavel) > 0):
            return "%" + variavel + "%"
        return variavel

    @staticmethod 
    def get_all_ncm_search_tipo(db , tipo, codigo, descricao):

        codigo = AtividadeEconomica.format_busca_like(codigo)
        descricao = AtividadeEconomica.format_busca_like(descricao)


        if len(codigo) == 0 and len(descricao) > 0:
            ncm = db.execute(
                    """
                    select * from atividadeEconomica 
                             where tipoAtividadeId = ? and descricaoNcm like ? and atividadeeconomicaId in (
                                select distinct atividadeEconomicaId from movimentacao m)
                            order by codigoNcm
                    """, [tipo, descricao]).fetchall()
        elif len(codigo) > 0 and len(descricao) == 0:
            ncm = db.execute(
                """ 
                    select * from atividadeEconomica 
                        where tipoAtividadeId = ? and codigoNcm like ? and atividadeeconomicaId in (
                                select distinct atividadeEconomicaId from movimentacao m)
                    order by codigoNcm   
                """, [tipo, codigo]).fetchall()
        elif len(codigo) > 0 and len(descricao) > 0:
            ncm = db.execute(
                """
                select * from atividadeEconomica 
                    where tipoAtividadeId = ? and (descricaoNcm like ? or codigoNcm like ?) and atividadeeconomicaId in (
                        select distinct atividadeEconomicaId from movimentacao m)
                order by codigoNcm
                
                """, [tipo, descricao, codigo]).fetchall()
        else:
            ncm = {}

        return ncm

    
    @staticmethod
    def get_all_ncm_tipo(db, tipo):
        return db.execute("""
            SELECT * From atividadeEconomica 
                where tipoAtividadeId = ? and atividadeeconomicaId in (
                    select distinct atividadeEconomicaId from movimentacao m  
                )
                order by codigoNCM
        """, [tipo]).fetchall()

    
    @staticmethod
    def get_info_ncm(db, codigo):
        return {
            "info": db.execute("SELECT * FROM AtividadeEconomica WHERE atividadeEconomicaId = ?;", [codigo]).fetchone(),
            "estadoImportacao": AtividadeEconomica.get_top_estados_ncm(db, codigo, "import"),
            "estadoExportacao": AtividadeEconomica.get_top_estados_ncm(db, codigo, "export"),
            "paisImportacao": AtividadeEconomica.get_top_pais_ncm(db, codigo, "import"),
            "paisExportacao": AtividadeEconomica.get_top_pais_ncm(db, codigo, "export"),
            'transporteImportacao': AtividadeEconomica.get_top_formaTransporte_ncm(db, codigo, "import"),
            'transporteExportacao': AtividadeEconomica.get_top_formaTransporte_ncm(db, codigo, "export")
        }
    
    @staticmethod
    def get_top_estados_ncm(db, codigo, tipo):
        return db.execute("""
            select e.estadoId as eId, e.nome as eNome, e.sigla as eSigla, count(*) as qtdMovimentacao, sum(m.valorFob) as totalFob, avg(m.valorFob) as mediaFob from movimentacao m
                inner join estado e
                    on e.estadoId = m.estadoId
                where m.atividadeEconomicaId = ? and m.tipo = ?
                group by e.estadoId
                order by totalFob DESC
                limit 10;
        """, [codigo, tipo]
        ).fetchall()
    
    @staticmethod
    def get_top_pais_ncm(db, codigo, tipo):
        return db.execute("""
            select p.paisId as pId, p.nome as pNome, p.sigla as pSigla, count(*) as qtdMovimentacao, sum(m.valorFob) as totalFob, avg(m.valorFob) as mediaFob from movimentacao m
                inner join pais p
                    on p.paisId = m.paisId
                where atividadeEconomicaId = ? and tipo = ?
                group by m.paisId
                order by totalFob DESC
            limit 10;
        """, [codigo, tipo]
        ).fetchall()
    
    @staticmethod
    def get_top_formaTransporte_ncm(db, codigo, tipo):
        return db.execute("""
            select m.formaTransporte, count(*) as qtdMovimentacao, sum(m.valorFob) as totalFob, avg(m.valorFob) as mediaFob from movimentacao m
                where atividadeEconomicaId = ? and tipo = ?
                group by m.formaTransporte
                order by totalFob DESC
            limit 10;                      
        """, [codigo, tipo]
        ).fetchall()
    
