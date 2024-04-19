import tkinter as tk
from tkinter import ttk
import sqlite3

conn = sqlite3.connect('escola.db')  # Conexão com o banco de dados SQLite
cursor = conn.cursor()


def criar_tabelas():
  cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos
        (id INTEGER PRIMARY KEY, nome TEXT, idade INTEGER, cidade TEXT)
        ''')

  cursor.execute('''
        CREATE TABLE IF NOT EXISTS professores
        (id INTEGER PRIMARY KEY, nome TEXT, idade INTEGER, disciplina TEXT)
        ''')

  cursor.execute('''
        CREATE TABLE IF NOT EXISTS disciplinas
        (id INTEGER PRIMARY KEY, nome TEXT, turno TEXT)
        ''')


criar_tabelas()  # Chamar a função para criar as tabelas


def salvar_dados(categoria, dados):
  if categoria == "alunos":
    cursor.execute("INSERT INTO alunos (nome, idade, cidade) VALUES (?, ?, ?)",
                   dados)
  elif categoria == "professores":
    cursor.execute(
        "INSERT INTO professores (nome, idade, disciplina) VALUES (?, ?, ?)",
        dados)
  elif categoria == "disciplinas":
    cursor.execute("INSERT INTO disciplinas (nome, turno) VALUES (?, ?)",
                   dados)

  conn.commit()
  print(f"Dados de {categoria} salvos com sucesso:", dados)


def consultar_dados(categoria):
  consulta_janela = tk.Toplevel(root)
  consulta_janela.title(f"Consulta de {categoria.capitalize()}")

  # Consulta os dados do banco de dados
  cursor.execute(f"SELECT * FROM {categoria}")
  dados = cursor.fetchall()

  # Cria um widget Treeview para exibir os dados em uma tabela
  tree = ttk.Treeview(consulta_janela,
                      columns=[str(i) for i in range(len(cursor.description))],
                      show="headings")

  # Configura os cabeçalhos da tabela com os nomes das colunas
  for i, desc in enumerate(cursor.description):
    tree.heading(str(i), text=desc[0])

  # Configura a largura das colunas
  for i, desc in enumerate(cursor.description):
    if desc[0] == "id":
      tree.column(str(i),
                  width=30)  # Definindo largura menor para o campo "id"
    else:
      tree.column(
          str(i), width=70
      )  # Definindo largura padrão para os demais                                                campos

    tree.heading(str(i), text=desc[0])

  # Insere os dados na tabela
  for row in dados:
    tree.insert("", "end", values=row)

  tree.pack(expand=True, fill="both")


root = tk.Tk()
root.title("Sistema de Gestão Escolar")

# Definindo a geometria da janela principal
largura_janela = 500
altura_janela = 500

largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()

pos_x = (largura_tela // 2) - (largura_janela // 2)
pos_y = (altura_tela // 2) - (altura_janela // 2)

root.geometry('{}x{}+{}+{}'.format(largura_janela, altura_janela, pos_x,
                                   pos_y))


def nova_janela(categoria, atributos):
  nova_janela = tk.Toplevel(root)
  nova_janela.title(f"Cadastro de {categoria.capitalize()}")

  # Definindo a geometria da nova janela
  largura_janela_categoria = 500
  altura_janela_categoria = 500
  nova_janela.geometry('{}x{}'.format(largura_janela_categoria,
                                      altura_janela_categoria))

  campos = []
  for i, atributo in enumerate(atributos):
    label = tk.Label(nova_janela, text=f"{atributo.capitalize()}:")
    label.grid(row=i, column=0, padx=10, pady=5)
    entry = tk.Entry(nova_janela, width=30)
    entry.grid(row=i, column=1, padx=10, pady=5)
    campos.append(entry)

  salvar_button = tk.Button(nova_janela,
                            text="Salvar",
                            command=lambda: salvar_dados(
                                categoria, [campo.get() for campo in campos]),
                            width=20)
  salvar_button.grid(row=len(atributos), columnspan=2, padx=10, pady=10)


# Botão para consultar os dados
def botao_consulta(categoria):
  return tk.Button(root,
                   text=f"Consultar {categoria.capitalize()}",
                   command=lambda: consultar_dados(categoria),
                   width=20,
                   height=2,
                   font=("Arial", 12))


alunos_button = tk.Button(
    root,
    text="Alunos",
    command=lambda: nova_janela("alunos", ["nome", "idade", "cidade"]),
    width=20,
    height=2,
    font=("Arial", 12))
alunos_button.pack(pady=10)

professores_button = tk.Button(
    root,
    text="Professores",
    command=lambda: nova_janela("professores", ["nome", "idade", "disciplina"]
                                ),
    width=20,
    height=2,
    font=("Arial", 12))
professores_button.pack(pady=10)

disciplinas_button = tk.Button(
    root,
    text="Disciplinas",
    command=lambda: nova_janela("disciplinas", ["nome", "turno"]),
    width=20,
    height=2,
    font=("Arial", 12))
disciplinas_button.pack(pady=10)

# Adicionando botões de consulta para cada categoria
alunos_consulta_button = botao_consulta("alunos")
alunos_consulta_button.pack(pady=10)

professores_consulta_button = botao_consulta("professores")
professores_consulta_button.pack(pady=10)

disciplinas_consulta_button = botao_consulta("disciplinas")
disciplinas_consulta_button.pack(pady=10)

root.mainloop()
