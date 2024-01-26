def copy_text_files(name: str, acron: str, url: str) -> tuple:
    return (f"def findVenda{acron}(service, options) -> list:\n\
    from selenium import webdriver\n\
    from selenium.webdriver.common.by import By\n\
    try: from {name}.main import linksVenda{acron}\n\
    except: from main import linksVenda{acron}\n\
\n\
    links = linksVenda{acron}(service, options)\n\
\n\
    driver = webdriver.Chrome(options=options, service=service)\n\
\n\
from webdriver_manager.chrome import ChromeDriverManager\n\
from selenium.webdriver.chrome.service import Service\n\
from selenium.webdriver.chrome.options import Options\n\
from selenium import webdriver\n\
\n\
service = Service(ChromeDriverManager().install())\n\
options = Options()\n\
options.add_argument('headless')\n\
options.add_argument('log-level=3')\n\
options.add_argument('--blink-settings=imagesEnabled=false')\n\
\n\
findVenda{acron}(service, options)", 
    
    f"def linksVenda{acron}(service, options) -> list:\n\
    from selenium import webdriver\n\
    from selenium.webdriver.common.by import By\n\
\n\
    links = []\n\
\n\
    driver = webdriver.Chrome(options=options, service=service)\n\
    driver.get('{url}')")
