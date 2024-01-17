
create table TipoAtividade(
    tipoAtividadeId INT auto_increment,
    codigo varchar(2) NOT NULL,
    descricao varchar(60),
    primary key(tipoAtividadeId)
);    

create table AtividadeEconomica(
    atividadeEconomicaId INT NOT NULL,
    tipoAtividadeId INT,
    codigoNCM INT NOT NULL,
    descricaoNCM varchar(100),
    codigoIsic INT,
    descricaoIsic varchar(100),
    primary key(atividadeEconomicaId),
    foreign key(tipoAtividadeId) references tipoAtividade(tipoAtividadeId)
);

create table Estado(
    estadoId INT NOT NULL,
    nome varchar(30),
    sigla varchar(2),
    regiao varchar(20),
    primary key(estadoId)
);

create table BlocoEconomico(
    blocoEconomicoId INT NOT NULL,
    nome varchar(30),
    primary key(blocoEconomicoId)
);

create table Pais(
    paisId INT NOT NULL,
    nome varchar(30),
    sigla varchar(30),
    continente varchar(30),
    primary key(paisId)
);

create table PaisBlocoEconomico(
    paisId INT NOT NULL,
    blocoEconomicoId INT NOT NULL,
    foreign key(paisId) references Pais(paisId),
    foreign key(blocoEconomicoId) references BlocoEconomico(blocoEconomicoId)
);

create table Movimentacao(
    atividadeEconomicaId INT NOT NULL,
    paisId INT NOT NULL,
    estadoId INT NOT NULL,
    ano INT,
    mes INT,
    peso DECIMAL(10, 2),
    valorFob DECIMAL(10,2),
    valorFrete DECIMAL(10,2),
    valorSeguro DECIMAL(10,2),
    tipo varchar(6),
    formaTransporte varchar(20),
    movimentacaoId INT auto_increment,
    primary key(movimentacaoId),
    foreign key(atividadeEconomicaId) references AtividadeEconomica(atividadeEconomicaID),
    foreign key(paisId) references Pais(paisId),
    foreign key(estadoId) references Estado(estadoId)
);

