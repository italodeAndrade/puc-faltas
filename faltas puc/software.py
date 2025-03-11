import subprocess
import time
import os
import getpass
import sqlite3
import hashlib

def cadastrar_user():
    usuario = input("Insira o seu usuário: ").strip()
    while not usuario:
        print("Usuário não pode ser vazio!")
        usuario = input("Insira o seu usuário: ").strip()

    senha = getpass.getpass(prompt='Insira a sua senha: ', stream=None)
    senha2 = getpass.getpass(prompt='Insira novamente sua senha: ', stream=None)

    while senha != senha2:
        print("!! As senhas inseridas não coincidem !!")
        senha = getpass.getpass(prompt='Insira a sua senha: ', stream=None)
        senha2 = getpass.getpass(prompt='Insira novamente sua senha: ', stream=None)

    if not senha:
        print("Senha não pode ser vazia!")
        return

    senha_codificada = senha.encode('utf-8')
    obj_sha = hashlib.sha256()
    obj_sha.update(senha_codificada)
    senha_hash = obj_sha.hexdigest()
    
    try:
        cursor.execute("INSERT INTO usuarios(nome, senha) VALUES (?, ?)", (usuario, senha_hash))
        conn.commit()
        print("Usuário cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: Usuário já existe!")
    except Exception as e:
        print(f"Erro ao cadastrar usuário: {e}")

def logar_user(usuario, senha):
    try:
        senha_codificada = hashlib.sha256(senha.encode('utf-8')).hexdigest()
        cursor.execute("SELECT id FROM usuarios WHERE nome = ? AND senha = ?", (usuario, senha_codificada))
        result = cursor.fetchone()
        return (result[0], True) if result else (None, False)
    except Exception as e:
        print(f"Erro durante o login: {e}")
        return None, False

def listar_mtr(id_user):
    try:
        cursor.execute("""
            SELECT nome_mtr, flts_aluno, 
                   ((crg_horaria * 0.25) - flts_aluno) as pode_faltar, 
                   (crg_horaria * 0.25) as faltas_totais 
            FROM materias 
            WHERE id_usuario = ?""", (id_user,))
        materias = cursor.fetchall()
        
        if not materias:
            print("Nenhuma matéria encontrada")
            return
            
        for materia in materias:
            print(f"""
            Matéria: {materia[0]}
            Faltas atuais: {materia[1]}
            Faltas permitidas restantes: {max(materia[2], 0)}
            Total de faltas permitidas: {materia[3]}
            """)
    except Exception as e:
        print(f"Erro ao listar matérias: {e}")

def criar_mtr(id_user):
    try:
        nome = input("Insira o nome da matéria: ").strip()
        while not nome:
            print("Nome da matéria não pode ser vazio!")
            nome = input("Insira o nome da matéria: ").strip()

        carga_horaria = int(input("Insira a carga horária da matéria: "))
        quantidade_falta = int(input("Insira sua quantidade de faltas: "))
        
        cursor.execute("""
            INSERT INTO materias(nome_mtr, crg_horaria, flts_aluno, id_usuario) 
            VALUES (?, ?, ?, ?)""", 
            (nome, carga_horaria, quantidade_falta, id_user))
        conn.commit()
        print("Matéria cadastrada com sucesso!")
    except ValueError:
        print("Erro: Valores numéricos inválidos!")
    except Exception as e:
        print(f"Erro ao criar matéria: {e}")
        conn.rollback()

def excluir_mtr(id_user):
    try:
        listar_mtr(id_user)
        materia = input("Qual matéria deseja excluir?: ").strip()
        if not materia:
            print("Operação cancelada")
            return

        cursor.execute("""
            DELETE FROM materias 
            WHERE nome_mtr = ? AND id_usuario = ?""", 
            (materia, id_user))
        conn.commit()
        print("Matéria excluída com sucesso!" if cursor.rowcount > 0 else "Matéria não encontrada")
    except Exception as e:
        print(f"Erro ao excluir matéria: {e}")
        conn.rollback()

def atualizar_faltas(id_user, operacao):
    try:
        listar_mtr(id_user)
        materia = input(f"Qual matéria deseja {operacao} faltas?: ").strip()
        if not materia:
            print("Operação cancelada")
            return

        quantidade = int(input(f"Quantas faltas deseja {operacao}?: "))
        operador = '+' if operacao == 'adicionar' else '-'
        
        cursor.execute(f"""
            UPDATE materias 
            SET flts_aluno = flts_aluno {operador} ? 
            WHERE id_usuario = ? AND nome_mtr = ?""", 
            (quantidade, id_user, materia))
        conn.commit()
        print("Faltas atualizadas com sucesso!" if cursor.rowcount > 0 else "Matéria não encontrada")
    except ValueError:
        print("Erro: Quantidade inválida!")
    except Exception as e:
        print(f"Erro ao atualizar faltas: {e}")
        conn.rollback()

def main_menu(id_user):
    while True:
        print("\n" + "="*30)
        print("1 - Listar matérias")
        print("2 - Criar nova matéria")
        print("3 - Excluir matéria")
        print("4 - Adicionar faltas")
        print("5 - Remover faltas")
        print("0 - Sair")
        
        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Opção inválida!")
            continue

        if opcao == 0:
            print("Até logo!")
            return
        elif opcao == 1:
            listar_mtr(id_user)
        elif opcao == 2:
            criar_mtr(id_user)
        elif opcao == 3:
            excluir_mtr(id_user)
        elif opcao == 4:
            atualizar_faltas(id_user, 'adicionar')
        elif opcao == 5:
            atualizar_faltas(id_user, 'remover')
        else:
            print("Opção inválida!")

# Configuração do banco de dados
conn = sqlite3.connect('usuarios.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

# Criar tabelas se não existirem
cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    )""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS materias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_mtr TEXT NOT NULL,
        crg_horaria INTEGER NOT NULL,
        flts_aluno INTEGER NOT NULL,
        id_usuario INTEGER,
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
        UNIQUE(id_usuario, nome_mtr)
    )""")
conn.commit()

# Menu principal
while True:
    print("\n" + "="*30)
    print("1 - Login")
    print("2 - Cadastro")
    print("0 - Sair")
    
    try:
        opcao = int(input("Escolha uma opção: "))
    except ValueError:
        print("Opção inválida!")
        continue

    if opcao == 0:
        print("Encerrando sistema...")
        break
        
    elif opcao == 1:
        usuario = input("Usuário: ").strip()
        senha = getpass.getpass("Senha: ")
        user_id, sucesso = logar_user(usuario, senha)
        
        if sucesso:
            print(f"\nBem-vindo(a), {usuario}!")
            main_menu(user_id)
        else:
            print("Credenciais inválidas!")
            
    elif opcao == 2:
        cadastrar_user()
        
    else:
        print("Opção inválida!")

conn.close()