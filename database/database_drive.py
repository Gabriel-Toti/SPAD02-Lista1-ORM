# Conexão com a base de dados
from psycopg import connect
from psycopg import OperationalError
from dotenv import load_dotenv
from os import getenv
from src.utils.logger import logger
from src.utils.error_handler import ErrorHandler
from psycopg import Connection
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


load_dotenv()

__connection_options = {
    "host":getenv("DATABASE_HOST", "localhost"),
    "dbname":"northwind",
    "user":getenv("DATABASE_USER", "postgres"),
    "password":getenv("DATABASE_PASSWORD", "postgres")
}

__northwind = create_engine(f"postgresql+psycopg://{__connection_options['user']}:{__connection_options['password']}@{__connection_options['host']}/{__connection_options['dbname']}")

def database(engine=__northwind) -> Session:
    logger.log(f"Tentando criar sessão em {__connection_options['host']} com {__connection_options['dbname']}...")
    try:

        LocalSession = sessionmaker(bind=engine)
        logger.log("Sessão criada com sucesso!")
        return LocalSession()
    except OperationalError as error:
        errorHandler = ErrorHandler()
        errorHandler.showError(errorHandler.catchError(error))
        return None