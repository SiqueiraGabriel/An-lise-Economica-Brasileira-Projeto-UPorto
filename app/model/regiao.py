class Regiao:

    @staticmethod
    def get_all_regiao(db):
        return db.execute("select regiao, count(*) as qtdEstado from Estado group by regiao;").fetchall()
    
    @staticmethod
    def get_basic_info(db, codigo):
        return {
            'basicInfo': db.execute("select distinct regiao from Estado where regiao = ?;", [codigo]).fetchone(),
            'ncmImportacao': Regiao.get_top_ncm(db, codigo, "import"),
            'ncmExportacao': Regiao.get_top_ncm(db, codigo, "export"),
            'paisImportacao': Regiao.get_top_pais(db, codigo, "import"),
            'paisExportacao': Regiao.get_top_pais(db, codigo, "export"),
            'estadoImportacao': Regiao.get_top_estado(db, codigo, "import"),
            'estadoExportacao': Regiao.get_top_estado(db, codigo, "export"),
            'listaEstados': db.execute("SELECT * FROM Estado where regiao = ? order by nome;", [codigo]).fetchall()
        }
    

    @staticmethod
    def get_top_ncm(db, codigo, tipo):
        return db.execute("""
            select a.atividadeEconomicaId, a.descricaoNCM, sum(m.valorFob) as totalFob, avg(valorFob) as mediaFob, count(*) as qtdMovimentacao from atividadeEconomica a
                inner join movimentacao m
                    on a.atividadeEconomicaId = m.atividadeEconomicaId
                inner join estado e
                    on e.estadoId = m.estadoId
                where e.regiao = ? and m.tipo = ?
                group by a.atividadeEconomicaId
                order by totalFob DESC
            limit 10;
        """, [codigo, tipo]
        ).fetchall()
    
    @staticmethod
    def get_top_pais(db, codigo, tipo):
        return db.execute("""
                    
            select p.paisId as pId, p.nome as pNome, count(*) as qtdMovimentacao, sum(m.valorFob) as totalFob, avg(m.valorFob) as mediaFob from movimentacao m
                inner join estado e
                    on e.estadoId = m.estadoId
                inner join pais p
                    on p.paisId = m.paisId
                where e.regiao = ? and tipo = ?
                group by p.paisId
                order by totalFob desc
            limit 10;
        """, [codigo, tipo]
        ).fetchall()
    
    @staticmethod
    def get_top_estado(db, codigo, tipo):
        return db.execute("""
            select e.regiao as eRegiao, e.estadoId as eId,  e.nome as eNome, count(*) as qtdMovimentacao, sum(valorFob) as totalFob, avg(valorFob) as mediaFob from movimentacao m
                inner join estado e
                    on m.estadoId = e.estadoId   
                where regiao = ? and tipo = ?
                group by m.estadoId
                order by totalFob desc
        """, [codigo, tipo]
        ).fetchall()