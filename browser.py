# -*- coding: utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import base64
import cv2
import numpy as np

class Browser():
    def __init__(self):
        chrome_options=Options()
        caps = {
            'browserName': 'chrome',
            'version': '',
            'platform': 'ANY',
            'goog:loggingPrefs': {'performance': 'ALL'},
            'goog:chromeOptions': {'extensions': [], 'args': ['']}
        }
        self.browser = webdriver.Chrome(desired_capabilities=caps, chrome_options=chrome_options, executable_path="./chromedriver")

    def clickByXPath(self, xpath):
        while True:
            try:
                self.browser.find_element_by_xpath(xpath).click()
                return
            except Exception as e:
                # print(e)
                pass

    def clickByCssSelector(self, cssSelector):
        while True:
            try:
                self.browser.find_element_by_css_selector(cssSelector).click()
                return
            except Exception as e:
                # print(e)
                pass

    def typeByCssSelector(self, cssSelector, text):
        while True:
            try:
                self.browser.find_element_by_css_selector(cssSelector).clear()
                self.browser.find_element_by_css_selector(cssSelector).send_keys(text)
                return
            except Exception as e:
                # print(e)
                pass

    def typeByXPath(self, xpath, text):
        while True:
            try:
                self.browser.find_element_by_xpath(xpath).clear()
                self.browser.find_element_by_xpath(xpath).send_keys(text)
                return
            except Exception as e:
                # print(e)
                pass

    def findElementByXPath(self, xpath):
        while True:
            try:
                element = self.browser.find_element_by_xpath(xpath)
                return element
            except Exception as e:
                # print(e)
                pass

    def findElementByCssSelector(self, cssSelector):
        while True:
            try:
                element = self.browser.find_element_by_css_selector(cssSelector)
                return element
            except Exception as e:
                # print(e)
                pass


    def gotoPage(self, url):
        print("goto page %s" % url)
        self.browser.execute_script("window.open(\"%s\")" % url)
        self.browser.switch_to.window(self.browser.window_handles[-1])

    def close(self):
        try:
            self.browser.quit()
            self.browser.close()
        except:
            pass

    def dragOffsetByXPath(self, xpath, offset):
        while True:
            try:
                element = self.browser.find_element_by_xpath(xpath)
                action_chains = ActionChains(self.browser)
                action_chains.drag_and_drop_by_offset(element, offset, 0).perform()
                return
            except Exception as e:
                # print(e)
                pass

    def getImgByteDataByXPath(self, xpath, name):
        while True:
            try:
                element = self.browser.find_element_by_xpath(xpath)
                base64_data = element.get_attribute("src").split(",")[1]
                byte_data = base64.b64decode(base64_data)
                return byte_data
            except Exception as e:
                # print(e)
                pass


            