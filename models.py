from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType


db = create_engine("sqlite:///banco.db")

#criar a base do banco de dados
Base = declarative_base()

#criar as classes/tabelas do banco
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True , autoincrement=True)
    name = Column("name", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.name = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin



#Pedido
class Pedidos(Base):
    __tablename__ = "pedidos"

   #STATUS_PEDIDOS = (
    #    ("PENDENTE", "PENDENTE"),
    #    ("CANCELADO", "CANCELADO"),
    #    ("FINALIZADO", "FINALIZADO"),
    #)

    id = Column("id", Integer, primary_key=True , autoincrement=True)
    status = Column("status", String)# pendendte, cancelado, finalizado
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco =Column("preco", Float)
    #itens = 

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.status = status
        self.preco = preco
#ItensPedido
class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column("id", Integer, primary_key=True , autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", Integer)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido

#executa a criação dos metodos do seu banco (cria efetivamente o banco de dados)