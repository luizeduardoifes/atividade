from pydantic import ValidationError
from produtos.produto_repo import PresidiarioRepo
from produtos.produto import Presidiario
from datetime import date

def exibir_menu():
    """Exibe o menu principal de opções no console."""
    print("\n--- Menu de Gerenciamento Carcerário ---")
    print("a) Cadastrar Presidiário")
    print("b) Listar Presidiários")
    print("c) Alterar Presidiário")
    print("d) Excluir Presidiário")
    print("e) Registrar Ponto")
    print("f) Sair")
    print("-----------------------------------------")

def obter_entrada_usuario(mensagem, tipo=str):
    """Solicita uma entrada do usuário, com validação de tipo."""
    while True:
        entrada = input(mensagem)
        try:
            if tipo == float:
                return float(entrada)
            elif tipo == int:
                return int(entrada)
            elif tipo == date:
                return date.fromisoformat(entrada)
            else:
                return entrada.strip()
        except ValueError:
            print(f"Entrada inválida. Por favor, insira um valor do tipo '{tipo.__name__}'.")

def cadastrar_presidiario(repo: PresidiarioRepo):
    """Função para lidar com a opção de cadastrar um novo presidiário."""
    print("\n--- Cadastro de Novo Presidiário ---")
    try:
        nome = obter_entrada_usuario("Nome: ")
        data_nascimento = obter_entrada_usuario("Data de Nascimento (AAAA-MM-DD): ", date)
        crime = obter_entrada_usuario("Crime: ")
        cela = obter_entrada_usuario("Cela: ", int)

        novo_presidiario = Presidiario(nome=nome, data_nascimento=data_nascimento, crime=crime, cela=cela)
        presidiario_id = repo.adicionar(novo_presidiario)

        if presidiario_id:
            print(f"Presidiário '{novo_presidiario.nome}' cadastrado com sucesso! ID: {presidiario_id}")
        else:
            print("Falha ao cadastrar o presidiário.")

    except ValidationError as e:
        print("\nErro de validação ao cadastrar presidiário:")
        for error in e.errors():
            print(f"- Campo '{error['loc'][0]}': {error['msg']}")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado ao cadastrar: {e}")

def listar_presidiarios(repo: PresidiarioRepo):
    """Função para lidar com a opção de listar todos os presidiários."""
    print("\n--- Lista de Presidiários Cadastrados ---")
    presidiarios = repo.obter_todos()

    if presidiarios:
        for presidiario in presidiarios:
            print(f"ID: {presidiario.id}")
            print(f"Nome: {presidiario.nome}")
            print(f"Data de Nascimento: {presidiario.data_nascimento}")
            print(f"Crime: {presidiario.crime}")
            print(f"Cela: {presidiario.cela}")
            print("---")
    else:
        print("Nenhum presidiário cadastrado.")

def alterar_presidiario(repo: PresidiarioRepo):
    """Função para lidar com a opção de alterar um presidiário existente."""
    print("\n--- Alteração de Presidiário ---")
    try:
        presidiario_id = obter_entrada_usuario("ID do presidiário a ser alterado: ", int)
        presidiario_existente = repo.obter(presidiario_id)

        if presidiario_existente:
            print("\nDados atuais do presidiário:")
            print(f"  Nome: {presidiario_existente.nome}")
            print(f"  Data de Nascimento: {presidiario_existente.data_nascimento}")
            print(f"  Crime: {presidiario_existente.crime}")
            print(f"  Cela: {presidiario_existente.cela}")
            print("\nDigite os novos dados (deixe em branco para manter o valor atual):")

            nome = obter_entrada_usuario(f"Novo Nome ({presidiario_existente.nome}): ") or presidiario_existente.nome
            data_nascimento_str = obter_entrada_usuario(f"Nova Data de Nascimento ({presidiario_existente.data_nascimento}): ")
            data_nascimento = date.fromisoformat(data_nascimento_str) if data_nascimento_str else presidiario_existente.data_nascimento
            crime = obter_entrada_usuario(f"Novo Crime ({presidiario_existente.crime}): ") or presidiario_existente.crime
            cela = obter_entrada_usuario(f"Nova Cela ({presidiario_existente.cela}): ", int) or presidiario_existente.cela

            presidiario_atualizado = Presidiario(id=presidiario_existente.id, nome=nome, data_nascimento=data_nascimento, crime=crime, cela=cela)

            if repo.atualizar(presidiario_atualizado):
                print(f"Presidiário ID {presidiario_id} atualizado com sucesso!")
            else:
                print(f"Falha ao atualizar o presidiário ID {presidiario_id}.")

        else:
            print(f"Presidiário com ID {presidiario_id} não encontrado.")

    except ValidationError as e:
        print("\nErro de validação ao alterar presidiário:")
        for error in e.errors():
            print(f"- Campo '{error['loc'][0]}': {error['msg']}")
    except ValueError:
        print("Entrada inválida para ID, data de nascimento ou cela. A alteração foi cancelada.")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado ao alterar: {e}")

def excluir_presidiario(repo: PresidiarioRepo):
    """Função para lidar com a opção de excluir um presidiário."""
    print("\n--- Exclusão de Presidiário ---")
    try:
        presidiario_id = obter_entrada_usuario("ID do presidiário a ser excluído: ", int)

        presidiario = repo.obter(presidiario_id)
        if not presidiario:
            print(f"Presidiário com ID {presidiario_id} não encontrado.")
            return

        confirmacao = input(f"Tem certeza que deseja excluir o presidiário '{presidiario.nome}' (ID: {presidiario_id})? (s/N): ").lower()

        if confirmacao == 's':
            if repo.excluir(presidiario_id):
                print(f"Presidiário ID {presidiario_id} excluído com sucesso.")
            else:
                print(f"Falha ao excluir o presidiário ID {presidiario_id}. Pode já ter sido removido.")
        else:
            print("Exclusão cancelada.")

    except ValueError:
        print("ID inválido. A exclusão foi cancelada.")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado ao excluir: {e}")

def registrar_ponto(repo: PresidiarioRepo):
    """Função para registrar o ponto de um presidiário."""
    print("\n--- Registro de Ponto ---")
    try:
        presidiario_id = obter_entrada_usuario("ID do presidiário: ", int)
        presidiario = repo.obter(presidiario_id)

        if not presidiario:
            print(f"Presidiário com ID {presidiario_id} não encontrado.")
            return

        # Aqui, você pode adicionar a lógica para registrar o ponto do presidiário
        # Isso pode envolver salvar a data e hora do registro em um arquivo ou banco de dados
        print(f"Ponto registrado para o presidiário '{presidiario.nome}' (ID: {presidiario_id})")

    except ValueError:
        print("ID inválido.")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado ao registrar o ponto: {e}")


def main():
    """Função principal que executa o loop do menu interativo."""
    repo = PresidiarioRepo()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").lower().strip()

        if opcao == 'a':
            cadastrar_presidiario(repo)
        elif opcao == 'b':
            listar_presidiarios(repo)
        elif opcao == 'c':
            alterar_presidiario(repo)
        elif opcao == 'd':
            excluir_presidiario(repo)
        elif opcao == 'e':
            registrar_ponto(repo)
        elif opcao == 'f':
            print("Saindo do programa. Até logo!")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()
