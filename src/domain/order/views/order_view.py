from tkinter import messagebox, Frame, Label, Entry, Listbox, IntVar, Checkbutton, Button, Toplevel, END
from tkinter.ttk import Treeview

class registerOrderView(Toplevel):

  def __init__(self, OrderController):
    self.OrderController = OrderController

    Toplevel.__init__(self)
    self.geometry('400x400')
    self.title("Cadastrar Pedido")

    #CAMPOS DE ENTRADAS
    self.frameOrderEmployeeFName = Frame(self)
    self.frameOrderEmployeeFName.pack()
    self.frameOrderEmployeeLName = Frame(self)
    self.frameOrderEmployeeLName.pack()
    self.frameOrderCustomer = Frame(self)
    self.frameOrderCustomer.pack()
    self.frameOrderDate = Frame(self)
    self.frameOrderDate.pack()
    self.frameOrderProduct = Frame(self)
    self.frameOrderProduct.pack()
    self.frameOrderQuantity = Frame(self)
    self.frameOrderQuantity.pack()

    #RÓTULOS DAS ENTRADAS
    self.labelOrderEmployeeFName = Label(self.frameOrderEmployeeFName, text="Nome do Vendedor: ")
    self.labelOrderEmployeeFName.pack(side='left')
    self.labelOrderEmployeeLName = Label(self.frameOrderEmployeeLName, text="Sobrenome do Vendedor: ")
    self.labelOrderEmployeeLName.pack(side='left')
    self.labelOrderCustomer = Label(self.frameOrderCustomer, text="Nome do Cliente: ")
    self.labelOrderCustomer.pack(side='left')
    self.labelOrderDate = Label(self.frameOrderDate, text="Data (YYYY-MM-DD): ")
    self.labelOrderDate.pack(side='left')
    self.labelOrderProduct = Label(self.frameOrderProduct, text="Nome do Produto: ")
    self.labelOrderProduct.pack(side='left')
    self.labelOrderQuantity = Label(self.frameOrderQuantity, text="Quantidade: ")
    self.labelOrderQuantity.pack(side='left')

    #DADOS DE ENTRADAS
    self.employee_fname = Entry(self.frameOrderEmployeeFName, width=20)
    self.employee_fname.pack(side='left')
    self.employee_lname = Entry(self.frameOrderEmployeeLName, width=20)
    self.employee_lname.pack(side='left')
    self.customer_name = Entry(self.frameOrderCustomer, width=20)
    self.customer_name.pack(side='left')
    self.order_date = Entry(self.frameOrderDate, width=20)
    self.order_date.pack(side='left')
    self.product_name = Entry(self.frameOrderProduct, width=20)
    self.product_name.pack(side='left')
    self.quantity = Entry(self.frameOrderQuantity, width=20)
    self.quantity.pack(side='left')

    self.frameListbox = Listbox(self, height=6, width=40)
    self.frameListbox.pack()

    self.frameButton = Frame(self)
    self.frameButton.pack()

    self.buttonSubmit = Button(self.frameButton, text='Cadastrar Pedido')
    self.buttonSubmit.pack(side='left')
    self.buttonSubmit.bind('<Button>', OrderController.enterRegisterHandler)

    self.buttonAdd = Button(self.frameButton, text='Adicionar Produto')
    self.buttonAdd.pack(side='left')
    self.buttonAdd.bind('<Button>', OrderController.enterAddHandler)

  def showView(self, title, msg):
    messagebox.showinfo(title, msg)


#--------------------------------------------------------------
class consultOrderView(Toplevel):

  def __init__(self, OrderController):
    self.OrderController = OrderController

    Toplevel.__init__(self)
    self.geometry('400x200')
    self.title("Consultar Pedido")

    self.frameOrder = Frame(self)
    self.frameOrder.pack()
    self.frameButton = Frame(self)
    self.frameButton.pack()

    self.labelOrderId = Label(self.frameOrder, text="Id do Pedido: ")
    self.labelOrderId.pack(side='left')

    self.order_id = Entry(self.frameOrder, width=20)
    self.order_id.pack(side='left')

    self.buttonSubmit = Button(self.frameButton, text='Consultar')
    self.buttonSubmit.pack(side='left')
    self.buttonSubmit.bind('<Button>', OrderController.searchHandler)

  def table(self, title, columns, rows, message):
    self.__message_view = Toplevel(master=self)
    self.__message_view.title(title)
    messageLabel = Label(self.__message_view, text=message, anchor="w")
    messageLabel.pack(expand=True)
    table = Treeview(self.__message_view, columns=columns, show="headings")
    for col in columns:
      table.heading(col, text=col)
      table.column(col, anchor="center")
    for item in rows:
      table.insert("", END, values=item)
    table.pack(side="top", anchor="w", fill="both", expand=True)
    close_button = Button(self.__message_view, text="Fechar")
    close_button.pack(expand=True)
    close_button.bind('<Button>', lambda event: self.__message_view.destroy())

