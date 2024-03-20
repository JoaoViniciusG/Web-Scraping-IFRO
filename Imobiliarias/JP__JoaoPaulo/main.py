def linksVendaJP(service) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.chrome.options import Options
    from time import sleep

    links = []

    options = Options()
    options.add_argument('log-level=3')

    driver = webdriver.Chrome(options=options, service=service)
    driver.get('https://joaopaulocorretordeimoveis.com.br/imovel/index/')
    driver.maximize_window()

    words_to_search = ["chácara", "sítio", "fazenda"]

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div/div/div[2]/div[3]/div[1]/div/span[2]')))
    driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div/div[2]/div[2]/form/div/div[2]/div[6]/div/input").send_keys("Vilhena")
    sleep(1)
    height = driver.execute_script("return document.body.scrollHeight")
    for num in [-1, 1/4, 2/4, 3/4]:
        ActionChains(driver).scroll_by_amount(0, int(height*num)).perform()
        sleep(1)

    for div_ad in driver.find_elements(By.CLASS_NAME, "MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation0.css-1kbp4ht"):
        ad_title = div_ad.find_elements(By.CLASS_NAME, "MuiTypography-root.MuiTypography-body1.MuiListItemText-primary.css-1wilzx2")[0].text.lower()
        
        #Remove imóveis rurais:
        for word in words_to_search:
            if ad_title.find(word) != -1: break
        else:
            try: ad_num = div_ad.find_elements(By.CLASS_NAME, "MuiBox-root.css-o2945x")[0].get_attribute("src").split("/")[4]
            except: continue
            links.append(f"https://joaopaulocorretordeimoveis.com.br/imovel/show/habitacao/{ad_num}/")

    driver.quit()
    return links