def findVendaJP(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    try: from Joao_Paulo.main import linksVendaJP
    except: from main import linksVendaJP

    links = linksVendaJP(service, options)

    driver = webdriver.Chrome(options=options, service=service)

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

service = Service(ChromeDriverManager().install())
options = Options()
options.add_argument('headless')
options.add_argument('log-level=3')
options.add_argument('--blink-settings=imagesEnabled=false')

findVendaJP(service, options)