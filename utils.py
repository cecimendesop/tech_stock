from models import Produto, db_session, Categoria, Movimentacao, Funcionario
from sqlalchemy import select


def inserir_produto():
    produto = Produto(nome=str(input('Nome: ')),
                      preco=float(input('Preço do produto: ')),
                      descricao=str(input('Descrição do produto: ')),
                      data_fabricacao=str(input('Data de fabricação do produto: ')),
                      quantidade=int(input('Quantidade do produto: ')),
                      versao_produto=str(input('Versão do produto: ')),
                      garantia_produto=str(input('Garantia do produto: ')),
                      desconto_produto=int(input('Desconto do produto: ')),
                      id_categoria_produto=int(input('Insira a Categoria do Produto: '))
                      )

    print(produto)
    produto.save()


def consulta_produto():
    var_produto = select(Produto)
    var_produto = db_session.execute(var_produto).all()
    print(var_produto)


def atualizar_produto():
    var_produto = select(Produto).where(str(input('Nome: ')) == Produto.nome)
    var_produto = db_session.execute(var_produto).scalar()
    print(var_produto)
    var_produto.nome = str(input('Novo Nome: '))
    var_produto.save()


def deletar_produto():
    produto_deletar = input('Qual produto deseja deletar? ')
    var_produto = select(Produto).where(produto_deletar == Produto.nome)
    var_produto = db_session.execute(var_produto).scalar()
    var_produto.delete()


def inserir_categoria():
    categoria = Categoria(nome=str(input('Categoria: ')))

    print(categoria)
    categoria.save()


def consulta_categoria():
    var_categoria = select(Categoria)
    var_categoria = db_session.execute(var_categoria).all()
    print(var_categoria)


def atualizar_categoria():
    var_categoria = select(Categoria).where(str(input('Nome Categoria: ')) == Categoria.nome)
    var_categoria = db_session.execute(var_categoria).scalar()
    print(var_categoria)
    var_categoria.nome = str(input('Nova Categoria: '))
    var_categoria.save()


def deletar_categoria():
    categoria_deletar = input('Qual Categoria Deseja Deletar? ')
    var_categoria = select(Categoria).where(categoria_deletar == Categoria.nome)
    var_categoria = db_session.execute(var_categoria).scalar()
    print(var_categoria)
    var_categoria.delete()


def inserir_movimentacao():
    movimentacao = Movimentacao(status=str(input('Status: ')),
                                local_armazenado=str(input('Local armazenado: ')),
                                data_atualizacao=str(input('Data atualizada: ')),
                                id_produto=int(input('ID Produto: ')),
                                id_funcionario=int(input('ID Funcionário: '))
                                )

    print(movimentacao)
    movimentacao.save()


def consulta_movimentacao():
    var_movimentacao = select(Movimentacao)
    var_movimentacao = db_session.execute(var_movimentacao).all()
    print(var_movimentacao)


def atualizar_movimentacao():
    var_movimentacao = select(Movimentacao).where(str(input('Atual Entrada ou Saída?: ')) == Movimentacao.status)
    var_movimentacao = db_session.execute(var_movimentacao).scalar()
    print(var_movimentacao)
    var_movimentacao.nome = str(input('Atualizar para Entrada ou Saída?: '))
    var_movimentacao.save()


def deletar_movimentacao():
    movimentacao_deletar = input('Qual movimentação deseja deletar?')
    var_movimentacao = select(Movimentacao).where(movimentacao_deletar == Movimentacao.status)
    var_movimentacao = db_session.execute(var_movimentacao).scalar()
    var_movimentacao.delete()


def inserir_funcionario():
    funcionario = Funcionario(nome=str(input('Nome: ')),
                              email=str(input('Email: ')),
                              telefone=int(input('Telefone: ')),
                              cpf=str(input('CPF: ')),
                              data_registro=str(input('Data de Registro: ')),
                              )

    print(funcionario)
    funcionario.save()


def consulta_funcionario():
    var_funcionario = select(Funcionario)
    var_funcionario = db_session.execute(var_funcionario).all()
    print(var_funcionario)


def atualizar_funcionario():
    var_funcionario = select(Funcionario).where(str(input('Nome: ')) == Funcionario.nome)
    var_funcionario = db_session.execute(var_funcionario).scalar()
    print(var_funcionario)
    var_funcionario.nome = str(input('Novo Nome: '))
    var_funcionario.save()


def deletar_funcionario():
    funcionario_deletar = int(input('Qual Funcionário deseja Deletar? (ID): '))
    var_funcionario = select(Funcionario).where(funcionario_deletar == Funcionario.id_funcionario)
    var_funcionario = db_session.execute(var_funcionario).scalar()
    var_funcionario.delete()


if __name__ == '__main__':

    while True:
        print('Menu')
        print('1 - inserir produto')
        print('2 - consultar produto')
        print('3 - atualizar produto')
        print('4 - deletar produto')
        print('5 - inserir categoria ')
        print('6 - consultar categoria')
        print('7 - atualizar categoria')
        print('8 - deletar categoria')
        print('9 - inserir movimentacao')
        print('10 - consultar movimentacao')
        print('11 - atualizar movimentacao')
        print('12 - deletar movimentacao')
        print('13 - inserir funcionario')
        print('14 - consultar funcionario')
        print('15 - atualizar funcionario')
        print('16 - deletar funcionario')
        escolha = input('Escolha: ')

        if escolha == '1':
            inserir_produto()
        elif escolha == '2':
            consulta_produto()
        elif escolha == '3':
            atualizar_produto()
        elif escolha == '4':
            deletar_produto()
        elif escolha == '5':
            inserir_categoria()
        elif escolha == '6':
            consulta_categoria()
        elif escolha == '7':
            atualizar_categoria()
        elif escolha == '8':
            deletar_categoria()
        elif escolha == '9':
            inserir_movimentacao()
        elif escolha == '10':
            consulta_movimentacao()
        elif escolha == '11':
            atualizar_movimentacao()
        elif escolha == '12':
            deletar_movimentacao()
        elif escolha == '13':
            inserir_funcionario()
        elif escolha == '14':
            consulta_funcionario()
        elif escolha == '15':
            atualizar_funcionario()
        elif escolha == '16':
            deletar_funcionario()
