from sqlalchemy.orm import sessionmaker
from models import db


def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()