# -*- coding: utf-8
from browser import Browser
import json, time
from datetime import datetime

class PKUVenue():
	def __init__(self, config):
		self.username = config["username"]
		self.password = config["password"]
		self.phone = config["phone"]
		self.orderStatement = []
		self.browser = Browser()

	def login(self):
		self.browser.gotoPage("https://epe.pku.edu.cn/ggtypt/login?service=https://epe.pku.edu.cn/venue-server/loginto")
		print("trying to login ......")
		self.browser.typeByCssSelector("#user_name", self.username)
		self.browser.typeByCssSelector("#password", self.password)
		self.browser.clickByCssSelector("#logon_button")
		self.browser.findElementByCssSelector("body > div.fullHeight > div > div > div.isLogin > div > div.loginUser")
		print("login success !!!!")

	def _reqListToDict(self, reqList):
		reqDict = {}
		for req in reqList:
			orderDate = req.split(" ")[0]
			orderTime = req.split(" ")[1]
			if orderDate in reqDict.keys():
				reqDict[orderDate].append(orderTime)
			else:
				reqDict[orderDate] = [orderTime]
		return reqDict

	def __jumpToDate(self, orderDate):
		print("selecting date %s" % orderDate)
		today = datetime.now()
		orderDatetime = datetime.strptime(orderDate, "%Y-%m-%d")
		dayDelta = (orderDatetime - today).days + 1
		for i in range(0, dayDelta):
			self.browser.clickByXPath("/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/form/div/div/button[2]/i")

	def __submitOrder(self):
		print("read & agree ✅!!!!")
		self.browser.clickByXPath("/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[4]/label/span/input")

		print("click to make order......")
		self.browser.clickByXPath("/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[5]/div/div[2]")

		print("submiting order ....... ")
		self.browser.typeByXPath("/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/form/div/div[4]/div/div/div/div/input", self.phone)
		# self.browser.clickByXPath("/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div/div/div[2]")

	def __makeOrder(self, sportsName, timeList, courtList, orderDate, orderTimeList):
		orderEnable = False
		for ot in orderTimeList:
			print("selecting time %s ........." % ot)
			timeTableRow = timeList.index(ot)+1
			courtSelected = False
			for page in range(0, len(courtList)):
				# waiting for the table to show up
				self.browser.findElementByXPath("/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[3]/div[1]/div/div/div/div/div/table/tbody/tr[15]/td[1]/div")
				for courtTablecolumn in range(2, len(courtList[page])+2):
					courtBlockElment = self.browser.findElementByXPath("/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[3]/div[1]/div/div/div/div/div/table/tbody/tr[%d]/td[%d]/div" % (timeTableRow, courtTablecolumn))
					if "free" in courtBlockElment.get_attribute('class'):
						courtBlockElment.click()
						courtSelected = True
						self.orderStatement.append("%s %s %s %s" % (sportsName, orderDate, ot, courtList[page][courtTablecolumn-2]))
						print("selected %s %s %s" % (orderDate, ot, courtList[page][courtTablecolumn-2]))
						break
				if courtSelected:
					break
				if page < len(courtList)-1:
					self.browser.clickByXPath("/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[3]/div[1]/div/div/div/div/div/table/thead/tr/td[6]/div/span/i")
			if not courtSelected:
				self.orderStatement.append("%s %s %s %s" % (sportsName, orderDate, ot, "无场"))
				print("without court left at %s %s" % (orderDate, ot))
			else:
				orderEnable = True
					
		return orderEnable

	def _order(self, sportsName, venueUrl, timeList, courtList, orderDate, orderTimeList):
		self.browser.gotoPage(venueUrl)
		self.__jumpToDate(orderDate)
		if self.__makeOrder(sportsName, timeList, courtList, orderDate, orderTimeList):
			self.__submitOrder()

	def orderBadmintonOnce(self, orderDate, orderTimeList):
		timeList = ["8:00-9:00","9:00-10:00","10:00-11:00","11:00-12:00","12:00-13:00","13:00-14:00","14:00-15:00","15:00-16:00","16:00-17:00","17:00-18:00","18:00-19:00","19:00-20:00","20:00-21:00","21:00-22:00"]
		courtList = [["1号", "2号", "3号", "4号", "5号"], ["6号", "7号", "8号", "9号", "10号"], ["11号", "12号"]]
		self._order("羽毛球", "https://epe.pku.edu.cn/venue/pku/venue-reservation/60", timeList, courtList, orderDate, orderTimeList)

	def orderBadminton(self, reqList):
		reqDict = self._reqListToDict(reqList)
		for orderDate in reqDict:
			for i in range(0, len(reqDict[orderDate]), 2):
				self.orderBadmintonOnce(orderDate, reqDict[orderDate][i:i+2])

	def orderBasketballOnce(self, orderDate, orderTimeList):
		timeList = ["8:00-9:00","9:00-10:00","10:00-11:00","11:00-12:00","12:00-13:00","13:00-14:00","14:00-15:00","15:00-16:00","16:00-17:00","17:00-18:00","18:00-19:00","19:00-20:00","20:00-21:00","21:00-22:00"]
		courtList = [["北1", "南1", "北2", "南2"]]
		self._order("篮球", "https://epe.pku.edu.cn/venue/pku/venue-reservation/68", timeList, courtList, orderDate, orderTimeList)


	def orderBasketball(self, reqList):
		reqDict = self._reqListToDict(reqList)
		for orderDate in reqDict:
			for i in range(0, len(reqDict[orderDate]), 2):
				self.orderBasketballOnce(orderDate, reqDict[orderDate][i:i+2])

	def outputOrderStatement(self):
		for i in range(0, len(self.orderStatement)):
			print("{:^52}".format(" " + "-" * 50 + " "))
			print("| " + "{:^48}".format(self.orderStatement[i]) + " |")
			print("{:^52}".format(" " + "-" * 50 + " "))

	def __del__(self):
		self.browser.close()

def main():
	with open("config.json", "r", encoding="utf8") as f:
		config = json.load(f)

	pkuvenue = PKUVenue(config["user_info"])
	pkuvenue.login()

	# waiting until rushtime
	now = datetime.now()
	rushtime = datetime.strptime(config["rushtime"], "%Y-%m-%d %H:%M:%S")
	if (rushtime - now).total_seconds() > 0:
		time.sleep((rushtime - now).total_seconds())

	for k in config["order"].keys():
		if k == u"羽毛球":
			pkuvenue.orderBadminton(config["order"][k])
		elif k == u"篮球":
			pkuvenue.orderBasketball(config["order"][k])

	pkuvenue.outputOrderStatement()

	del pkuvenue

if __name__=="__main__":
	main()