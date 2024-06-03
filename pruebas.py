import os
from dotenv import load_dotenv
from pprint import pprint

from package.craper import driver_chrome
from package.craper import url_generator
from package.craper import scroll_down
from package.craper import wait_elements
from package.craper import extract_product_info

from package.craper import keep_browser_open


from package.constants import URLS
from package.constants import ELEMENT_SELECTORS_TO_WAIT



driver = driver_chrome()

url_gen = url_generator(driver, URLS)



# Use the generator in a loop
for ecommerce, url in url_gen:
    scroll_down(driver=driver, timeout=7.5)
    wait_elements(driver=driver, ecommerce=ecommerce, selectors=ELEMENT_SELECTORS_TO_WAIT)

extract_product_info(driver=driver)


keep_browser_open(driver)
