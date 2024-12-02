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
app.geometry("550x450")

# Criação dos frames (páginas)
frame_login = ctk.CTkFrame(app)
frame_criar_conta = ctk.CTkFrame(app)
frame_tabela = ctk.CTkFrame(app)

# Função para alternar entre frames
def mostrar_frame(frame):
    frame_login.pack_forget()
    frame_criar_conta.pack_forget()
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
        # Adiciona botão de exclusão
        ctk.CTkButton(frame_tabela, text="Excluir", 
                      command=lambda u=usuario[1]: confirmar_exclusao(u)).grid(row=i, column=2, padx=5, pady=5)

    ctk.CTkButton(frame_tabela, text="Voltar", command=lambda: mostrar_frame(frame_login)).grid(row=len(usuarios)+1, column=0, columnspan=3, pady=10)

def confirmar_exclusao(usuario):
    # Criar uma nova janela (popup) para confirmação
    popup = ctk.CTkToplevel(app)
    popup.title("Confirmar Exclusão")
    popup.geometry("300x150")
    popup.resizable(False, False)
    
    ctk.CTkLabel(popup, text=f"Tem certeza que deseja excluir\n a conta '{usuario}'?", justify="center").pack(pady=20)
    
    # Botão para confirmar a exclusão
    def confirmar():
        excluir_conta(usuario)
        popup.destroy()  # Fechar o popup

    # Botão para cancelar
    def cancelar():
        popup.destroy()

    # Botões de ação
    ctk.CTkButton(popup, text="Sim", command=confirmar, fg_color="red").pack(side="left", padx=20, pady=10)
    ctk.CTkButton(popup, text="Não", command=cancelar).pack(side="right", padx=20, pady=10)

def excluir_conta(usuario):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE usuario = ?", (usuario,))
    conn.commit()
    conn.close()
    ctk.CTkLabel(frame_tabela, text=f"A conta '{usuario}' foi excluída com sucesso!", text_color="green").grid(row=0, column=0, columnspan=3, pady=5)
    carregar_usuarios()  # Atualiza a lista de usuários

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

# Mostrar página inicial
mostrar_frame(frame_login)

# Loop principal
app.mainloop()
