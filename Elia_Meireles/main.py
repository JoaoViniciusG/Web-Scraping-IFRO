def linksVendaEM(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    links = []

    driver = webdriver.Chrome(options=options, service=service)
    driver.get('https://eliameirelescorretora.com.br/imoveis/?q=vilhena&pagina=1')

    while True:
        for div_ad in driver.find_elements(By.CLASS_NAME, "col-xs-12.col.isoCol"):
            #Remove os anúncios já vendidos ou alugados:
            try: 
                if div_ad.find_elements(By.CLASS_NAME, "label.label-danger")[0].text.lower() in ("vendido", "alugado"): continue
            except: pass

            #Revome os imóveis rurais:
            if div_ad.find_elements(By.TAG_NAME, "h2")[0].text.lower().find("rural") != -1: continue
            
            links.append(div_ad.find_elements(By.TAG_NAME, "a")[0].get_attribute("href"))

        next_button = driver.find_elements(By.CLASS_NAME, "next.page-numbers")[0]
        if next_button.get_attribute("href") == None: break
        next_button.click()

    driver.quit()
    return links