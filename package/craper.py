import re
import time

from colorama import init
from colorama import Fore

from typing import List
from typing import Dict
from typing import Optional
from typing import Generator

from package.constants import USER_AGENT

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

init(autoreset=True)
load_dotenv()


def driver_chrome() -> webdriver.Chrome:
    """
        Creates and configures a Chrome WebDriver instance with specified options.

    The function sets various Chrome options to customize the browser behavior, including:
    - Setting the user agent string.
    - Disabling web security.
    - Disabling extensions.
    - Ignoring certificate errors.
    - Disabling the sandbox mode.
    - Setting the log level to suppress verbose logs.
    - Allowing running insecure content.
    - Disabling default browser checks and first-run behavior.
    - Disabling the proxy server.
    - Disabling automation control detection.

    Additionally, it configures experimental options to exclude certain switches and set default preferences, such as:
    - Disabling notifications.
    - Setting the default language to Spanish.
    - Disabling download prompts.
    - Setting a default download directory.
    - Disabling credential service.

    Returns:
        webdriver.Chrome: A configured Chrome WebDriver instance.

    """

    option = Options()
    option.add_argument(f"user-agent={USER_AGENT}")
    option.add_argument("--disable-websecurity")
    option.add_argument("--disable-extensions")
    option.add_argument("--ignore-certificate-errors")
    option.add_argument("--no-sandbox")
    option.add_argument("--log-level=3")
    option.add_argument("--allow-running-insecure-content")
    option.add_argument("--no-default-browser-check")
    option.add_argument("--no-first-run")
    option.add_argument("--no-proxy-server")
    option.add_argument("--disable-blink-features=AutomationControlled")
    option.add_experimental_option("excludeSwitches", 
                                    ["enable-logging", "enable-automation", "ignore-certificate-errors"])
    option.add_experimental_option("prefs", {
                                    "profile.default_content_setting_values.notifications": 2,
                                    "intl.accept_languages": ["es-ES", "es"],
                                    "download.prompt_for_download": False,
                                    "download.default_directory": "/path/to/download/directory",
                                    "credentials_enable_service": False
    })

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)

    return driver


def keep_browser_open(driver: webdriver.Chrome) -> None:
    print("Navegador abierto. Presiona Ctrl+C para cerrar.")
    try:
        while True:
            time.sleep(1) 
    except KeyboardInterrupt:
        print("Cerrando navegador...")
        driver.close()
        

def url_generator(driver: webdriver.Chrome, urls: dict) -> Generator[None, None, None]:
    """
    Generator function to iterate through each URL in the provided dictionary of URLs
    and navigate to it using the driver.

    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance.
        urls (dict): Dictionary where keys are e-commerce site names and values are lists of URLs.

    Yields:
        None: After navigating to each URL.
    """
    for ecommerce, url_list in urls.items():
        for url in url_list:
            driver.get(url)
            print(Fore.GREEN + f"Processing the page {url} from {ecommerce}")
            yield ecommerce, url


def scroll_down(driver: webdriver.Chrome, timeout: int) -> None:
    """
    Scrolls down the webpage using the specified Selenium WebDriver instance until the end of the page is reached.

    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance controlling the browser.
        timeout (int): The time (in seconds) to wait between scroll actions to allow the page to load more content.
    """
    scroll_pause_time = timeout
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollBy(0, window.innerHeight);")  # Scrolls down by one viewport height
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        
        last_height = new_height


def wait_elements(driver: webdriver.Chrome, ecommerce: str, selectors: dict) -> bool:
    """
    Wait for elements to be present on the page based on the website.

    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance.
        ecommerce (str): The website key to select the appropriate element to wait for.
        selectors (dict): Dictionary of selectors for each website.

    Returns:
        bool: True if the element is found, False if it times out.
    """
    try:

        tag_name, class_name = selectors[ecommerce]
        is_element_present = EC.presence_of_element_located((By.XPATH, f"//{tag_name}[@class='{class_name}']"))
        WebDriverWait(driver, 10).until(is_element_present)
        print(f"//{tag_name}[@class='{class_name}']")

        return True
    
    except TimeoutException:
        print(f"Timed out waiting for page to load for {ecommerce}")
        return False


def obtain_html(driver: webdriver.Chrome) -> str:
    """
    Obtain the HTML content of the current page.

    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance.

    Returns:
        str: The HTML content of the current page as a string.
    """
    try:

        page_source = driver.page_source        
        return page_source
    
    except Exception as e:

        print(f"An error occurred while obtaining the HTML: {e}")
        return ""


def parse_html(driver: webdriver.Chrome) -> str:
    """
    Process the elements of the current page by parsing the HTML content.

    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance.

    Returns:
        BeautifulSoup: A BeautifulSoup object containing the parsed HTML content, or None if an error occurs.
    """
    page_source = obtain_html(driver)
    if page_source:
        try:
            soup = BeautifulSoup(page_source, 'html.parser')
            return soup
        except Exception as e:
            print(f"An error occurred while parsing the HTML: {e}")
            return None
    else:
        print("No page source available to process.")
        return None


def extract_product_info(driver: webdriver.Chrome):

    soup = parse_html(driver)

    products = soup.find_all('article', class_='sc-brPLxw klioUI')
    print(len(products))


def extract_product_infoasda(soup: BeautifulSoup) -> List[Dict]:

    products = soup.find_all('article', class_='sc-brPLxw klioUI')
    product_info_list = []
    for product in products:
        img_tag = product.find('div', class_='sc-gmPhUn pIiLW imagen-producto false').find('img')
        img_src = img_tag['src'] if img_tag else 'No image found'

        hotsale_tag = product.find('div', class_='sc-hknOHE jxmMoG')
        hotsale_text = hotsale_tag.text if hotsale_tag else 'No hot sale tag found'

        precio_tag = product.find('div', class_='sc-ihgnxF YylJn') or product.find('p', class_='sc-bypJrT bHSdcL')
        precio_text = precio_tag.text.strip() if precio_tag else 'No price found'
        moneda_tag = precio_tag.find('span') if precio_tag else None
        moneda_text = moneda_tag.text.strip() if moneda_tag else 'No currency found'

        precio_match = re.search(r'\d+(\.\d+)?', precio_text)
        precio_value = precio_match.group(0) if precio_match else 'No price found'

        descuento_tag = product.find('div', class_='sc-jMakVo eimOBf')
        descuento_text = descuento_tag.text if descuento_tag else 'No discount found'
        descuento_match = re.search(r'\d+(\.\d+)?', descuento_text)
        descuento_value = descuento_match.group(0) if descuento_match else 'No discount found'

        url_tag = product.find('a', class_='sc-iHbSHJ fbBSuk') 
        product_url = url_tag['href'] if url_tag else ''

        nombre_desc_tag = product.find('div', class_='sc-bBeLUv itxppj')
        nombre_desc_text = nombre_desc_tag.text if nombre_desc_tag else 'No product name or description found'

        product_info = {
            "img_src": img_src,
            "hotsale_text": hotsale_text,
            "precio_text": precio_value,
            "moneda_text": moneda_text,
            "descuento_text": descuento_value,
            "product_url": product_url,
            "nombre_desc_text": nombre_desc_text
        }

        product_info_list.append(product_info)
    
    return product_info_list
