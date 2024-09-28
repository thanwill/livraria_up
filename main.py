import csv
import sqlite3
import tkinter as tk
from tkinter import filedialog


def criar_tabela_livros():
    
    conn = sqlite3.connect('livraria.db')
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        preco REAL NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()

def adicionar_livro():
    titulo = input("Digite o título do livro: ")
    autor = input("Digite o autor do livro: ")
    preco = float(input("Digite o preço do livro: "))
    
    # Conectar ao banco de dados
    conn = sqlite3.connect('livraria.db')
    cursor = conn.cursor()
    
    # Inserir dados na tabela
    cursor.execute("""
    INSERT INTO livros (titulo, autor, preco)
    VALUES (?, ?, ?)
    """, (titulo, autor, preco))
    
    # Confirmar a transação
    conn.commit()
    
    print(f"Livro '{titulo}' adicionado com sucesso!")
    
    # Fechar conexão
    conn.close()
    
def exibir_todos_livros():
    # Conectar ao banco de dados
    conn = sqlite3.connect('livraria.db')
    cursor = conn.cursor()
    
    # Selecionar todos os registros da tabela
    cursor.execute("SELECT * FROM livros")
    livros = cursor.fetchall()
    
    # Exibir os registros
    if livros:
        for livro in livros:
            print(f"ID: {livro[0]}, Título: {livro[1]}, Autor: {livro[2]}, Preço: {livro[3]}")
    else:
        print("Nenhum livro encontrado.")
    
    # Fechar conexão
    conn.close()
    
def atualizar_preco_livro():
    # Conectar ao banco de dados
    conn = sqlite3.connect('livraria.db')
    cursor = conn.cursor()
    
    # Atualizar preço de um livro
    id_livro = int(input("Digite o ID do livro: "))
    novo_preco = float(input("Digite o novo preço do livro: "))
    
    cursor.execute("""
    UPDATE livros
    SET preco = ?
    WHERE id = ?
    """, (novo_preco, id_livro))
    
    conn.commit()
    conn.close()
    
def remover_livro():
    # Conectar ao banco de dados
    conn = sqlite3.connect('livraria.db')
    cursor = conn.cursor()
    
    # Remover livro
    id_livro = int(input("Digite o ID do livro: "))
    
    cursor.execute("""
    DELETE FROM livros
    WHERE id = ?
    """, (id_livro,))
    
    conn.commit()
    conn.close()

def buscar_livros_por_autor():
    
    autor_pesquisa = input("Digite o nome do autor: ").strip().lower()
    
    conn = sqlite3.connect('livraria.db')
    cursor = conn.cursor()    
    
    cursor.execute("""
    SELECT titulo, autor, preco FROM livros
    WHERE LOWER(autor) LIKE ?
    """, ('%' + autor_pesquisa + '%',))
    
    livros = cursor.fetchall()
    
    if livros:
        for livro in livros:
            print(f"Título: {livro[0]}, Autor: {livro[1]}, Preço: {livro[2]}")
    else:
        print("Nenhum livro encontrado.")
        
    # Fechar conexão5
    conn.close()

def exportar_dados_para_csv():
    # Conectar ao banco de dados
    conn = sqlite3.connect('livraria.db')
    cursor = conn.cursor()
    
    # Selecionar todos os registros da tabela
    cursor.execute("SELECT * FROM livros")
    livros = cursor.fetchall()
    
    # Exportar dados para CSV
    with open('livros.csv', 'w') as arquivo:
        for livro in livros:
            arquivo.write(f"{livro[0]},{livro[1]},{livro[2]},{livro[3]}\n")
    
    print("Dados exportados com sucesso.")
    conn.close()

def importar_dados_de_csv():
    caminho_csv = input("Digite o caminho do arquivo CSV: ")
    
    # Abrir o arquivo CSV e ler os dados
    with open(caminho_csv, newline='') as csvfile:
        leitor_csv = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(leitor_csv)  # Pular o cabeçalho
        
        # Conectar ao banco de dados
        conn = sqlite3.connect('livraria.db')
        cursor = conn.cursor()
        
        # Inserir os dados na tabela
        for linha in leitor_csv:
            if len(linha) >= 4:
                id, titulo, autor, preco = linha[:4]
                try:
                    preco = float(preco)
                    cursor.execute("""
                    INSERT INTO livros (titulo, autor, preco)
                    VALUES (?, ?, ?)
                    """, (titulo, autor, preco))
                except ValueError:
                    print(f"Preço inválido para o livro '{titulo}': {preco}")
            else:
                print(f"Linha inválida: {linha}")
        
        # Confirmar a transação
        conn.commit()
        
        print("Dados importados com sucesso!")
        
        # Fechar conexão
        conn.close()

while True:
    print()
    print('*** Livraria ***')
    print()
    print('1 - Adicionar novo livro')
    print('2 - Exibir todos os livros')
    print('3 - Atualizar preço de um livro')
    print('4 - Remover um livro')
    print('5 - Buscar livros por autor')
    print('6 - Exportar dados para CSV')
    print('7 - Importar dados de CSV')
    print('8 - Fazer backup do banco de dados')
    print('9 - Sair')
    print()

    opcao = input('Escolha uma opção: ')
    print()

    if opcao == '1':
        adicionar_livro()
    elif opcao == '2':
        exibir_todos_livros()
    elif opcao == '3':
        atualizar_preco_livro()
    elif opcao == '4':
        remover_livro()
    elif opcao == '5':
        buscar_livros_por_autor()
    elif opcao == '6':
        exportar_dados_para_csv()
    elif opcao == '7':
        importar_dados_de_csv()
    elif opcao == '8':
        print('Fazer backup do banco de dados')
    elif opcao == '9':
        print('Sair')
        break
    else:
        print('Opção inválida')