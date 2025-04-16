from database.database_drive import database
from domain.models import Employees
from utils.errors.not_found_exception import NotFoundException
class EmployeeDataAccess():
    def __init__(self):
        pass

    @staticmethod
    def get_employee_by_name(first_name: str, last_name: str):
        employee = None
        session = database()
        employee = session.query(Employees).filter(Employees.firstname == first_name and Employees.lastname == last_name).first()
        session.close()

        if employee == None:
            raise NotFoundException(f"Funcionario com nome {first_name} {last_name} não encontrado.")
        
        return employee