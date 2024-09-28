import subprocess
import time
import os
import getpass
import sqlite3

def cadastrar_user():
    usuario=input("insira o seu usuario")
    senha=input("insira a sua senha")
    cursor.execute(" INSERT INTO usuarios values (? , ?)" , (usuario, senha))
    

def logar_user(id_user):
    login_vld= False
    usuario= str(input("insira o seu nome de usuario: "))
    senha = str(input("insira a sua senha: "))
    
    try:
        cursor.execute("SELECT * FROM usuarios WHERE nome = ? && senha= ?"(usuario, senha))
        if cursor.fetchone():
            cursor.execute("SELECT id FROM usuarios WHERE nome = ?"(usuario,))
            id_user=cursor.fetchone()
            login_vld= True
            print(f"!! bem vindo {usuario} !!")
        
    except Exception as e:
        print(f"ocorreu um erro : {e}")
    return login_vld
        
    
def criar_materia(nome):
    carga_horaria=input("insira a carga horaria da matéria: ")
    quantidade_falta= input("insira a sua quantidade de faltas: ")
    aluno =nome
    with open('files/materias.txt', 'w') as matérias_arquivo:
        linha= f"{aluno} , {carga_horaria} , {quantidade_falta}"
        matérias_arquivo.write(linha)
  


  

while true:
    conn = sqlite3.connect('usuarios.db')            
    cursor= conn.cursor
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute( "CREATE TABLE usuarios (id INTERGER PRIMARY KEY AUTOINCREMENT , nome text not null, senha varchar not null)")
    cursor.execute("CREATE TABLE materias (id INTERGER PRIMARY KEY AUTOINCREMENT, nome_mtr TEXT NOT NULL, FOREING KEY (id_usuario) REFERENCE usuarios(id)")
    
    
    
    
    
    conn.commit()
    conn.close()