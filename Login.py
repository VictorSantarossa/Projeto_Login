import customtkinter as ctk
import sqlite3
import hashlib

# Configuração inicial
ctk.set_appearance_mode("dark")

# Configuração do banco de dados SQLite
def configurar_banco():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Função para criar hash da senha
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Janela principal
configurar_banco()
app = ctk.CTk()
app.title("Sistema de Login")
app.geometry("350x450")

# Criação dos frames (páginas)
frame_login = ctk.CTkFrame(app)
frame_criar_conta = ctk.CTkFrame(app)
frame_excluir_conta = ctk.CTkFrame(app)
frame_tabela = ctk.CTkFrame(app)

# Função para alternar entre frames
def mostrar_frame(frame):
    frame_login.pack_forget()
    frame_criar_conta.pack_forget()
    frame_excluir_conta.pack_forget()
    frame_tabela.pack_forget()
    frame.pack(fill="both", expand=True)

# Funções de cada página
def validar_login():
    usuario = campo_usuario.get()
    senha = campo_senha.get()
    
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    senha_hashed = hash_senha(senha)
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha_hashed))
    usuario_encontrado = cursor.fetchone()
    conn.close()
    
    if usuario_encontrado:
        resultado_login.configure(text="Login Feito Com Sucesso!", text_color="green")
    else:
        resultado_login.configure(text="Login Incorreto!", text_color="red")

def criar_conta():
    novo_usuario = campo_novo_usuario.get()
    nova_senha = campo_nova_senha.get()
    confirmar_senha = campo_confirmar_senha.get()

    if not novo_usuario or not nova_senha or not confirmar_senha:
        resultado_criar_conta.configure(text="Todos os campos são obrigatórios!", text_color="red")
        return

    if nova_senha != confirmar_senha:
        resultado_criar_conta.configure(text="As senhas não coincidem!", text_color="red")
        return

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    senha_hashed = hash_senha(nova_senha)

    try:
        cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (novo_usuario, senha_hashed))
        conn.commit()
        resultado_criar_conta.configure(text="Conta criada com sucesso!", text_color="green")
    except sqlite3.IntegrityError:
        resultado_criar_conta.configure(text="Usuário já existe!", text_color="red")
    finally:
        conn.close()

def excluir_conta():
    usuario = campo_usuario_excluir.get()
    senha = campo_senha_excluir.get()

    if not usuario or not senha:
        resultado_excluir_conta.configure(text="Todos os campos são obrigatórios!", text_color="red")
        return

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    senha_hashed = hash_senha(senha)
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha_hashed))
    usuario_encontrado = cursor.fetchone()

    if usuario_encontrado:
        cursor.execute("DELETE FROM usuarios WHERE usuario = ?", (usuario,))
        conn.commit()
        resultado_excluir_conta.configure(text="Conta excluída com sucesso!", text_color="green")
    else:
        resultado_excluir_conta.configure(text="Usuário ou senha incorretos!", text_color="red")

    conn.close()

def carregar_usuarios():
    for widget in frame_tabela.winfo_children():
        widget.destroy()

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, usuario FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()

    ctk.CTkLabel(frame_tabela, text="ID", width=50).grid(row=0, column=0, padx=5, pady=5)
    ctk.CTkLabel(frame_tabela, text="Usuário", width=200).grid(row=0, column=1, padx=5, pady=5)

    for i, usuario in enumerate(usuarios, start=1):
        ctk.CTkLabel(frame_tabela, text=str(usuario[0]), width=50).grid(row=i, column=0, padx=5, pady=5)
        ctk.CTkLabel(frame_tabela, text=usuario[1], width=200).grid(row=i, column=1, padx=5, pady=5)

    ctk.CTkButton(frame_tabela, text="Voltar", command=lambda: mostrar_frame(frame_login)).grid(row=len(usuarios)+1, column=0, columnspan=2, pady=10)

# Página de Login
ctk.CTkLabel(frame_login, text="Usuário:").pack(pady=10)
campo_usuario = ctk.CTkEntry(frame_login)
campo_usuario.pack(pady=10)

ctk.CTkLabel(frame_login, text="Senha:").pack(pady=10)
campo_senha = ctk.CTkEntry(frame_login, show="*")
campo_senha.pack(pady=10)

resultado_login = ctk.CTkLabel(frame_login, text="")
resultado_login.pack(pady=10)

ctk.CTkButton(frame_login, text="Login", command=validar_login).pack(pady=10)
ctk.CTkButton(frame_login, text="Criar Conta", command=lambda: mostrar_frame(frame_criar_conta)).pack(pady=10)
ctk.CTkButton(frame_login, text="Excluir Conta", command=lambda: mostrar_frame(frame_excluir_conta)).pack(pady=10)
ctk.CTkButton(frame_login, text="Exibir Usuários", command=lambda: [carregar_usuarios(), mostrar_frame(frame_tabela)]).pack(pady=10)

# Página Criar Conta
ctk.CTkLabel(frame_criar_conta, text="Novo Usuário:").pack(pady=10)
campo_novo_usuario = ctk.CTkEntry(frame_criar_conta)
campo_novo_usuario.pack(pady=10)

ctk.CTkLabel(frame_criar_conta, text="Nova Senha:").pack(pady=10)
campo_nova_senha = ctk.CTkEntry(frame_criar_conta, show="*")
campo_nova_senha.pack(pady=10)

ctk.CTkLabel(frame_criar_conta, text="Confirmar Senha:").pack(pady=10)
campo_confirmar_senha = ctk.CTkEntry(frame_criar_conta, show="*")
campo_confirmar_senha.pack(pady=10)

resultado_criar_conta = ctk.CTkLabel(frame_criar_conta, text="")
resultado_criar_conta.pack(pady=10)

ctk.CTkButton(frame_criar_conta, text="Salvar", command=criar_conta).pack(pady=10)
ctk.CTkButton(frame_criar_conta, text="Voltar", command=lambda: mostrar_frame(frame_login)).pack(pady=10)

# Página Excluir Conta
ctk.CTkLabel(frame_excluir_conta, text="Usuário:").pack(pady=10)
campo_usuario_excluir = ctk.CTkEntry(frame_excluir_conta)
campo_usuario_excluir.pack(pady=10)

ctk.CTkLabel(frame_excluir_conta, text="Senha:").pack(pady=10)
campo_senha_excluir = ctk.CTkEntry(frame_excluir_conta, show="*")
campo_senha_excluir.pack(pady=10)

resultado_excluir_conta = ctk.CTkLabel(frame_excluir_conta, text="")
resultado_excluir_conta.pack(pady=10)

ctk.CTkButton(frame_excluir_conta, text="Excluir", command=excluir_conta).pack(pady=10)
ctk.CTkButton(frame_excluir_conta, text="Voltar", command=lambda: mostrar_frame(frame_login)).pack(pady=10)

# Mostrar página inicial
mostrar_frame(frame_login)

# Loop principal
app.mainloop()
