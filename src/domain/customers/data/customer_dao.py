from database.database_drive import database
from domain.models import Customers
from utils.errors.not_found_exception import NotFoundException

class CustomerDataAccess():
    def __init__(self):
        pass

    @staticmethod
    def get_customer_by_name(name: str):
        customer = None

        session = database()
        customer = session.query(Customers).filter(Customers.companyname == name).first()
        session.close()

        if customer == None:
            raise NotFoundException(f"Cliente com nome {name} não encontrado.")

        return customer
