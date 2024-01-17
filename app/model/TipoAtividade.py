class TipoAtividade:

    @staticmethod
    def get_all_tipoAtividade(db):
        return db.execute("""        
            select t.codigo as codigo, t.tipoAtividadeId as tipoAtividadeId, t.descricao as descricao, count(*) as qtdNcm from tipoAtividade t
                inner join atividadeEconomica a 
                    on a.tipoAtividadeId = t.tipoAtividadeId
                group by a.tipoAtividadeId
                order by codigo;
        """
        ).fetchall()
    
    @staticmethod
    def get_basic_info(db, codigo):
        return {
            'basicInfo': db.execute("SELECT * FROM tipoAtividade where tipoAtividadeId = ?", [codigo]).fetchone(),
            'ncmImportacao': TipoAtividade.get_top_ncm(db, codigo, "import"),
            'ncmExportacao': TipoAtividade.get_top_ncm(db, codigo, "export"),
            'paisImportacao': TipoAtividade.get_top_pais(db, codigo, "import"),
            'paisExportacao': TipoAtividade.get_top_pais(db, codigo, "export"),
            'estadoImportacao': TipoAtividade.get_top_estado(db, codigo, "import"),
            'estadoExportacao': TipoAtividade.get_top_estado(db, codigo, "export")

        }
    

    @staticmethod
    def get_top_ncm(db, codigo, tipo):
        return db.execute("""
            select a.atividadeEconomicaId, a.descricaoNCM, sum(m.valorFob) as totalFob, avg(valorFob) as mediaFob, count(*) as qtdMovimentacao from atividadeEconomica a
                inner join movimentacao m
                    on a.atividadeEconomicaId = m.atividadeEconomicaId
                where a.tipoAtividadeId = ? and m.tipo = ?
                group by a.atividadeEconomicaId
                order by totalFob DESC
            limit 10;
        """, [codigo, tipo]
        ).fetchall()
    
    @staticmethod
    def get_top_pais(db, codigo, tipo):
        return db.execute("""
                    
                select m.paisId, p.nome,  sum(m.valorFob) as totalFob, avg(valorFob) as mediaFob, count(*) as qtdMovimentacao from atividadeEconomica a
                    inner join movimentacao m
                        on a.atividadeEconomicaId = m.atividadeEconomicaId
                    inner join pais p
                        on p.paisId = m.paisId
                    where a.tipoAtividadeId = ? and m.tipo = ?
                    group by  m.paisId
                    order by totalFob DESC
                    limit 10;
            """, [codigo, tipo]
        ).fetchall()
    
    @staticmethod
    def get_top_estado(db, codigo, tipo):
        return db.execute("""
            select e.estadoId, e.nome,  sum(m.valorFob) as totalFob, avg(valorFob) as mediaFob, count(*) as qtdMovimentacao from atividadeEconomica a
            inner join movimentacao m
                on a.atividadeEconomicaId = m.atividadeEconomicaId
            inner join Estado e
                on m.estadoId = e.estadoId
            
            where a.tipoAtividadeId = ? and m.tipo = ?
            group by  m.estadoId
            order by totalFob DESC
            limit 10
        """, [codigo, tipo]
        ).fetchall()