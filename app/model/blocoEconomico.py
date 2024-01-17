class BlocoEconomico:

    @staticmethod
    def get_all_bloco_economico(db):
        return db.execute("""
            select b.blocoEconomicoId as bId, b.nome as bNome, count(*) as qtdPaises from pais p
                inner join paisBlocoEconomico pb
                    on p.paisId = pb.paisId
                inner join blocoEconomico b
                    on pb.blocoEconomicoId = b.blocoEconomicoId
            group by pb.blocoEconomicoId
            order by bNome;
        """
        ).fetchall()
    
    @staticmethod
    def get_info_bloco_economico(db, codigo):
        return {
            
            'info': BlocoEconomico.get_qtd_paises(db, codigo),
            'listaPais': BlocoEconomico.get_all_pais(db, codigo),
            'ncmImportacao': BlocoEconomico.get_top_ncm(db, codigo, "import"),
            'ncmExportacao': BlocoEconomico.get_top_ncm(db, codigo, "export"),
            'paisImportacao': BlocoEconomico.get_top_pais(db, codigo, "import"),
            'paisExportacao': BlocoEconomico.get_top_pais(db, codigo, "export"),
            'estadoImportacao': BlocoEconomico.get_top_estado(db, codigo, "import"),
            'estadoExportacao': BlocoEconomico.get_top_estado(db, codigo, "export")
        }
    

    @staticmethod
    def get_top_ncm(db, codigo, tipo):
        return db.execute("""
            select a.atividadeEconomicaId, a.descricaoNCM, sum(m.valorFob) as totalFob, avg(valorFob) as mediaFob, count(*) as qtdMovimentacao from movimentacao m
                inner join atividadeEconomica a
                    on a.atividadeEconomicaId = m.atividadeEconomicaId
                inner join paisBlocoEconomico pb
                    on pb.paisId = m.paisId
                where pb.blocoEconomicoId = ? and m.tipo = ?
                group by a.atividadeEconomicaId
                order by totalFob desc
            limit 10
        """, [codigo, tipo]
        ).fetchall()
    
    @staticmethod
    def get_top_pais(db, codigo, tipo):
        return db.execute("""
            select p.paisId as pId, p.nome as pNome, p.sigla as pSigla, sum(m.valorFob) as totalFob, avg(valorFob) as mediaFob, count(*) as qtdMovimentacao from movimentacao m
                inner join pais p
                    on p.paisId = m.paisId
                inner join paisBlocoEconomico pb
                    on pb.paisId = m.paisId
                where pb.blocoEconomicoId = ? and m.tipo = ?
                group by p.paisId
                order by totalFob desc
            limit 10
        """, [codigo, tipo]
        ).fetchall()
    
    @staticmethod
    def get_top_estado(db, codigo, tipo):
        return db.execute("""
            select e.estadoId as eId, e.nome as eNome, e.sigla as eSigla, sum(m.valorFob) as totalFob, avg(valorFob) as mediaFob, count(*) as qtdMovimentacao from movimentacao m
                inner join estado e
                    on e.estadoId = m.estadoId
                inner join paisBlocoEconomico pb
                    on pb.paisId = m.paisId
                where pb.blocoEconomicoId = ? and m.tipo = ?
                group by e.estadoId
                order by totalFob desc
            limit 10
        """, [codigo, tipo]
        ).fetchall()

    @staticmethod
    def get_qtd_paises(db, codigo):
        return db.execute("""
            select b.blocoEconomicoId as bId, b.nome as bNome, count(*) as qtdPaises from pais p
                inner join paisBlocoEconomico pb
                    on p.paisId = pb.paisId
                inner join blocoEconomico b
                    on pb.blocoEconomicoId = b.blocoEconomicoId
                where pb.blocoEconomicoId = ?
                order by p.paisId;
        """, [codigo]).fetchone()
    
    @staticmethod
    def get_all_pais(db, codigo):
        return db.execute("""
            select p.paisId as pId, p.nome as pNome, p.sigla as pSigla from pais p
                inner join paisBlocoEconomico pb
                    on p.paisId = pb.paisId
                where pb.blocoEconomicoId = ?
                order by p.paisId;
        """, [codigo]
        ).fetchall()
