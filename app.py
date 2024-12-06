from flask import Flask, render_template, request, redirect, url_for, flash

from models import Produto, Categoria, Funcionario, Movimentacao, db_session
from sqlalchemy import select

import plotly.express as px
import plotly.io as pio


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


@app.route('/')
def index():
    return redirect('/home')


@app.route('/home')
def home():
    return render_template('main.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/Cadastros', methods=['POST', 'GET'])
def cadastros():
    return render_template('cadastros.html')


@app.route('/produtos', methods=["POST", "GET"])
def produtos():
    sql_produtos = select(Produto)
    resultado_produtos = db_session.execute(sql_produtos).scalars()
    lista_produtos = [n.serialize_Produto() for n in resultado_produtos]
    return render_template('produtos.html', lista_produtos=lista_produtos)


@app.route('/cadastro_produto', methods=['POST', 'GET'])
def cadastro_produto():
    if request.method == 'POST':
        if not request.form["form_nome"]:
            flash("Preencher todos os campos", "error")
        else:
            form_evento = Produto(
                id_categoria_produto=int(request.form.get("form_id_categoria_produto")),
                nome=request.form.get("form_nome"),
                preco=float(request.form.get("form_preco")),
                data_fabricacao=request.form.get("form_data_fabricacao"),
                descricao=request.form.get("form_descricao"),
                garantia_produto=request.form.get("form_garantia_produto"),
            )
            print(form_evento)
            form_evento.save()
            db_session.close()
            flash("Produto Criado!", "success")
            return redirect(url_for('produtos'))

    return render_template('cadastro_produto.html')


@app.route('/editar_produto/<int:id_p>', methods=['GET', 'POST'])
def editar_produto(id_p):
    produto = db_session.execute(select(Produto).where(Produto.id_produto == id_p)).scalar()

    if request.method == 'POST':
        produto.nome = request.form['form_nome']
        produto.preco = request.form['form_preco']
        produto.data_fabricacao = request.form['form_data_fabricacao']
        produto.descricao = request.form['form_descricao']
        produto.garantia_produto = request.form['form_garantia_produto']

        db_session.commit()
        return redirect(url_for('produtos'))

    return render_template('editar_produto.html', produto=produto)


@app.route('/categorizacao')
def categorizacao():
    sql_categoria = select(Categoria)
    resultado_categoria = db_session.execute(sql_categoria).scalars().all()
    lista_categoria = [n.serialize_categorizacao() for n in resultado_categoria]
    return render_template("produtos.html", lista_categoria=lista_categoria)


@app.route('/cadastro_funcionario', methods=['POST', 'GET'])
def cadastro_funcionario():
    if request.method == 'POST':
        if not request.form["form_nome"]:
            flash("Preencher todos os campos", "error")
        else:
            user_cpf = select(Funcionario).where(Funcionario.cpf == request.form.get("form_cpf"))
            user_cpf = db_session.execute(user_cpf).scalars().first()

            if not user_cpf:
                form_evento = Funcionario(
                    nome=request.form.get("form_nome"),
                    email=request.form.get("form_email"),
                    senha=request.form.get("form_senha"),
                    telefone=int(request.form.get("form_telefone")),
                    cpf=request.form.get("form_cpf"),
                )
                print(form_evento)
                form_evento.save()
                db_session.close()
                flash("Funcionário Criado!", "success")
                return redirect(url_for('funcionarios'))
            else:
                flash("O CPF já existe", "error")

    return render_template('cadastro_funcionario.html')


@app.route('/funcionarios')
def funcionarios():
    sql_funcionarios = select(Funcionario)
    resultado_funcionarios = db_session.execute(sql_funcionarios).scalars().all()
    lista_funcionarios = [n.serialize_funcionario() for n in resultado_funcionarios]
    return render_template("funcionarios.html", lista_funcionarios=lista_funcionarios)




@app.route('/movimentacao', methods=["POST", "GET"])
def movimentacao():
    if request.method == "POST":
        try:
            # Validação e extração dos dados do formulário
            produto_id = int(request.form.get("form_nome_produto"))
            quantidade = request.form.get("form_quantidade")

            # Se não passar a quantidade, retorna com erro
            if not quantidade:
                flash("Quantidade é obrigatória", "error")
                return redirect(url_for("movimentacao"))

            quantidade = int(quantidade)  # Converte a quantidade para inteiro

            data_atualizacao = request.form.get("form_data_atualizacao")
            status = request.form.get("action")  # Entrada ou Saída
            id_funcionario = int(request.form.get("form_funcionario"))

            # Busca o produto no banco
            produto = db_session.query(Produto).filter_by(id_produto=produto_id).first()

            if not produto:
                flash("Produto não encontrado!", "error")
                return redirect(url_for("movimentacao"))

            # Valida e atualiza a quantidade do produto
            if status == "Entrada":
                produto.quantidade = (produto.quantidade or 0) + quantidade
            elif status == "Saída":
                if produto.quantidade and produto.quantidade >= quantidade:
                    produto.quantidade -= quantidade
                else:
                    flash("Quantidade insuficiente no estoque!", "error")
                    return redirect(url_for("movimentacao"))
            else:
                flash("Status de movimentação inválido!", "error")
                return redirect(url_for("movimentacao"))

            # Cria e registra a movimentação no banco
            nova_movimentacao = Movimentacao(
                id_produto=produto_id,
                id_funcionario=id_funcionario,
                local_armazenado="Local Padrão",  # Alterar caso tenha essa informação no formulário
                data_atualizacao=data_atualizacao,
                status=status,
                quantidade=quantidade  # Garantir que a quantidade seja fornecida
            )
            db_session.add(nova_movimentacao)
            db_session.commit()  # Confirma a transação no banco de dados

            flash("Movimentação registrada com sucesso!", "success")

            # Redireciona para a página de relatórios após a movimentação ser registrada
            return redirect(url_for("relatorio"))

        except (ValueError, TypeError):
            db_session.rollback()  # Desfaz qualquer mudança no banco em caso de erro de valor
            flash("Dados inválidos no formulário!", "error")
        except Exception as e:
            db_session.rollback()  # Desfaz qualquer mudança no banco em caso de erro inesperado
            flash(f"Erro inesperado: {e}", "error")

    # Dados para renderização da página de movimentação
    sql_produtos = select(Produto)
    sql_funcionario = select(Funcionario)
    resultado_produtos = db_session.execute(sql_produtos).scalars().all()
    resultado_funcionario = db_session.execute(sql_funcionario).scalars().all()
    lista_produtos = [n.serialize_Produto() for n in resultado_produtos]
    lista_funcionarios = [n.serialize_funcionario() for n in resultado_funcionario]

    return render_template(
        "movimentacao.html",
        lista_produtos=lista_produtos,
        lista_funcionarios=lista_funcionarios
    )


@app.route('/relatorio')
def relatorio():
    # Consulta as movimentações do banco
    sql_movimentacoes = select(Movimentacao).order_by(Movimentacao.data_atualizacao.desc())
    resultado_movimentacoes = db_session.execute(sql_movimentacoes).scalars().all()

    # Serializa as movimentações para passar ao template
    lista_movimentacoes = [m.serialize_movimentacao() for m in resultado_movimentacoes]

    return render_template("relatorio.html", movimentacoes=lista_movimentacoes)


@app.route('/grafico')
def grafico():
    # Consulta ao banco para pegar nome e quantidade de cada produto (limite de 5)
    valor_produtos = db_session.execute(
        select(Produto.nome, Produto.quantidade).limit(5)  # Limite de 5 produtos
    ).fetchall()

    # Verificando se há produtos retornados pela consulta
    if not valor_produtos:
        return "Nenhum produto encontrado no estoque.", 404

    # Exibindo os dados dos produtos no console para depuração
    print("Produtos encontrados:", valor_produtos)

    # Dados dos produtos conforme sua estrutura
    produto = [
        {"nome": valor_produtos[0][0], "quantidade": valor_produtos[0][1]},
        {"nome": valor_produtos[1][0], "quantidade": valor_produtos[1][1]},
        {"nome": valor_produtos[2][0], "quantidade": valor_produtos[2][1]},
        {"nome": valor_produtos[3][0], "quantidade": valor_produtos[3][1]},
        {"nome": valor_produtos[4][0], "quantidade": valor_produtos[4][1]}
    ]

    # Exibindo a estrutura dos dados organizados
    print("Estrutura dos produtos:", produto)

    # Convertendo os dados para um DataFrame para facilitar o gráfico
    df = px.pd.DataFrame(produto)

    # Criando o gráfico com Plotly Express
    fig = px.bar(
        df,
        x="nome",
        y="quantidade",
        title="Quantidade dos produtos no estoque (Top 5)",
        labels={"quantidade": "Quantidade", "nome": "Produto"},
        color="nome"
    )

    # Adicionando rótulos com os valores das quantidades nas barras

    # Convertendo o gráfico para HTML
    graph_html = fig.to_html(full_html=False)

    # Renderizando o template com o gráfico
    return render_template("grafico.html", graph_html=graph_html)


app.run(debug=True)
