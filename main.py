# -*- coding: utf-8
from lib2to3.pgen2 import driver
import re
from browser import Browser
import json, time
from datetime import datetime
import numpy as np
import cv2

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
		# waiting for the table to show up
		self.browser.findElementByXPath("/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[3]/div[1]/div/div/div/div/div/table/tbody/tr[15]/td[1]/div")

	def __submitOrder(self):
		print("read & agree ✅!!!!")
		self.browser.clickByXPath("/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[4]/label/span/input")

		print("click to make order......")
		self.browser.clickByXPath("/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[5]/div/div[2]")

		print("submiting order ....... ")
		self.browser.typeByXPath("/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/form/div/div[4]/div/div/div/div/input", self.phone)
		self.browser.clickByXPath("/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div/div/div[2]")


	def __makeOrder(self, sportsName, timeList, courtPriorityList, courtIndexDict, orderDate, orderTimeList):
		orderEnable = False
		currentPageIndex = 0
		pageJumpButtonIndex = [None, 6, 2]
		for ot in orderTimeList:
			print("selecting time %s ........." % ot)
			timeTableRow = timeList.index(ot)+1
			courtSelected = False
			for court in courtPriorityList:
				courtPageIndex = courtIndexDict[court]["page"]
				courtTableColumn = courtIndexDict[court]["column"]
				# judge whether jump page or not
				pageDelta = courtPageIndex - currentPageIndex
				jumpDirection = 1 if pageDelta > 0 else -1
				for _ in range(0, pageDelta, jumpDirection):
					self.browser.clickByXPath("/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[3]/div[1]/div/div/div/div/div/table/thead/tr/td[%d]/div/span/i" % pageJumpButtonIndex[jumpDirection])
					currentPageIndex += jumpDirection
				# select court block
				courtBlockElment = self.browser.findElementByXPath("/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[3]/div[1]/div/div/div/div/div/table/tbody/tr[%d]/td[%d]/div" % (timeTableRow, courtTableColumn+1))
				if "free" in courtBlockElment.get_attribute('class'):
					courtBlockElment.click()
					courtSelected = True
					self.orderStatement.append("%s %s %s %s" % (sportsName, orderDate, ot, court))
					print("selected %s %s %s" % (orderDate, ot, court))
					break
			if not courtSelected:
				self.orderStatement.append("%s %s %s %s" % (sportsName, orderDate, ot, "无场"))
				print("without court left at %s %s" % (orderDate, ot))
			else:
				orderEnable = True

		return orderEnable

	def _order(self, sportsName, venueUrl, timeList, courtPriorityList, courtIndexDict, orderDate, orderTimeList):
		self.browser.gotoPage(venueUrl)
		self.__jumpToDate(orderDate)
		if self.__makeOrder(sportsName, timeList, courtPriorityList, courtIndexDict, orderDate, orderTimeList):
			self.__submitOrder()

	def orderBadmintonOnce(self, orderDate, orderTimeList):
		timeList = ["8:00-9:00","9:00-10:00","10:00-11:00","11:00-12:00","12:00-13:00","13:00-14:00","14:00-15:00","15:00-16:00","16:00-17:00","17:00-18:00","18:00-19:00","19:00-20:00","20:00-21:00","21:00-22:00"]
		# courtList = [["1号", "2号", "3号", "4号", "5号"], ["6号", "7号", "8号", "9号", "10号"], ["11号", "12号"]]
		courtPriorityList = ["3号", "4号", "9号", "10号", "1号", "2号", "5号", "6号", "7号", "8号", "11号", "12号"]
		courtIndexDict = {
			"1号" : {"page": 0, "column": 1},
			"2号" : {"page": 0, "column": 2},
			"3号" : {"page": 0, "column": 3},
			"4号" : {"page": 0, "column": 4},
			"5号" : {"page": 0, "column": 5},
			"6号" : {"page": 1, "column": 1},
			"7号" : {"page": 1, "column": 2},
			"8号" : {"page": 1, "column": 3},
			"9号" : {"page": 1, "column": 4},
			"10号": {"page": 1, "column": 5},
			"11号": {"page": 2, "column": 1},
			"12号": {"page": 2, "column": 2}
		}
		self._order("羽毛球", "https://epe.pku.edu.cn/venue/pku/venue-reservation/60", timeList, courtPriorityList, courtIndexDict, orderDate, orderTimeList)

	def orderBadminton(self, reqList):
		reqDict = self._reqListToDict(reqList)
		for orderDate in reqDict:
			for i in range(0, len(reqDict[orderDate]), 2):
				self.orderBadmintonOnce(orderDate, reqDict[orderDate][i:i+2])
				self.slideCaptchaValid()

	def orderBasketballOnce(self, orderDate, orderTimeList):
		timeList = ["8:00-9:00","9:00-10:00","10:00-11:00","11:00-12:00","12:00-13:00","13:00-14:00","14:00-15:00","15:00-16:00","16:00-17:00","17:00-18:00","18:00-19:00","19:00-20:00","20:00-21:00","21:00-22:00"]
		# courtList = [["北1", "南1", "北2", "南2"]]
		courtPriorityList = ["北1", "南1", "北2", "南2"]
		courtIndexDict = {
			"北1" : {"page": 0, "column": 1},
			"南1" : {"page": 0, "column": 2},
			"北2" : {"page": 0, "column": 3},
			"南2" : {"page": 0, "column": 4}
		}
		self._order("篮球", "https://epe.pku.edu.cn/venue/pku/venue-reservation/68", timeList, courtPriorityList, courtIndexDict, orderDate, orderTimeList)


	def orderBasketball(self, reqList):
		reqDict = self._reqListToDict(reqList)
		for orderDate in reqDict:
			for i in range(0, len(reqDict[orderDate]), 2):
				self.orderBasketballOnce(orderDate, reqDict[orderDate][i:i+2])
				self.slideCaptchaValid()

	def _countDistance(self, template, target):
		encode_img = np.asarray(bytearray(template), dtype="uint8")
		template = cv2.imdecode(encode_img, cv2.IMREAD_UNCHANGED)
		# cv2.imwrite('template.png', template)
		template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
		encode_img = np.asarray(bytearray(target), dtype="uint8")
		target = cv2.imdecode(encode_img, cv2.IMREAD_UNCHANGED)
		# cv2.imwrite('target.png', target)
		target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
		w, h = target.shape[::1]
		left = w
		right = 0
		up = h
		down = 0
		for row in range(0, h):
			for col in range(0, w):
				if target[col][row] != 0:
					if left > col:
						left = col
					if right < col:
						right = col
					if up > row:
						up = row
					if down < row:
						down = row
		result = cv2.matchTemplate(target[left:right, up:down], template, cv2.TM_CCOEFF_NORMED)
		_, y = np.unravel_index(result.argmax(), result.shape)
		# x, y = np.unravel_index(result.argmax(), result.shape)
		# cv2.rectangle(template, (y, x), (y+right-left, x+down-up), (7, 249, 151), 2)
		# cv2.imwrite('targ.png', target[left:right, up:down])
		# cv2.imwrite('temp.png', template)
		# cv2.imwrite('show.png', template)
		return y


	def slideCaptchaValid(self):
		valid = False
		padding = 5
		while not valid:
			print("slide Captcha ing ......... ")
			_ = self.browser.browser.get_log("performance")
			distance = self._countDistance(self.browser.getImgByteDataByXPath("/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/img", "template.png"),
										self.browser.getImgByteDataByXPath("/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[2]/div/div[2]/div/div[2]/div/div/div/img", "target.png"))
			self.browser.dragOffsetByXPath("/html/body/div[1]/div/div/div[3]/div[2]/div/div[2]/div[2]/div/div[2]/div/div[2]/div/div", distance + padding)

			# for retry ....
			waiting = True
			while waiting:
				requests = self.browser.browser.get_log("performance")
				for r in requests:
					r = json.loads(r['message'])['message']
					if r["method"] == 'Network.responseReceived' and r['params']['response']['url'] == "https://epe.pku.edu.cn/venue-server/api/captcha/check":
						response_body = self.browser.browser.execute_cdp_cmd('Network.getResponseBody', {'requestId': r['params']['requestId']})['body']
						response_body = json.loads(response_body)
						if response_body["data"]["success"]:
							print("slide Captcha Success !!!!!!! ")
							valid = True
						waiting = False
			# retry after 2s ....
			time.sleep(2)
						
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