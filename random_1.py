import random
import numpy as np
from faker import Faker as fk
import psycopg2
fk = fk("pt_BR")


config = {
    'dbname':'betdb',
    'user':'paulo',
    'password':'dT5GNc6ANDRpUpTPTeiUeA',
    'host':'clutch-master-2467.g8x.gcp-southamerica-east1.cockroachlabs.cloud',
    'port':'26257'
}


def connect():
# Establish database connection
    cnx = psycopg2.connect(**config)
    print("Conexão com Database OK!")

    # Create a cursor object
    with cnx.cursor() as cursor:
        cursor.execute("SELECT NOW();")
        queries(cursor, cnx)

def queries(cursor, cnx):
    cursor.execute("DROP TABLE IF EXISTS usuário, depósito, Usuário_Depósito, esportes, aposta, cassino")
    print("Tabelas atualizadas!")

    #TABELA USUÁRIO
    create_tb = """
    CREATE TABLE Usuário (
    id_usuário      VARCHAR(255) PRIMARY KEY,
    nome_usuário    VARCHAR(255),
    email           VARCHAR(255) UNIQUE,
    banca           FLOAT,
    qntd_cassino    INT,
    qntd_bet        INT,
    dia_aposta      INT,
    mes_aposta      INT,
    ano_aposta      INT
);

    """
    cursor.execute(create_tb)

    #TABELA DEPÓSITO
    create_tb = """
    CREATE TABLE Depósito (
    id_pagamento    INT PRIMARY KEY,
    nome_banco      VARCHAR(255),
    pix             BOOLEAN,
    número_cartão   INT,
    CVV_cartão      INT,
    quantidade      FLOAT,
    UNIQUE (nome_banco, número_cartão, CVV_cartão, pix, quantidade)
);

    """
    cursor.execute(create_tb)

    #TABELA USUÁRIO COM DEPÓSITO
    create_tb = """
    CREATE TABLE Usuário_Depósito (
    id_usuário      VARCHAR(255),
    id_pagamento    INT,
    nome_banco      VARCHAR(255),
    pix             BOOLEAN,
    número_cartão   INT,
    CVV_cartão      INT,
    quantidade      FLOAT,
    PRIMARY KEY     (id_usuário, id_pagamento),
    FOREIGN KEY     (id_usuário) REFERENCES Usuário(id_usuário),
    FOREIGN KEY     (id_pagamento) REFERENCES Depósito(id_pagamento)
);


    """
    cursor.execute(create_tb)

    #TABELA ESPORTES
    create_tb = """
    CREATE TABLE Esportes (
    id_esporte      VARCHAR(255) PRIMARY KEY,
    nome_jogo       VARCHAR(255),
    jogo_dia        VARCHAR(255),
    jogo_mês        VARCHAR(255),
    jogo_ano        VARCHAR(255),
    equipe1         VARCHAR(255),
    equipe2         VARCHAR(255)
    );
    """
    cursor.execute(create_tb)
    
    #TABELA APOSTA
    create_tb = """
    CREATE TABLE Aposta (
    id_aposta       INT PRIMARY KEY,
    id_esporte      VARCHAR(255),
    id_usuário      VARCHAR(255),
    odds_equipe1    FLOAT,
    odds_equipe2    FLOAT,
    odds_escolhida  FLOAT,
    valor_aposta    FLOAT,
    valor_retorno   FLOAT,
    FOREIGN KEY     (id_usuário) REFERENCES Usuário(id_usuário),
    FOREIGN KEY     (id_esporte) REFERENCES Esportes(id_esporte)
);

    """
    cursor.execute(create_tb)

    #TABELA CASSINO
    create_tb = """
    CREATE TABLE Cassino (
    id_cassino       INT PRIMARY KEY,
    nome_cassino     VARCHAR(255),
    valor_aposta     INT,
    valor_retorno    INT
    );
    """
    cursor.execute(create_tb)
    
    cnx.commit()
    print("Tabelas Criadas!")

def alt_queries(cursor,cnx):
    alt_query = """
    ALTER TABLE Aposta
    ADD CONSTRAINT id_aposta FOREIGN KEY (id_aposta) REFERENCES Aposta(id_aposta)
    ON DELETE CASCADE;    

    ALTER TABLE Usuário
    ADD CONSTRAINT id_usuário FOREIGN KEY (id_usuário) REFERENCES Usuário(id_usuário)
    ON DELETE CASCADE;    


    """
    cursor.execute(alt_query)

    cnx.commit()
    print("Tabelas Alteradas!")
    inserir_queries(cursor,cnx)

def inserir_queries(cursor, cnx):

    #QUERY USUÁRIO
    inserir_query = """
    INSERT INTO Usuário (id_usuário, nome_usuário, email, banca, qntd_cassino, qntd_bet, dia_aposta, mes_aposta, ano_aposta)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for i in range(1, 71):
        nome_usuario = fk.name()
        id_usuario = nome_usuario + i
        emails = ["@gmail.com", "@outlook.com"]
        email_user = id_usuario + random.choice(emails)
        ano_aposta = random.randint(2021,2024)
        mes_aposta = random.randint(1,12)
        dia_aposta = random.randint(1,30)
        qntd_cassino = random.randint(0,800)
        qntd_bet = random.randint(0,700)
        banca = random.randint(-200, 10000)
        _id = (id_usuario, nome_usuario, email_user, banca, qntd_cassino, qntd_bet, dia_aposta, mes_aposta, ano_aposta)
        cursor.execute(inserir_query, _id)
        cnx.commit()


    #QUERY DEPÓSITO
    inserir_query = """
    INSERT INTO depósito (id_pagamento, nome_banco, pix, número_cartão, CVV_cartão, quantidade)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    for i in range(1, 101):
        id_pagamento = i
        bancos = ['Santander', 'Banco do Brasil', 'Itaú', 'PicPay', 'Nubank', 'Bradesco']
        nome_banco = random.choice(bancos)
        pix = bool(random.getrandbits(1))
        if pix == False:
            n_cartao = random.randint(550000231,999123491)
            cvv = random.randint(000,999)
        else:
            n_cartao = bool(0)
            cvv = bool(0)
        
        quantidade = random.randint(30,10000)
        _id = (id_pagamento, nome_banco, pix, n_cartao, cvv, quantidade)
        cursor.execute(inserir_query, _id)
        cnx.commit()

     #QUERY Usuário_Depósito
    inserir_query = """
    INSERT INTO Usuário_Depósito (id_usuário, id_pagamento, nome_banco, pix, número_cartão, CVV_cartão, quantidade)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    for i in range(1,91):
        _id = (id_usuario, id_pagamento, nome_banco, pix, n_cartao, cvv, quantidade)
        cursor.execute(inserir_query, _id)
        cnx.commit()

    #QUERY ESPORTES
    inserir_query = """
    INSERT INTO Esportes (id_esporte, nome_jogo, jogo_dia, jogo_mês, jogo_ano, equipe1, equipe2)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    nome_jogo = random.choice('Futebol','Basquete','CS2')

    for i in range(1,121):
        if nome_jogo == 'Futebol':
            equipes = ['Corinthians','Internacional','Vasco','Flamengo','Barcelona','Real Madrid','Souza','Brasiliense','Cruzeiro','Boca Juniors','Portuguesa','Botafogo']

        if nome_jogo == 'Basquete':
            equipes = ['Dallas Maverics', 'Corinthians','Miami Heat', 'Brooklyn Nets', 'Franca', 'Timberwolves', 'Lakers','Golden State','Grizziles']
    
        if nome_jogo == 'CS2':
            equipes = ['Corinthians', 'Imperial','Spirit','MIBR','Furia','Fluxo','Faze','Liquid','Virtus Pro','SK','NAVI','OG']
            
        jogo_ano = random.randint(2023,2024)
        jogo_mes = random.randint(1,12)
        jogo_dia = random.randint(1,30)
        equipe1 = random.choice(equipes)
        equipe2 = random.choice(equipes)
        id_esporte = equipe1 + equipe2 + jogo_ano + jogo_mes + jogo_dia
        _id = (id_esporte, nome_jogo, jogo_dia, jogo_mes, jogo_ano)
        cursor.execute(inserir_query, _id)
        cnx.commit()

    #QUERY APOSTA
    inserir_query = """
    INSERT INTO Aposta (id_aposta, id_esporte, nome_usuário, odds_equipe1, odds_equipe2, odds_escolhida, valor_aposta, valor_retorno)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    for i in range(1, 161):
        odds = round(random.uniform(1,7), 2)
        odds_equipe1 = random.choice(odds)
        odds_equipe2 = random.choice(odds)
        valor_aposta = random.randint(1,2000)
        ganhou = bool(random.getrandbits(1))
        odds_escolhida = random.choice(odds_equipe1, odds_equipe2)
        if ganhou == True: 
            valor_retorno = valor_aposta * odds_escolhida
        else:
            valor_retorno = 0

        _id = (i, id_esporte, nome_usuario, odds_equipe1, odds_equipe2, odds_escolhida, valor_aposta, valor_retorno)
        cursor.execute(inserir_query, _id)
        cnx.commit()

    
    #QUERY CASSINO
    inserir_query = """
    INSERT INTO Cassino (id_cassino, nome_cassino, valor_aposta, valor_retorno)
    VALUES (%s, %s, %s, %s)
    """
    cassino = ['Tigrinho', 'Touro', 'Avião', 'BlackJack', 'Roleta', 'Penalty']

    for i in range(1,91):
        nome_cassino = random.choice(cassino)
        valor_aposta = random.randint(1,200)
        ganhou = bool(random.getrandbits(1))
        if ganhou == True: 
            valor_retorno = valor_aposta * round(random.uniform(1,6), 2)
        else:
            valor_retorno = 0
        _id = (i, nome_cassino, valor_aposta, valor_retorno)
        cursor.execute(inserir_query, _id)
        cnx.commit()


if __name__ == "__main__":
    connect()
