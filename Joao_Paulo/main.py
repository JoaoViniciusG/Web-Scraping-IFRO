def linksVendaJP(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.action_chains import ActionChains
    from time import sleep

    links = []

    driver = webdriver.Chrome(options=options, service=service)
    driver.get('https://joaopaulocorretordeimoveis.com.br/imovel/index/')

    words_to_search = ["chácara", "sítio", "fazenda"]

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div/div/div[2]/div[3]/div[1]/div/span[2]')))
    sleep(1)

    current_ad = 0
    print(int(driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div/div[2]/div[3]/div[1]/div/span[2]").text.split(" ")[0]) - 1)
    while current_ad < int(driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div/div[2]/div[3]/div[1]/div/span[2]").text.split(" ")[0]) - 1:
        
        div_ad = driver.find_elements(By.CLASS_NAME, "MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation0.css-1kbp4ht")[current_ad]
        for word in words_to_search:
            text_title_ad = div_ad.find_elements(By.CLASS_NAME, "MuiTypography-root.MuiTypography-body1.MuiListItemText-primary.css-1wilzx2")[0].text.lower()
            if text_title_ad.find(word) != -1: current_ad += 1; continue

        ActionChains(driver).move_to_element(div_ad).perform()
        div_ad.click()
        
        sleep(1)
        links.append(driver.current_url)
        current_ad += 1
        
        driver.back()
        sleep(1)

    print(links)
    print(len(links))

        





from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

service = Service(ChromeDriverManager().install())
options = Options()
#options.add_argument('headless')
options.add_argument('log-level=3')
#options.add_argument('--blink-settings=imagesEnabled=false')

linksVendaJP(service, options)