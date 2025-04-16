from ..data.report_dao import ReportDataAccess
from ..views import report_view
from datetime import datetime
from utils.error_handler import ErrorHandler

class ReportController():

  def __init__(self, controller):
    self.controller = controller
    self.list = []

  def consultReport(self):
    self.reportConsultView = report_view.consultReportView(self)

#-------------------

  def searchHandler(self, event):
    try:
      start_date = self.reportConsultView.start_date.get()
      end_date = self.reportConsultView.end_date.get()

      if(start_date == '' or end_date == ''):
        raise ValueError('Há campos em branco!')

      try:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
      except ValueError:
        raise ValueError('Data inválida! Use o formato AAAA-MM-DD.')

      if start > end:
        raise ValueError('Data inicial maior que a data final!')

      self.list = self.takeList(start, end)
      
      self.reportConsultView.table('Relatório de Ranking', ['nome', 'total de produtos', 'valor vendido'], self.list, "Ranking de funcionários")
    except Exception as error:
      ErrorHandler.showError(ErrorHandler.catchError(error))
    finally:
      self.clearHandler()


#-------------------

  def clearHandler(self):
    self.reportConsultView.start_date.delete(
        0, len(self.reportConsultView.start_date.get()))
    self.reportConsultView.end_date.delete(
        0, len(self.reportConsultView.end_date.get()))

#-------------------

  def takeList(self, start: str, end: str):
    try:
      return ReportDataAccess.employees_report(start, end)
    except Exception as error:
      raise error
    
