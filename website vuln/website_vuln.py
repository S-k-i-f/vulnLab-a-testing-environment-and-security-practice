"""
Website Vulnerável

Módulo para a simulação de invasão de um website usando métodos de injeção de banco de dados
em texto puro, página de login sem limmite de tentativas e funções administrativas mal implementadas.

    • Utiliza o módulo getpass para ocultar a senha no terminal e garantir a privacidade do usuário.
    • Utiliza o módulo json para simular um banco de dados real.
"""

import getpass
import json

BANCO_DADOS = "database.json"

def iniciar_banco_dados():
    # Inicialização: Inicia o banco de dados e retorna uma lista vazia se o arquivo estiver vazio ou não existir.

    try:
        with open(BANCO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
        
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_usuarios(lista_usuarios):
    # Adição ao banco: Quando o usuário finaliza o cadastro, seus dados são adicionados à lista de usuários existentes.

    with open(BANCO_DADOS, "w", encoding="utf-8") as f:
        json.dump(lista_usuarios, f, indent=4)

def inspecionar_requisicoes():
    # Payload: Simula a inspeção de requisições para iniciar a invasão.

    print("-" * 71)
    print("                          Inspecionar Requisições")
    print("-" * 71)
    
    usuarios = iniciar_banco_dados()
    if not usuarios:
        print("Nenhum dado capturado nas requisições.")
    else:
        print(json.dumps(usuarios, indent=4))

def pagina_cadastro():
    """
    Interface de cadastro para novos usuários.

        • Criação de um nome de usuário em letras minúsculas com o método "lower".
        • Craição de senha de até 5 caracteres que o culta os dígitos para simplificar a invasão.
        • Verfica o banco de dados e adiciona os dados do novo usuário.
    """

    while True:
        print("-" * 71)
        print("                              Cadastre-se")
        print("-" * 71)

        novo_nome = input("Digite seu nome: ").lower()
        nova_senha = getpass.getpass("Crie uma nova senha (máx 5 caracteres): ")
        confirmar_nova_senha = getpass.getpass("Confirme a senha: ")

        if nova_senha == confirmar_nova_senha:
            print("Senha criada com sucesso!")

        else:
            print("As senhas não considem, tente novamente.")
            continue

        novo_cadastro = f'{{"nome": "{novo_nome}", "senha": "{nova_senha}", "admin": false}}'

        try:
            # Conversão de string: o sistema do site tenta converter a string corretamente em um objeto.
            usuarios = iniciar_banco_dados()
            injecao = json.loads(novo_cadastro)
            
            usuarios.append(injecao)
            salvar_usuarios(usuarios)

            print("Usuário criado com sucesso!")
            break
        
        # Erro de execução: se o atacante errar, o JSON quebra e o sistema cai.
        except Exception:
            print("Erro: O input inserido quebrou a estrutura da requisição.")
            break

def pagina_login():
    """
    Interface para login de usuários.

        • O usuário acessa o site com os dados já existentes no banco de dados.
        • Se os dados estiverem incorretos, o acesso é negado e os dados são solicitados novamente.
    """

    print("-" * 71)
    print("                                 Login")
    print("-" * 71)
    print(" ")
    
    login = input("Digite seu nome de usuário: ").lower()
    senha_login = getpass.getpass("Senha: ")
    
    usuarios = iniciar_banco_dados()  
    logado = False

    for u in usuarios:

        if u["nome"] == login and u["senha"] == senha_login:
            print(f"Bem-vindo de volta {u["nome"]}!")

            # Identifcação: verifica se o usuário tem privilégios de adiminstrador.
            if u.get("admin"):
                print("Acesso de Administrador concedido. Painel de controle liberado.")

            else:
                print("Acesso de usuário comum.")

            logado = True
            break
            
    if not logado:
        print("Usuário ou senha incorretos.")

def menu_principal():
    """
    Interface de interaçã com o usuário.

          • Loop que carrega as opções.
          • Inicia o cadastro e o login.
    """

    while True:
        print("-" * 71)
        print("                             Bem vindo(a)!")
        print("-" * 71)
        print("O que deseja fazer?")
        print("    1. Cadastre-se.")
        print("    2. Fazer Login.")
        print("    3. Sair.")

        opcao = input("Escolha uma opção (1, 2 ou 3): ").strip()

        if opcao == "1":
            pagina_cadastro()

        elif opcao == "2":
            pagina_login()
        
        elif opcao == "4":
            inspecionar_requisicoes()

        elif opcao == "3":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu_principal()
