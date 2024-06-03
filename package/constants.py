import os
from dotenv import load_dotenv

load_dotenv()


# Use to driver_chrome function
USER_AGENT=os.getenv('USER_AGENT')


URLS = {

    'loi': os.getenv('LOI_URLS').split(','),
    'covercompany': os.getenv('COVERCOMPANY_URLS').split(','),
    'amw': os.getenv('AMW_URLS').split(','),

}

ELEMENT_SELECTORS_TO_WAIT = {

    'loi': ('CSS_SELECTOR', '.parent-element-loi'),
    'covercompany': ('XPATH', '//*[@id="parent-element-covercompany"]'),
    'amw': ('ID', 'parent-element-amw'),
    
}

if __name__ == '__main__':


    for ecommerce, url_list in URLS.items():
        for url in url_list:
            print(f"{ecommerce}: {url}")