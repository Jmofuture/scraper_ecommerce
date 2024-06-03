from pprint import pprint

from package.craper import driver_chrome
from package.craper import scroll_down
from package.craper import keep_browser_open
from package.craper import extract_product_info
from package.craper import process_elements
from package.craper import url_list




def scrape_loi_products() -> None:
    urls = url_list()
    for url in urls:
        pprint(f"Processing URL: {url}")
        driver = driver_chrome()
        driver.get(url)
        scroll_down(driver=driver, timeout=10)
        soup = process_elements(driver=driver)
        products_info = extract_product_info(soup=soup)

        for idx, product in enumerate(products_info, start=1):
            pprint(f"Producto {idx}:")
            pprint(f"  Imagen del producto: {product['img_src']}")
            pprint(f"  Hot sale: {product['hotsale_text']}")
            pprint(f"  Precio: {product['precio_text']}")
            pprint(f"  Moneda: {product['moneda_text']}")
            pprint(f"  Descuento: {product['descuento_text']}")
            pprint(f"  URL del producto: {product['product_url']}")
            pprint(f"  Nombre y descripción del producto: {product['nombre_desc_text']}")
            pprint("")

        driver.quit()

if __name__ == '__main__':
    scrape_loi_products()
