from domain.models import OrderDetails
from database.database_drive import database
from sqlalchemy.orm import Session
from utils.logger import logger
class OrderDetailsDataAccess():
    
    def __init__(self):
        pass
    
    @staticmethod
    def create_many_order_details(order_details: list[OrderDetails], session: Session):
        session.bulk_save_objects(order_details)
        logger.log("Detalhes adicionados com sucesso")