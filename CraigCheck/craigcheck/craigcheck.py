from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from .mail_sender import send_email_notification

#from pyvirtualdisplay import Display     #Uncomment when running headless on raspberry pi


class CraigCheck:
	def __init__(self, headless=False, url='https://sfbay.craigslist.org/'):
		if headless:
			self.display = Display(visible=0, size=(1600,900))
			self.display.start()
			self.browser = webdriver.Firefox()
		else:
			self.browser = webdriver.Firefox(executable_path='./Driver/geckodriver')

		self.url = url
		self.headless = headless
		self.wait = WebDriverWait(self.browser, 100)
		self.new_items = list()
		self.new_items_found = False

		self.aborting = False

	def initialize_browser(self):
		self.browser.get(self.url)
		self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'querybox')))

	def item_loop(self):
		item_file = open("./items.txt", "r")
		item_list = item_file.read().splitlines()
		for item in item_list:
			print('Checking for ' + item + '...')
			self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'querybox')))
			search_field = self.browser.find_element_by_name('query')
			search_field.clear()
			search_field.send_keys(item)
			search_field.send_keys(u'\ue007')
			self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'dropdown-item')))
			mode_toggle = self.browser.find_element_by_link_text('relevant')
			mode_toggle.click()
			new_mode = self.browser.find_element_by_link_text('newest')
			new_mode.click()
			item_links = self.browser.find_elements_by_class_name('result-title')
			if item_links:
				#check to see if there are new items
				cat_file = cat_file = open('./catalog.txt', 'r')
				cat_list = cat_file.read().splitlines()
				for item in item_links:
					new_post = True
					for cat_item in cat_list:
						if item.get_attribute('href') == cat_item:
							new_post = False
					if new_post:
						print("New listing found...")
						self.new_items_found = True
						self.new_items.append(item.get_attribute('href'))
					cat_file.close()
			#self.browser.execute_script("window.history.go(-2)")
			self.browser.get(self.url)
			search_field = self.browser.find_element_by_name('query')
		item_file.close()
		if self.new_items_found:
			send_email_notification("New items - \r\n" + "\r\n".join(self.new_items),"","","") #add email credentials
		return self.new_items_found

	def catalog_current_items(self):
		item_file = open("./items.txt", "r")
		item_list = item_file.read().splitlines()
		cat_file = open('./catalog.txt', 'w')
		print('Catalogging current items...')
		for item in item_list:
			self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'querybox')))
			search_field = self.browser.find_element_by_name('query')
			search_field.clear()
			search_field.send_keys(item)
			search_field.send_keys(u'\ue007')
			self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'dropdown-item')))
			mode_toggle = self.browser.find_element_by_link_text('relevant')
			mode_toggle.click()
			new_mode = self.browser.find_element_by_link_text('newest')
			new_mode.click()
			item_links = self.browser.find_elements_by_class_name('result-title')
			if item_links:
				for link in item_links:
					cat_file.write('%s\n' % link.get_attribute('href'))
			self.browser.execute_script("window.history.go(-2)")
		print("Done cataloging.")

	def exit(self):
		self.browser.delete_all_cookies()
		self.browser.close()

		if self.headless:
			self.display.stop()




