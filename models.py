from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, relationship

# PrimaryKeyConstraint significa um valores unicos e na nulos, exclusivo de cada registro na tabela
engine = create_engine('sqlite:///techstock.sqlite3')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Produto(Base):
    query = None
    __tablename__ = 'produtos'
    id_produto = Column(Integer, primary_key=True)
    nome = Column(String(40), nullable=False, index=True)
    preco = Column(Float(20), nullable=False, index=True)
    data_fabricacao = Column(String(255), nullable=False, index=True)
    descricao = Column(String(255), nullable=False, index=True)
    quantidade = Column(Integer, index=True)
    id_categoria_produto = Column(Integer, ForeignKey('categorias.id_categoria'), nullable=False, index=True)
    categoria = relationship('Categoria')  #
    versao_produto = Column(String(255), index=True)
    garantia_produto = Column(String(255), index=True)
    desconto_produto = Column(Integer, index=True)

    movimentacoes = relationship('Movimentacao', back_populates="produto")

    def __repr__(self):
        return '<Produto:  {} {} {} {} {} {} {}>'.format(self.nome, self.preco, self.descricao, self.data_fabricacao,
                                                         self.versao_produto, self.garantia_produto,
                                                         self.desconto_produto, self.quantidade)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_Produto(self):
        dados_produtos = {
            "id_produto": self.id_produto,
            "nome": self.nome,
            "preco": self.preco,
            "data_fabricacao": self.data_fabricacao,
            "descricao": self.descricao,
            "id_categoria_produto": self.id_categoria_produto,
            "categoria_produto": self.categoria,
            "quantidade": self.quantidade,
            "versao_produto": self.versao_produto,
            "garantia_produto": self.garantia_produto,
            "desconto_produto": self.desconto_produto,

        }
        return dados_produtos


class Categoria(Base):
    __tablename__ = 'categorias'
    id_categoria = Column(Integer, primary_key=True)
    nome = Column(String(80))

    def __repr__(self):
        return '<Produto: {}>'.format(self.nome, )

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_categorizacao(self):
        dados_categoria = {
            "id_categoria": self.id_categoria,
            "nome": self.nome,
        }
        return dados_categoria


class Movimentacao(Base):
    __tablename__ = 'movimentacoes'
    id_movimentacao = Column(Integer, primary_key=True)
    local_armazenado = Column(String(255), nullable=False)
    data_atualizacao = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False)
    quantidade = Column(Integer, nullable=False)
    id_produto = Column(Integer, ForeignKey('produtos.id_produto'), nullable=False)
    id_funcionario = Column(Integer, ForeignKey('funcionarios.id_funcionario'), nullable=False)

    # Relacionamentos
    produto = relationship('Produto', back_populates="movimentacoes")
    funcionario = relationship('Funcionario', back_populates="movimentacoes")

    def __repr__(self):
        return f"<Movimentacao(id={self.id_movimentacao}, produto={self.produto.nome if self.produto else 'N/A'}, " \
               f"funcionario={self.funcionario.nome if self.funcionario else 'N/A'}, " \
               f"local_armazenado='{self.local_armazenado}', data_atualizacao='{self.data_atualizacao}', status='{self.status}')>"

    def save(self):
        """Salva a movimentação no banco de dados."""
        db_session.add(self)
        db_session.commit()

    def delete(self):
        """Deleta a movimentação do banco de dados."""
        db_session.delete(self)
        db_session.commit()

    def serialize_movimentacao(self):
        """Serializa os dados da movimentação para um formato dicionário."""
        return {
            "id_movimentacao": self.id_movimentacao,
            "produto": {"id": self.id_produto, "nome": self.produto.nome} if self.produto else None,
            "funcionario": {"id": self.id_funcionario, "nome": self.funcionario.nome} if self.funcionario else None,
            "local_armazenado": self.local_armazenado,
            "quantidade": self.quantidade,
            "data_atualizacao": self.data_atualizacao,
            "status": self.status,
        }


class Funcionario(Base):
    __tablename__ = 'funcionarios'
    id_funcionario = Column(Integer, primary_key=True)
    nome = Column(String(255))
    email = Column(String(255), unique=True, nullable=False)
    senha = Column(String(150), unique=True)
    telefone = Column(Integer, unique=True, nullable=False)
    status_funcionario = Column(String(255))
    cpf = Column(String(255), unique=True, nullable=False)
    data_registro = Column(String(255))

    movimentacoes = relationship('Movimentacao', back_populates="funcionario")

    def __repr__(self):
        return '<funcionario: {} {} {} {}>'.format(self.nome, self.email, self.telefone, self.cpf)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_funcionario(self):
        dados_funcionario = {
            "id_funcionario": self.id_funcionario,
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
            "telefone": self.telefone,
            "status": self.status_funcionario,
            "cpf": self.cpf,
            "data_registro": self.data_registro,
        }
        return dados_funcionario


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
