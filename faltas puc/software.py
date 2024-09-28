import subprocess
import time
import os
import getpass

class matéria:
    def __init__ (self,aluno ,crg_horaria, qnt_falta) :
        self.crg_horaria= crg_horaria
        self.qnt_falta= qnt_falta
        self.nome=aluno
    
    def print_cargah(self):
        carga= self.crg_horaria * (100 / 25)
        falta=self.qnt_falta
        if falta == carga:
            print(" você esta reprovado por falta")
    
    def print_faltas(self):
        carga= self.crg_horaria * (100 / 25)
        pd_faltar= carga - self.qnt_falta
        if pd_faltar != self.qnt_falta: 
            print(f"você ja faltou {self.qnt_falta} porém vc pode faltar {pd_faltar}")
        else:
            print(f"você ja reprovou por falta porra, você faltou {self.qnt_falta} você poderia faltar somente {pd_faltar}")


def cadastrar_user():
    usuario=input("insira o seu usuario")
    senha=input("insira a sua senha")
    with open ('files/usuarios.txt', 'w') as arquivo_cadastro:
        linha=f"{usuario}, {senha} "
        arquivo_cadastro.write(linha)
def logar_user(nome_usuario, senha):
 with open('files/usuarios.txt', 'r') as login_arquivo:
    linhas = login_arquivo.readlines()
    for linha in linhas:
        partes = linha.strip().split(',')
        usuario = None
        senha_usuario = None
        for parte in partes:
            if 'usuario' in parte:
                usuario = parte.split(',')[1].strip()
            elif 'senha' in parte:
                senha_usuario = parte.split(',')[1].strip()
        if usuario == nome_usuario and senha_usuario == senha:
         return True
    return False     
def criar_materia(nome):
    carga_horaria=input("insira a carga horaria da matéria: ")
    quantidade_falta= input("insira a sua quantidade de faltas: ")
    aluno =nome
    with open('files/materias.txt', 'w') as matérias_arquivo:
        linha= f"{aluno} , {carga_horaria} , {quantidade_falta}"
        matérias_arquivo.write(linha)
while true:
    ...