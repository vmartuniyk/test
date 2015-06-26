# -*- coding: utf-8 -*-

from zato.server.service import Service

class ErrorGenerator:

	def __init__(self, errmessage):
		self.message = errmessage

	def getmetatag(self):
		item = {'code':'500', \
		'type':'Internal server error', \
		'message':'{}'.format(self.message)}
		return item


class GetCashboxList(Service):

	class SimpleIO:
		output_optional = ('meta','data')

	def setErrorMessage(self, errmessage):
		err = ErrorGenerator(errmessage)
		self.response.payload.meta = err.getmetatag()
		self.response.payload.data = ''

	def getSoapIface(self):
		try:
			salary = self.outgoing.soap.get('salary')
		except Exception: 
			self.setErrorMessage('Could not find wsdl link to <Salary> project')
			return None

		return salary

	def getCashboxList(self, salary):
		with salary.conn.client() as client:

			try:
				CashboxList = client.service.GetCashboxList()
			except Exception:
				self.setErrorMessage('Could not execute method GetCashboxList() in <Salary> project')
				return None

		return CashboxList

	def validateCashboxList(self, CashboxList):
		if ('Meta' not in CashboxList):
			self.setErrorMessage('Could not find <Meta> tag in <CashboxList>')
			return False

		if ('Data' not in CashboxList):
			self.setErrorMessage('Could not find <Data> tag in <CashboxList>')
			return False

		if ('Cashbox' not in CashboxList['Data']):
			self.setErrorMessage('Could not find <Cashbox> tag in <CashboxList[''Data'']>')
			return False

		return True

	def getOperationCode(self, CashboxList):
		return CashboxList['Meta']['Code']

	def getMetaTag(self, CashboxList):
		return {'code':'{}'.format(CashboxList['Meta']['Code']), \
			'type':'{}'.format(CashboxList['Meta']['ErrorType']), \
			'message':'{}'.format(CashboxList['Meta']['ErrorMessage'].encode('utf-8'))}

	def getDataTag(self, CashboxList):
		data = []
		if not CashboxList['Data']:
			return ""
		for datatag in CashboxList['Data']['Cashbox']:
			item = {'name':'{}'.format(datatag['Name'].encode('utf-8')), 'uid':'{}'.format(datatag['UID'].encode('utf-8'))}
			data.append(item)
		return data

	def handle(self):

		salary = self.getSoapIface()
		if (salary is None):
			return

		CashboxList = self.getCashboxList(salary)
		if (CashboxList is None):
			return

		if (not self.validateCashboxList(CashboxList)):
			return

		if (self.getOperationCode(CashboxList) == 200):
			self.response.payload.meta = self.getMetaTag(CashboxList)
			self.response.payload.data = self.getDataTag(CashboxList)
		else:	
			self.setErrorMessage(CashboxList['Meta']['ErrorMessage'].encode('utf-8'))


class GetOrderList(Service):

	class SimpleIO:
		output_optional = ('meta','data')

	def setErrorMessage(self, errmessage):
		err = ErrorGenerator(errmessage)
		self.response.payload.meta = err.getmetatag()
		self.response.payload.data = ''

	def validateOrderRequest(self):
		if ('partnerid' not in self.request.payload):
			self.setErrorMessage('Could not find request parameter <partnerid>')
			return False
		return True

	def getSoapIface(self):
		try:
			salary = self.outgoing.soap.get('salary')
		except Exception: 
			self.setErrorMessage('Could not find wsdl link to <Salary> project')
			return None

		return salary

	def getOrderList(self, salary, partnerid):
		with salary.conn.client() as client:

			try:
				OrderList = client.service.GetOrderList(partnerid)
			except Exception:
				self.setErrorMessage('Could not execute method GetCashboxList() in <Salary> project')
				return None

		return OrderList

	def getOperationCode(self, OrderList):
		return OrderList['Meta']['Code']

	def getMetaTag(self, OrderList):
		return {'code':'{}'.format(OrderList['Meta']['Code']), \
			'type':'{}'.format(OrderList['Meta']['ErrorType']), \
			'message':'{}'.format(OrderList['Meta']['ErrorMessage'].encode('utf-8'))}

	def getDataTag(self, OrderList):
		data = []
		if not OrderList['Data']:
			return ""
		for datatag in OrderList['Data']['Order']:
			item = {'date':'{}'.format(datatag['Date'].encode('utf-8')), \
			'sum':'{}'.format(datatag['Sum']), \
			'cashbox':'{}'.format(datatag['Cashbox'].encode('utf-8')), \
			'paymentdate':'{}'.format(datatag['PaymentDate'].encode('utf-8')), \
			'orderstatus':'{}'.format(datatag['OrderStatus'].encode('utf-8')), \
			'uid':'{}'.format(datatag['UID'].encode('utf-8')), \
			'ispaid':'{}'.format(datatag['IsPaid'])}
			data.append(item)
		return data

	def handle(self):

		if (not self.validateOrderRequest()):
			return

		salary = self.getSoapIface()
		if (salary is None):
			return

		partnerid = self.request.payload['partnerid']
		OrderList = self.getOrderList(salary, partnerid)

		if (OrderList is None):
			return

		if (self.getOperationCode(OrderList) == 200):
			self.response.payload.meta = self.getMetaTag(OrderList)
			self.response.payload.data = self.getDataTag(OrderList)
		else:	
			self.setErrorMessage(OrderList['Meta']['ErrorMessage'].encode('utf-8'))


class GetSumToPay(Service):

	class SimpleIO:
		output_optional = ('meta','data')

	def setErrorMessage(self, errmessage):
		err = ErrorGenerator(errmessage)
		self.response.payload.meta = err.getmetatag()
		self.response.payload.data = ''

	def validateSumRequest(self):
		if ('partnerid' not in self.request.payload):
			self.setErrorMessage('Couldn''t find request parameter <partnerid>')
			return False
		return True

	def getSoapIface(self):
		try:
			salary = self.outgoing.soap.get('salary')
		except Exception: 
			self.setErrorMessage('Couldn''t find wsdl link to <Salary> project')
			return None

		return salary

	def getSum(self, salary, partnerid):
		with salary.conn.client() as client:

			try:
				sumToPay = client.service.GetSumToBePaid(partnerid)
			except Exception:
				self.setErrorMessage('Couldn''t execute method GetSumToBePaid() in <Salary> project')
				return None

		return sumToPay

	def getMetaTag(self, sumToPay):
		return {'code':'{}'.format(sumToPay['Meta']['Code']), \
			'type':'{}'.format(sumToPay['Meta']['ErrorType']), \
			'message':'{}'.format(sumToPay['Meta']['ErrorMessage'].encode('utf-8'))}

	def getOperationCode(self, sumToPay):
		return sumToPay['Meta']['Code']

	def handle(self):

		if (not self.validateSumRequest()):
			return

		salary = self.getSoapIface()
		if (salary is None):
			return

		partnerid = self.request.payload['partnerid']
		sumToPay = self.getSum(salary, partnerid)

		if (sumToPay is None):
			return

		if (self.getOperationCode(sumToPay) == 200):
			self.response.payload.meta = self.getMetaTag(sumToPay)
			self.response.payload.data = sumToPay['Data']
		else:	
			self.setErrorMessage(OrderList['Meta']['ErrorMessage'].encode('utf-8'))


class CreateOrder(Service):

	class SimpleIO:
		output_optional = ('meta',)

	def setErrorMessage(self, errmessage):
		err = ErrorGenerator(errmessage)
		self.response.payload.meta = err.getmetatag()

	def validateOrderRequest(self):
		if ('partnerid' not in self.request.payload):
			self.setErrorMessage('Could not find request parameter <partnerid>')
			return False

		if ('cashboxuid' not in self.request.payload):
			self.setErrorMessage('Could not find request parameter <cashboxuid>')
			return False

		if ('sum' not in self.request.payload):
			self.setErrorMessage('Could not find request parameter <sum>')
			return False

		if ('date' not in self.request.payload):
			self.setErrorMessage('Could not find request parameter <date>')
			return False

		return True

	def getSoapIface(self):
		try:
			salary = self.outgoing.soap.get('salary')
		except Exception: 
			self.setErrorMessage('Could not find wsdl link to <Salary> project')
			return None

		return salary

	def createOrder(self, salary, partnerid, cashboxuid, sumtopay, date):
		with salary.conn.client() as client:

			try:
				orderMeta = client.service.CreateOrder(partnerid, cashboxuid, sumtopay, date)
			except Exception:
				self.setErrorMessage('Could not execute method CreateOrder() in <Salary> project')
				return None

		return orderMeta

	def getMetaTag(self, orderMeta):
		return {'code':'{}'.format(orderMeta['Meta']['Code']), \
			'type':'{}'.format(orderMeta['Meta']['ErrorType']), \
			'message':'{}'.format(orderMeta['Meta']['ErrorMessage'].encode('utf-8'))}

	def getOperationCode(self, sumToPay):
		return sumToPay['Meta']['Code']

	def handle(self):

		if (not self.validateOrderRequest()):
			return

		salary = self.getSoapIface()
		if (salary is None):
			return

		partnerid = self.request.payload['partnerid']
		cashboxuid = self.request.payload['cashboxuid']
		sumtopay = self.request.payload['sum']
		date = self.request.payload['date']
		orderMeta = self.createOrder(salary, partnerid, cashboxuid, sumtopay, date)

		if (orderMeta is None):
			return

		if (self.getOperationCode(orderMeta) == 200):
			self.response.payload.meta = self.getMetaTag(orderMeta)
		else:	
			self.setErrorMessage(orderMeta['Meta']['ErrorMessage'].encode('utf-8'))


class DeleteOrder(Service):

	class SimpleIO:
		output_optional = ('meta',)

	def setErrorMessage(self, errmessage):
		err = ErrorGenerator(errmessage)
		self.response.payload.meta = err.getmetatag()

	def validateOrderRequest(self):
		if ('uid' not in self.request.payload):
			self.setErrorMessage('Could not find request parameter <uid>')
			return False
		return True

	def getSoapIface(self):
		try:
			salary = self.outgoing.soap.get('salary')
		except Exception: 
			self.setErrorMessage('Could not find wsdl link to <Salary> project')
			return None

		return salary

	def deleteOrder(self, salary, uid):
		with salary.conn.client() as client:
			try:
				orderMeta = client.service.DeleteOrder(uid)
			except Exception:
				self.setErrorMessage('Could not execute method DeleteOrder() in <Salary> project')
				return None

		return orderMeta

	def getMetaTag(self, orderMeta):
		return {'code':'{}'.format(orderMeta['Meta']['Code']), \
			'type':'{}'.format(orderMeta['Meta']['ErrorType']), \
			'message':'{}'.format(orderMeta['Meta']['ErrorMessage'].encode('utf-8'))}

	def getOperationCode(self, orderMeta):
		return orderMeta['Meta']['Code']

	def handle(self):

		if (not self.validateOrderRequest()):
			return

		salary = self.getSoapIface()
		if (salary is None):
			return

		uid = self.request.payload['uid']
		orderMeta = self.deleteOrder(salary, uid)

		if (orderMeta is None):
			return

		if (self.getOperationCode(orderMeta) == 200):
			self.response.payload.meta = self.getMetaTag(orderMeta)
		else:	
			self.setErrorMessage(orderMeta['Meta']['ErrorMessage'].encode('utf-8'))