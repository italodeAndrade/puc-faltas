import subprocess
import time
import os
import getpass
import sqlite3

def cadastrar_user():
    usuario=input("insira o seu usuario")
    senha=getpass.getpass(prompt='insira a sua senha: ', stream=None)
    senha2= getpass.getpass(prompt='insira novamente sua senha: ', stream=None)

    while senha != senha2:
        print("!!as senhas inseridas não estão iguais!!")
        senha=getpass.getpass(prompt='insira a sua senha: ', stream=None)
        senha2= getpass.getpass(prompt='insira novamente sua senha: ', stream=None)
        if usuario == 0 or senha == 0 :
            break
    if senha == senha2 :
        cursor.execute(" INSERT INTO usuarios values (? , ?)" , (usuario, senha))
    
    

def logar_user(id_user):
    login_vld= False
    usuario= (input("insira o seu nome de usuario: "))
    senha = getpass.getpass(prompt='insira a sua senha: ', stream=None)

    if usuario != 0 or senha != 0 :
        try:
            cursor.execute("SELECT * FROM usuarios WHERE nome = ?AND senha= ?"(usuario, senha))
            if cursor.fetchone():
                cursor.execute("SELECT id FROM usuarios WHERE nome = ?"(usuario,))
                id_user=cursor.fetchone()
                login_vld= True
                print(f"!! bem vindo {usuario} !!")
                return True
            
        except Exception as e:
            print(f"ocorreu um erro : {e}")
        return login_vld
    else:
        print("cancelando login\n -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            
    
def listar_mtr(id_user):
    cusor.execute("SELECT nome_mtr, flts_aluno , (crg_horaria * 0,25)as flts_possiveis FROM materias WHERE id_usuario = ? ",(id_user,))
    materias = cursor.fetchall()
    if materias:
        for materia , faltas, faltas_possiveis in materias:
            print(f"matéria: {materia} , faltas: {faltas} , ainda pode faltar: {faltas_possiveis}")
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
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- \n 1- criar matéria \n 2- excluir matéria \n 3- adicionar falta \n 4- tirar falta \n")
        sclh= input("qual operação deseja realizar:")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

        



conn = sqlite3.connect('usuarios.db')            
cursor= conn.cursor
cursor.execute("PRAGMA foreign_keys = ON;")
cursor.execute( "CREATE TABLE usuarios (id INTERGER PRIMARY KEY AUTOINCREMENT , nome text not null, senha varchar not null)")
cursor.execute("CREATE TABLE materias (id INTERGER PRIMARY KEY AUTOINCREMENT,nome_mtr TEXT NOT NULL,crg_horaria INTERGER NOT NULL,flts_aluno INTERGER NOT NULL, FOREING KEY (id_usuario) REFERENCE usuarios(id)")

while True:
    id_user = None
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    print(f"1- login \n 2- cadastro")
    sclh= input("escolha operação: ")
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    if sclh == 1 :
            print("insira 0 para sair")
            logar_user(id_user)
            while not logar_user :
                print("login invalido tente novamente ou digite 0 para sair")
                logar_user(id_user)
            main_func(id_user)
    else:
        print("insira 0 para sair")
        cadastrar_user(id_user)
        break
    
    
    
    
conn.commit()
conn.close()