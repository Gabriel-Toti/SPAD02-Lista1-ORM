from domain.models import Orders
from database.database_drive import database
from utils.logger import logger
from sqlalchemy.orm import Session
from utils.errors.not_found_exception import NotFoundException

class OrderDataAccess():
    def __init__(self):
        pass

    @staticmethod
    def get_last_order_id():
        order_id = None

        session = database()
        response = session.query(Orders.orderid).order_by(Orders.orderid.desc()).first()
        session.close()

        if response == None:
            order_id = 0
        else:
            order_id = response[0]

        return order_id
    
    @staticmethod
    def create_order(order: Orders, session: Session): # depende de outro DAO, então preciso do cursor pra manter dentro de uma mesma transação
        session.add(order)
        logger.log("Order criada com sucesso!")
    
