# coding=utf-8
from modules.browser import Browser
import time

browser = Browser()
browser.openbrowser()
browser.geturl('http://112.74.191.10:8000/')
time.sleep(5)
browser.quit()
