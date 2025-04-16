from database.database_drive import database
from domain.models import Products
from sqlalchemy.orm import Session
from utils.logger import logger
from utils.errors.not_found_exception import NotFoundException

class ProductDataAccess():
    def __init__(self):
        pass

    @staticmethod
    def get_product_by_name(name: str):
        product = None
        session = database()
        product = session.query(Products).filter(Products.productname == name).first()
        session.close()
        
        if product == None:
            raise NotFoundException(f"Produto com nome {name} não encontrado.")

        return product
    
    
    @staticmethod
    def update_many_products_stock(product_id: list[int], amount: list[tuple[int, int]], session: Session):
        session.bulk_update_mappings(Products, [{"productid": id, "unitsinstock": qtd[0], "unitsonorder": qtd[1]} for id, qtd in zip(product_id, amount)])
                