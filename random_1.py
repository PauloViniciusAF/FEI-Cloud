import random
import numpy as np
from faker import Faker as fk
import psycopg2
fk = fk("pt_BR")

'''
config = {
    'dbname':'NOME DO BANCO DE DADOS',
    'user':'NOME USUÁRIO',
    'password':'SENHA',
    'host':'HOST DO BANCO DE DADOS',
    'port':'26257'
}
'''

def connect():
# Establish database connection
    cnx = psycopg2.connect(**config)
    print("Conexão com Database OK!")

    # Create a cursor object
    with cnx.cursor() as cursor:

        cursor.execute("SELECT NOW();")
        queries(cursor, cnx)

def queries(cursor, cnx):
    cursor.execute("DROP TABLE IF EXISTS música, playlist, disco, usuário, artista, playlist_música, música_artista")
    print("Tabelas atualizadas!")
    

    #TABELA ARTISTA
    create_tb = """
    CREATE TABLE artista(
    id_artista      bigint NOT NULL,
    primary key     (id_artista),
    nome_artista    varchar(255),
    nascimento_dia  INT,
    nascimento_mes  INT,
    nascimento_ano  INT
    );
    """
    cursor.execute(create_tb)

    

    #TABELA DISCO
    create_tb = """
    CREATE TABLE Disco (
    id_disco        INT PRIMARY KEY,
    título          VARCHAR(255),
    lançamento_dia  VARCHAR(255),
    lançamento_mes  VARCHAR(255),
    lançamento_ano  VARCHAR(255),
    id_artista      INT,
    FOREIGN KEY (id_artista) REFERENCES Artista(id_artista)
    );
    """
    cursor.execute(create_tb)

    #TABELA MÚSICA
    create_tb = """
    CREATE TABLE Música (
    id_música       INT PRIMARY KEY,
    título          VARCHAR(255),
    duração         INT,
    id_disco        INT,
    FOREIGN KEY (id_disco) REFERENCES Disco(id_disco)
    );
    """
    cursor.execute(create_tb)

    #TABELA USUÁRIO
    create_tb = """
    CREATE TABLE Usuário (
    id_usuário      INT PRIMARY KEY,
    nome_usuário    VARCHAR(255),
    email           VARCHAR(255) UNIQUE,
    registro_dia    VARCHAR(255),
    registro_mes    VARCHAR(255),
    registro_ano    VARCHAR(255)
    );
    """
    cursor.execute(create_tb)

    #TABELA PLAYLIST
    create_tb = """
    CREATE TABLE Playlist (
    id_playlist     INT PRIMARY KEY,
    título          VARCHAR(255),
    id_usuário      INT,
    FOREIGN KEY (id_usuário) REFERENCES Usuário(id_usuário)
    );
    """
    cursor.execute(create_tb)


    #TABELA PLAYLIST COM AS MÚSICAS
    create_tb = """
    CREATE TABLE Playlist_Música (
    id_playlist     INT,
    id_música       INT,
    PRIMARY KEY (id_playlist, id_música),
    FOREIGN KEY (id_playlist) REFERENCES Playlist(id_playlist),
    FOREIGN KEY (id_música) REFERENCES Música(id_música)
    );
    """
    cursor.execute(create_tb)

    #TABELA MÚSICA COM OS ARTISTAS
    create_tb = """
    CREATE TABLE Música_Artista (
    id_música       INT,
    id_artista      INT,
    PRIMARY KEY (id_música, id_artista),
    FOREIGN KEY (id_música) REFERENCES Música(id_música),
    FOREIGN KEY (id_artista) REFERENCES Artista(id_artista)
    );
    """
    cursor.execute(create_tb)

    cnx.commit()
    print("Tabelas Criadas!")
    alt_queries(cursor,cnx)

def alt_queries(cursor,cnx):
    alt_query = """
    ALTER TABLE disco
    ADD CONSTRAINT id_artista FOREIGN KEY (id_artista) REFERENCES artista(id_artista)
    ON DELETE CASCADE;    
    """
    cursor.execute(alt_query)

    cnx.commit()
    print("Tabelas Alteradas!")
    inserir_queries(cursor,cnx)

def inserir_queries(cursor, cnx):

    #QUERY ARTISTA
    inserir_query = """
    INSERT INTO artista (id_artista, nome_artista, nascimento_dia, nascimento_mes, nascimento_ano)
    VALUES (%s, %s, %s, %s, %s)
    """
    for i in range(1, 31):
        nome_artista = fk.name()
        ano = random.randint(1980,2007)
        mes = random.randint(1,12)
        dia = random.randint(1,30)
        _id = (i, nome_artista, dia, mes, ano)
        cursor.execute(inserir_query, _id)
        cnx.commit()


    #QUERY USUÁRIO
    inserir_query = """
    INSERT INTO usuário (id_usuário, nome_usuário, email, registro_dia, registro_mes, registro_ano)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    for i in range(1, 41):
        id_usuario = i
        nome_usuario = fk.first_name() +" "+ fk.last_name()
        user = nome_usuario.replace(" ", "").lower()
        gmail = user+str(id_usuario)+"@gmail.com"
        outlook = user+str(id_usuario)+"@outlook.com"
        email = [gmail, outlook]
        email_user = random.choice(email)
        ano = random.randint(1960,2006)
        mes = random.randint(1,12)
        dia = random.randint(1,30)
        _id = (id_usuario, nome_usuario, email_user, dia, mes, ano)
 
        cursor.execute(inserir_query, _id)
        cnx.commit()


    #QUERY DISCO
    inserir_query = """
    INSERT INTO disco (id_disco, título, lançamento_dia, lançamento_mes, lançamento_ano, id_artista)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    for i in range(1,31):
        titulo = fk.word()
        ano = random.randint(1980,2024)
        mes = random.randint(1,12)
        dia = random.randint(1,30)
        id_artista = random.randint(1,30)
        _id = (i, titulo, dia, mes, ano, id_artista)
        cursor.execute(inserir_query, _id)
        cnx.commit()

    #QUERY MÚSICA
    inserir_query = """
    INSERT INTO música (id_música, título, duração, id_disco)
    VALUES (%s, %s, %s, %s)
    """
    palavra1 = ["Diário", "Not Like", "Você", "BARRAS &", "Jorge", "Castelo &", "A", "Triunfo", "Sucrilhos", "Ouro de", "Me dê", "1406", "Pais e", "The Story of", "PRIDE", "Vamp", "Fantástico", "Se", "Tolo", "Planos", "Proteção", "Tudo que ", "É na", "Ainda é", "Da Vinci", "Moonlight", "Devil In A", "Rumo à", "Aerials", "Wind of", "telepatía"]
    palavra2 = ["You","Imahori","Primavera","4M","Coqueiro","saiu da tumba","baixo","Apocalipse","Sucrilhos","Mundo da Oakley","Vitória","cantar","Ambulante","madrugada","Code","Capadócia","Comédia Humana","oco","New Dress","BARRAS","Maravilha","Change","Tolo","Motivo","'Em Up","Az A Ridah","O.J.","Versículo 3","Filho","Us","Detento"]
    
    for i in range(1, 61):
        p1 = random.choice(palavra1)
        p2 = random.choice(palavra2)
        titulo = p1 + " " + p2
        duracao = random.randint(60,450)
        id_disco = random.randint(1,30)
        _id = (i, titulo, duracao, id_disco)
        cursor.execute(inserir_query, _id)
        cnx.commit()

    
    #QUERY PLAYLIST
    inserir_query = """
    INSERT INTO playlist (id_playlist, título, id_usuário)
    VALUES (%s, %s, %s)
    """
    
    for i in range(1,91):
        titulo = fk.word()
        id_usuario = random.randint(1,40) 
        id_playlist = i
        _id = (id_playlist, titulo, id_usuario)
        cursor.execute(inserir_query, _id)
        cnx.commit()


    #QUERY MÚSICA-ARTISTA 
    inserir_query = """
    INSERT INTO Música_Artista (id_música, id_artista)
    VALUES (%s, %s)
    """
    for i in range(1,61):
        id_musica = i
        id_artista = random.randint(1,30)
        _id = (id_musica, id_artista)
        cursor.execute(inserir_query, _id)
        cnx.commit()



    #QUERY PLAYSLIST-MÚSICA 
    inserir_query = """
    INSERT INTO Playlist_Música (id_playlist, id_música)
    VALUES (%s, %s)
    """
    for i in range(1,81):
        id_playlist = i
        id_musica = random.randint(1,60)
        _id = (id_playlist, id_musica)
        cursor.execute(inserir_query, _id)
        cnx.commit()

if __name__ == "__main__":
    connect()