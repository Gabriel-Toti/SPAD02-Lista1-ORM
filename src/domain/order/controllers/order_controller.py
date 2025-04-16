from ..data.order_dao import OrderDataAccess
from ..data.order_details_dao import OrderDetailsDataAccess
from domain.employees.data.employee_dao import EmployeeDataAccess
from domain.customers.data.customer_dao import CustomerDataAccess
from domain.product.data.product_dao import ProductDataAccess
from ..views import order_view
from domain.models import Orders
from domain.models import OrderDetails
from utils.error_handler import ErrorHandler
from datetime import date, datetime
from database.database_drive import database
from src.utils.errors.out_of_stock_exception import OutOfStockException
from tkinter import END
from ...report.data.report_dao import ReportDataAccess


class OrderController():
    def __init__(self, controller):
        self.controller = controller
        self.list = []

    def registerOrder(self):
        self.orderRegisterView = order_view.registerOrderView(self)

    def consultOrder(self):
        self.orderConsultView = order_view.consultOrderView(self)

#------------------------------------

    def enterRegisterHandler(self, event):
        try:
            
            first_name = self.orderRegisterView.employee_fname.get()
            last_name = self.orderRegisterView.employee_lname.get()
            customer_name = self.orderRegisterView.customer_name.get()
            order_date = self.orderRegisterView.order_date.get()

            if(first_name == '' or last_name == '' or customer_name == '' or order_date == ''):
                raise ValueError('Há campos em branco!')

            try:
                datetime.strptime(order_date, '%Y-%m-%d')
            except ValueError:
                raise ValueError('Data inválida! Use o formato AAAA-MM-DD.')

            if not self.list:
                raise ValueError('Adicione pelo menos um produto!')
            
            self.__create_order(first_name, last_name, customer_name, self.list, order_date)


            self.orderRegisterView.showView('Sucesso', 'Pedido cadastrado!')
            self.orderRegisterView.state.set(0)
            self.list.clear()
            self.clearRegisterHandler(event)
        except Exception as error:
            ErrorHandler.showError(ErrorHandler.catchError(error))

#------------------------------------

    def enterAddHandler(self, event):

        try:
            product_name = self.orderRegisterView.product_name.get().strip()
            quantity = self.orderRegisterView.quantity.get().strip()

            if(product_name == ''):
                raise ValueError("Preencha o nome do produto.")
                
            if (quantity == ''):
                raise ValueError('Preencha a quantidade!')
            
            if not quantity.isdigit() or int(quantity) <= 0:
                raise ValueError("'Quantidade inválida!'")

            self.list.append((product_name, int(quantity)))
            self.orderRegisterView.frameListbox.insert(END, f"Produto: {product_name} | Quantidade: {quantity}")
        except Exception as error:
            ErrorHandler.showError(ErrorHandler.catchError(error))
        finally:
            self.orderRegisterView.product_name.delete(
                0, len(self.orderRegisterView.product_name.get()))
            self.orderRegisterView.quantity.delete(
                0, len(self.orderRegisterView.quantity.get()))

#------------------------------------

    def searchHandler(self, event):
        try:
            order_id = self.orderConsultView.order_id.get()

            if (order_id == ''):
                raise ValueError('Preencha o id!')
            
            if not order_id.isdigit():
                raise ValueError("'Id inválido!'")

            report_data = self.__get_order_report(int(order_id))
            
            if (report_data is not None):
                report = ""
                report += f'Pedido: {report_data["order_id"]}\n'
                report += f'Vendedor: {report_data["employee_name"]}\n'
                report += f'Cliente: {report_data["company_name"]}\n'
                report += f'Data: {report_data["order_date"]}\n'
                report += f'Itens do Pedido: \n'


                self.orderConsultView.table('Dados do Pedido', ['nome', 'quantidade', 'preço total'], report_data['products'], report)
        except Exception as error:
            ErrorHandler.showError(ErrorHandler.catchError(error))
        finally:
            self.orderConsultView.order_id.delete(
                    0, len(self.orderConsultView.order_id.get()))

#------------------------------------

    def clearRegisterHandler(self, event):
        self.orderRegisterView.employee_fname.delete(
            0, len(self.orderRegisterView.employee_fname.get()))
        self.orderRegisterView.employee_lname.delete(
            0, len(self.orderRegisterView.employee_lname.get()))
        self.orderRegisterView.customer_name.delete(
            0, len(self.orderRegisterView.customer_name.get()))
        self.orderRegisterView.order_date.delete(
            0, len(self.orderRegisterView.order_date.get()))
        self.orderRegisterView.product_name.delete(
            0, len(self.orderRegisterView.product_name.get()))
        self.orderRegisterView.quantity.delete(
            0, len(self.orderRegisterView.quantity.get()))
        self.orderRegisterView.state.set(0)
        self.orderRegisterView.frameListbox.delete(0, END)
        

    def clearConsultHandler(self, event):
        self.orderConsultView.order_id.delete(
            0, len(self.orderConsultView.order_id.get()))

#------------------------------------

    def __create_order(self, first_name: str, last_name: str, customer_name: str, products_data: list[tuple[str, int]], order_date: date): # Callback
            session = database()
            try: 
                employee = EmployeeDataAccess.get_employee_by_name(first_name, last_name)
                customer = CustomerDataAccess.get_customer_by_name(customer_name)
                
                products = []
                products_ids = []
                quantities = []

                for name, quantity in products_data:
                    product = ProductDataAccess.get_product_by_name(name) # Produto por produto, porque se um não existir, é mais fácil de indicar qual

                    # Verificação de estoque
                    if(product.unitsinstock < quantity):
                        raise OutOfStockException(f"Não há unidades suficientes de '{product.productname}' para o pedido.")
                    
                    products.append((product, quantity))
                    quantities.append((product.unitsinstock - quantity, product.unitsonorder + quantity))
                    products_ids.append(product.productid)

                order_id = OrderDataAccess.get_last_order_id() + 1 # Gera um id para o produto baseado nos que já existem
                order = Orders(orderid=order_id, customerid=customer.customerid, employeeid=employee.employeeid, orderdate=order_date)
                
                details_list = []
                
                for product in products: # Um details para cada produto
                    order_details = OrderDetails(orderid=order_id, productid=product[0].productid, unitprice=product[0].unitprice, quantity=product[1])
                    details_list.append(order_details)
                    
                
                # Executando tudo em uma mesma transação

                OrderDataAccess.create_order(order, session)

                session.flush()

                OrderDetailsDataAccess.create_many_order_details(details_list, session)
                ProductDataAccess.update_many_products_stock(products_ids, quantities, session)

                session.commit()
                # Fim da transação;

            except Exception as error:
                session.rollback()
                print(error)
                raise error

    def __get_order_report(self, order: int):
        try:
            return ReportDataAccess.order_report(order)
        except Exception as error:
            raise error
    
