

function searchPais(){
    nome = document.getElementById("nomePais").value
    sigla = document.getElementById("siglaPais").value

    if(sigla.length > 3)
        window.alert("[ERRO] A sigla do país, deve conter no máximo 3 caracteres.")
    else{
        if(nome == "" && sigla == "")
            window.alert("[ERRO] Por favor, informe os dados para busca.")
        else
            window.open(`/search/paises/nome=${nome}&sigla=${sigla}`, "_self")
    }

}

function searchEstado(){
    nome = document.getElementById("nomeEstado").value
    sigla = document.getElementById("siglaEstado").value

    if(sigla.length > 2)
        window.alert("[ERRO] A sigla do Estado deve conter no máximo 2 caracteres.")
    else{
        if(nome == "" && sigla == "")
            window.alert("[ERRO] Por favor, informe os dados para busca.")
        else
            window.open(`/search/estados/nome=${nome}&sigla=${sigla}`, "_self")
        }

    
}

function searchNcm(){
    console.log("Temos erro")
    codigo = document.getElementById("codigoNCM").value
    descricao = document.getElementById("descricaoNCM").value

    if(codigo.length > 8)
        window.alert("[ERRO] O código da NCM deve conter no máximo 8 caracteres.")
    else
        window.open(`/search/ncm/codigo=${codigo}&descricao=${descricao}`, "_self")
}

function advancedSearch(){
    tipo = document.querySelector("#ftipo").value
    pais = document.querySelector("#fpais").value
    estado = document.querySelector("#festado").value
    mes = document.querySelector("#fmes").value
    tipoAtividade = document.querySelector("#ftipoatividade").value

    window.open(`../../movimentacao/search/tipo=${tipo}&pais=${pais}&estado=${estado}&mes=${mes}&tipoAtividade=${tipoAtividade}`, "_self")
}