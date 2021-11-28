# -*- coding: utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Browser():
    def __init__(self):
        chrome_options=Options()
        chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=chrome_options, executable_path="./chromedriver")


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
        self.browser.switch_to_window(self.browser.window_handles[-1])

    def close(self):
        try:
            self.browser.quit()
            self.browser.close()
        except:
            pass