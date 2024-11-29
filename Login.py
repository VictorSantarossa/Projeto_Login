import customtkinter as ctk
import sqlite3

# configuração aparência
ctk.set_appearance_mode('dark')

# Criação das funçôes de funcionalidades
def validar_login():
    usuario = campo_usuario.get()
    senha = campo_senha.get()
    
    # verificar se o usuário é Victor e a senha e 123456
    if usuario == 'victor' and senha == '123456':
        resultado_login.configure(text='Login Feito Com Sucesso!', text_color='green')
    else:
        resultado_login.configure(text='Login Incorreto!', text_color='red')

# Criação da janela principal
login = ctk.CTk()
login.title('Sistema De Login')
login.geometry('350x350')

# Criação dos campos

# Label Do Usuário
label_usuario = ctk.CTkLabel(login,text='Usuário:')
label_usuario.pack(pady=10)

# Entry Do Usuário
campo_usuario = ctk.CTkEntry(login,placeholder_text='Digite seu usuário')
campo_usuario.pack(pady=10)

# Label Da Senha
label_senha = ctk.CTkLabel(login,text='Senha:')
label_senha.pack(pady=10)

# Entry Da Senha
campo_senha = ctk.CTkEntry(login,placeholder_text='Digite sua senha', show='*')
campo_senha.pack(pady=10)

# Button Do Login
botao_login = ctk.CTkButton(login,text='Login',command=validar_login)
botao_login.pack(pady=10)

# Campo de Feedback do Login
resultado_login = ctk.CTkLabel(login,text='')
resultado_login.pack(pady=10)

# Inicia o loop da aplicação
login.mainloop()