from craigcheck import CraigCheck
from time import sleep
import schedule
import time
import datetime


def run():
	print("Running..." + datetime.datetime.now().strftime('%I:%M%p'))
	session = CraigCheck(headless=False)

	session.initialize_browser()
	new_item_found = session.item_loop()
	if new_item_found:
		session.catalog_current_items()
	else:
		print('\nNo new items found.')
	session.exit()
	print("Waiting..." + datetime.datetime.now().strftime('%I:%M%p') + "\n")
schedule.every(30).minutes.do(run)

print "-------------------------------"
print "     Welcome to CraigCheck     "
print "-------------------------------"
run()
while True:
	schedule.run_pending()
	time.sleep(1)
