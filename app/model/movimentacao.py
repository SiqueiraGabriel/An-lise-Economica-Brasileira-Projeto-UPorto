class Movimentacao:

    @staticmethod
    def get_all_info(db, codigo, mes):
        return {
            "mes" : mes[codigo-1],
            "estadoImportacao": Movimentacao.get_top_estados(db, codigo, "import"),
            "estadoExportacao": Movimentacao.get_top_estados(db, codigo, "export"),
            "paisImportacao": Movimentacao.get_top_pais(db, codigo, "import"),
            "paisExportacao": Movimentacao.get_top_pais(db, codigo, "export"),
            "atividadeImportacao": Movimentacao.get_top_ncm(db, codigo, "import"),
            "atividadeExportacao": Movimentacao.get_top_ncm(db, codigo, "export"),
            'transporteImportacao': Movimentacao.get_top_formaTransporte(db, codigo, "import"),
            'transporteExportacao': Movimentacao.get_top_formaTransporte(db, codigo, "export")
        }
    

    @staticmethod
    def create_sql_search(db, dados):
        valores = []

        sql = """
            select e.estadoId as eId, e.sigla as eSigla, t.tipoAtividadeId, p.paisId as pId, p.sigla as pSigla, m.mes, e.nome as eNome, p.nome as pNome, t.descricao as tDescricao, t.codigo as tCodigo, m.valorFob from movimentacao m
                inner join pais p 
                    on m.paisId = p.paisId
                inner join estado e
                    on m.estadoId = e.estadoId
                inner join atividadeEconomica a
                    on a.atividadeEconomicaId = m.atividadeEconomicaId
                inner join tipoAtividade t
                    on t.tipoAtividadeId = a.tipoAtividadeId
            where m.tipo = ?
        """

        #Array que contém os parâmetros utilizados
        valores.append(dados["tipo"])

        if(dados["pais"] != "todos"):
            valores.append(dados["pais"])
            sql += "and p.paisId = ?"
        if(dados["estado"] != "todos"):
            valores.append(dados["estado"])
            sql += "and e.estadoId = ?"
        if(dados["mes"] != "todos"):
            valores.append(dados["mes"])
            sql += "and m.mes = ?"
        if(dados["tipoAtividade"] != "todos"):
            valores.append(dados["tipoAtividade"])
            sql += "and a.tipoAtividadeId = ?"

        return [sql, valores]


    @staticmethod 
    def advanced_search(db, dados):
        
        valores = {
            "topPais": [], "topEstado": [], "topMes": [], "topTipoAtividade": []
        }

        instrucao_sql = Movimentacao.create_sql_search(db, dados)

        valores["resumo"] = db.execute("select count(*) as qtdMovimentacao, sum(valorFob) as totalFob, avg(valorFob) as mediaFob from (" + instrucao_sql[0] + ")", instrucao_sql[1]).fetchall()

        if(dados["pais"] == "todos"):
            valores["topPais"] = db.execute(
                f"select pId, pNome, pSigla,  count(*) as qtdMovimentacao, sum(valorFob) as totalFob, avg(valorFob) as mediaFob from ({instrucao_sql[0]}) group by pId order by totalFOb Desc limit 10", instrucao_sql[1]).fetchall()
        if(dados["estado"] == "todos"):
            valores["topEstado"] = db.execute("select eId, eNome, eSigla, count(*) as qtdMovimentacao, sum(valorFob) as totalFob, avg(valorFob) as mediaFob from (" + instrucao_sql[0] + ") group by eId order by totalFOb Desc limit 10", instrucao_sql[1]).fetchall()
        if(dados["mes"] == "todos"):
            valores["topMes"] = db.execute("select mes, count(*) as qtdMovimentacao, sum(valorFob) as totalFob, avg(valorFob) as mediaFob from (" + instrucao_sql[0] + ") group by mes order by mes", instrucao_sql[1]).fetchall()
        if(dados["tipoAtividade"] == "todos"):
            valores["topTipoAtividade"] = db.execute("select tipoAtividadeId, tDescricao, tCodigo, count(*) as qtdMovimentacao, sum(valorFob) as totalFob, avg(valorFob) as mediaFob from (" + instrucao_sql[0] + ") group by tipoAtividadeId order by totalFOb Desc limit 10", instrucao_sql[1]).fetchall()
        
        return valores

    @staticmethod
    def info_search(db, dados, mes):
        valores = {
            "tipo": "Importação" if dados["tipo"] is "import" else "Exportação",
            "pais": "Todos" if dados["pais"] == "todos" else db.execute("SELECT nome from pais where paisId = ?", [dados["pais"]]).fetchone(),
            "estado": "Todos" if dados["estado"] == "todos" else db.execute("SELECT nome from estado where estadoId = ?", [dados["estado"]]).fetchone(),
            "tipoAtividade": "Todos" if dados["tipoAtividade"] == "todos" else db.execute("SELECT descricao from tipoAtividade where tipoAtividadeId = ?", [dados["tipoAtividade"]]).fetchone(),
            "mes": "Todos" if dados["mes"] == "todos" else mes[int(dados["mes"]) - 1]
        }

        return valores


    @staticmethod
    def get_top_estados(db, codigo, tipo):
        return db.execute("""
            select e.estadoId as eId, e.nome as eNome, e.sigla as eSigla, count(*) as qtdMovimentacao, sum(m.valorFob) as totalFob, avg(m.valorFob) as mediaFob, count(distinct m.formaTransporte) as qtdFormaTransporte from movimentacao m
                inner join estado e
                    on e.estadoId = m.estadoId
                where m.mes = ? and m.tipo = ?
                group by e.estadoId
                order by totalFob DESC
                limit 10;
        """, [codigo, tipo]
        ).fetchall()
    
    
    
    @staticmethod
    def get_top_formaTransporte(db, codigo, tipo):
        return db.execute("""
            select m.formaTransporte, count(*) as qtdMovimentacao, sum(m.valorFob) as totalFob, avg(m.valorFob) as mediaFob from movimentacao m
                where m.mes = ? and tipo = ?
                group by m.formaTransporte
                order by totalFob DESC
            limit 10;                      
        """, [codigo, tipo]
        ).fetchall()
    
    @staticmethod
    def get_top_pais(db, codigo, tipo):
        return db.execute("""
                    
            select p.paisId as pId, p.nome as pNome, count(*) as qtdMovimentacao, sum(m.valorFob) as totalFob, avg(m.valorFob) as mediaFob from movimentacao m
                inner join pais p
                    on p.paisId = m.paisId
                where m.mes = ? and tipo = ?
                group by p.paisId
                order by totalFob desc
            limit 10;
        """, [codigo, tipo]
        ).fetchall()
    
    @staticmethod
    def get_top_ncm(db, codigo, tipo):
        return db.execute("""
            select a.atividadeEconomicaId as codNcm, a.descricaoNCM as ncmNome, sum(m.valorFob) as totalFob, avg(valorFob) as mediaFob, count(*) as qtdMovimentacao from atividadeEconomica a
                inner join movimentacao m
                    on a.atividadeEconomicaId = m.atividadeEconomicaId
                where m.mes = ? and m.tipo = ?
                group by a.atividadeEconomicaId
                order by totalFob DESC
            limit 10;
        """, [codigo, tipo]
        ).fetchall()