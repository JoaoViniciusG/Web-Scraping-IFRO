def linksVendaAR(service, options) -> list:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC 
    from selenium import webdriver

    links = []

    driver = webdriver.Chrome(options=options, service=service)
    driver.get("https://www.arevalimoveis.com.br/imoveis/a-venda/vilhena")

    while True:
        try: WebDriverWait(driver, timeout = 3).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn.btn-md.btn-primary.btn-next")))
        except: break

        driver.execute_script("document.getElementsByClassName('btn btn-md btn-primary btn-next')[0].click()")

    links_loc = driver.find_elements(By. CLASS_NAME, "card_split_vertically.borderHover")
    
    for element in links_loc:
        #Remove imóveis rurais e os lançamentos de bairros/condomínios:
        if element.find_elements(By.CLASS_NAME, "card_split_vertically__code")[0].text[:2] not in ("CA", "SO", "PT", "TE"): continue
        links.append(element.get_attribute("href"))

    driver.quit()
    return links