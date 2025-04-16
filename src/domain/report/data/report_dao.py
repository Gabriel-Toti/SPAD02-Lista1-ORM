from datetime import date
from database.database_drive import database
from utils.errors.not_found_exception import NotFoundException
from domain.models import Orders, OrderDetails, Products, Customers, Employees
from sqlalchemy import func
class ReportDataAccess():
    def __init__(self):
        pass

    @staticmethod
    def order_report(order_id: int):

        report = {
            "order_id": None,
            "order_date": None,
            "company_name": None,
            "employee_name": None,
            "products": []
        }

        session = database()
        report_data = session.query(Orders).filter(Orders.orderid == order_id).first()
        

        if report_data == None:
                    raise NotFoundException(f"Pedido com id {order_id} não encontrado.")

        report["order_id"] = report_data.orderid
        report["order_date"] = report_data.orderdate.strftime("%d/%m/%Y")
        report["company_name"] = report_data.customers.companyname
        report["employee_name"] = f"{report_data.employees.firstname} {report_data.employees.lastname}"
        
        products_data = []

        for details in report_data.order_details:
            products_data.append((details.products.productname, details.quantity, f"{(details.quantity * details.products.unitprice):.2f}"))
        
        report["products"] = products_data

        session.close()

        return report
    
    @staticmethod
    def employees_report(inital_date: date, final_date: date):
        report = []

        session = database()
        report_data = session.query(Employees.firstname, Employees.lastname,
                                     func.sum(OrderDetails.quantity),
                                     func.sum(OrderDetails.quantity * OrderDetails.unitprice)
                                    ).join(Orders, Orders.employeeid == Employees.employeeid
                                    ).join(OrderDetails, OrderDetails.orderid == Orders.orderid
                                    ).filter(Orders.orderdate.between(inital_date, final_date)
                                    ).group_by(Employees.employeeid
                                    ).order_by(func.sum(OrderDetails.quantity * OrderDetails.unitprice).desc()).all()
        
        if len(report_data) == 0:
            raise NotFoundException(f"Nenhum pedido encontrado no intervalo '{inital_date}' - '{final_date}'.")

        for data in report_data:
            report.append((f"{data[0]} {data[1]}", data[2], f"R${data[3]:,.2f}"))

        session.close()
        return report
                
                
