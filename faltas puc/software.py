import subprocess
import time
import os
import getpass
import sqlite3
import hashlib

def cadastrar_user():
    usuario=input("insira o seu usuario: ")

    senha=getpass.getpass(prompt='insira a sua senha: ', stream=None)
    senha2= getpass.getpass(prompt='insira novamente sua senha: ', stream=None)

    while senha != senha2:
        print("!!as senhas inseridas não estão iguais!!")
        senha=getpass.getpass(prompt='insira a sua senha: ', stream=None)
        senha2= getpass.getpass(prompt='insira novamente sua senha: ', stream=None)
        if usuario == 0 or senha == 0 :
            break
    if senha == senha2 :
        senha_codificada=senha.encode('utf-8')
        obj_sha=hashlib.sha256()
        obj_sha.update(senha_codificada)
        senha=obj_sha.hexdigest()
        cursor.execute(" INSERT INTO usuarios(nome, senha) values (? , ?)" , (usuario, senha))
        conn.commit()
    
    

def logar_user(usuario, senha):
    lgn_vld = False
    try:
        senha_codificada = hashlib.sha256(senha.encode('utf-8')).hexdigest()
        senha=senha_codificada
        cursor.execute("SELECT id FROM usuarios WHERE nome = ? AND senha = ?", (usuario, senha))
        result = cursor.fetchone()  
        if result:  
            id_user = result[0]  
            lgn_vld = True  
            print(f"!! Bem-vindo, {usuario} !!")
            return id_user, lgn_vld 
    except Exception as e:
        print(f"ocorreu um erro : {e}")

    return None, lgn_vld
            
    
def listar_mtr(id_user):
    cursor.execute("SELECT nome_mtr, flts_aluno , ((crg_horaria * 0.25) - flts_aluno)as pode_faltar, (crg_horaria * 0.25) as faltas_totais FROM materias WHERE id_usuario = ? ",(id_user,))
    materias = cursor.fetchall()
    if materias:
        for materia , faltas, pode_faltar,faltas_totais, in materias:
            print(f"matéria: {materia} , faltas: {faltas} , ainda pode faltar: {pode_faltar}, faltas totais permitidas: {faltas_totais}")
    else :
        print("nenhuma matéria encontrada")

def criar_mtr(id_user):
    nome= input("insira o nome da matéria: ")
    carga_horaria=input("insira a carga horaria da matéria: ")
    quantidade_falta= input("insira a sua quantidade de faltas: ")
    try:
        cursor.execute("INSERT INTO materias(nome_mtr, crg_horaria,flts_aluno,id_usuario) values (?,?,?,?) ",(nome,carga_horaria,quantidade_falta,id_user))
        conn.commit()
        print("inserção realizada com sucesso!!")
    except sqlite3.Error as e:
        print(f"erro ao inserir os dados {e}")
    
def excluir_mtr(id_user):
    listar_mtr(id_user)
    esclh=input("qual matéria você gostaria de excluir?: ")
    if esclh:
        print("excluindo matéria")
        cursor.execute("DELETE FROM materias WHERE nome_mtr = ? AND id_usuario = ?",(esclh, id_user))
    else:
        print("!!ocorreu um erro na operação!!")

def add_flt(id_user):
    listar_mtr(id_user)
    esclh= input("qual matéria você gostaria de adicionar falta? ")
    faltas= input("quantas faltas você gostaria de adicionar? ")
    if esclh & faltas:
        print(f"adicionando {flatas} faltas na matéria: {esclh}")
        cursor.execute("ALTER materias SET flts_aluno = flts_aluno + ? WHERE id_usuario = ? AND nome_mtr = ?",(faltas,id_user , esclh))
    else:
        print("!!ocorreu um erro na operação!!")

def tirar_flt(id_user):
    istar_mtr(id_user)
    esclh= input("qual matéria você gostaria de tirar falta? ")
    faltas= input("quantas faltas você gostaria de tirar? ")
    if esclh & faltas:
        print(f"adicionando {flatas} faltas na matéria: {esclh}")
        cursor.execute("ALTER materias SET flts_aluno = flts_aluno - ? WHERE id_usuario = ? AND nome_mtr = ?",(faltas,id_user , esclh))
    else:
        print("!!ocorreu um erro na operação!!")

  

def main_func(id):
    while True:
        listar_mtr(id)
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- \n 1- criar matéria \n 2- excluir matéria \n 3- adicionar falta \n 4- tirar falta \n 0-sair")
        
        sclh = int(input("qual operação deseja realizar: "))
        if sclh == 0 :
            print("tchau!!")
            break
        elif sclh == 1:
            criar_mtr(id)
        elif sclh == 2:
            excluir_mtr(id)
        elif sclh == 3:
            add_flt(id)
        elif sclh == 4:
            tirar_flt(id)
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

        



conn = sqlite3.connect('usuarios.db')            
cursor= conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")
'''
CASO NÃO TENHA CRIADO AS TABELAS APENAS TIRAR DO COMENTARIO E APAGAR ESTA LINHA
cursor.execute( "CREATE TABLE usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT , nome text not null, senha varchar not null)")
cursor.execute("CREATE TABLE materias (id INTEGER PRIMARY KEY AUTOINCREMENT,nome_mtr TEXT NOT NULL,crg_horaria INTEGER NOT NULL,flts_aluno  NOT NULL,id_usuario INTEGER, FOREIGN KEY (id_usuario) REFERENCES usuarios(id))")
'''
while True:
    id_user = 0
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    print(f"pressione 0 para sair\n1- login \n2- cadastro")
    sclh= int(input("escolha operação: "))
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    while sclh not in [0,1,2]:
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n !!NÃO EXISTE ESTA OPERAÇÃO ESCOLHA NOVAMENTE!!!")
        print(f"pressione 0 para sair\n1- login \n2- cadastro")
        sclh= int(input("escolha operação: "))
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        
    if sclh == 1:
        usuario = input("insira o seu nome de usuario: ")
        if usuario == '0':
            print("!!cancelando login!!")
            continue

        senha = getpass.getpass(prompt='insira a sua senha: ', stream=None)
        id_user, lgn_vld = logar_user(usuario, senha) 

        if not lgn_vld:
            print("login inválido, tente novamente ou digite 0 para sair.")
            continue

        main_func(id_user)




    elif sclh == 0:
        print("até logo!!")
        break
    else:
        print("insira 0 para sair")
        cadastrar_user()
        
conn.close()