def linksVendaEM(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    #Link, Tipo do Imóvel
    links_types = [[],[]]

    driver = webdriver.Chrome(options=options, service=service)
    driver.get('https://eliameirelescorretora.com.br/imoveis/?q=vilhena&pagina=1')

    types_of_add = [["apartamento", "galpão", "casa", "terreno", "prédio"],
                   ["AP", "GA", "CA", "TE", "PR"]]
    
    while True:
        for div_ad in driver.find_elements(By.CLASS_NAME, "col-xs-12.col.isoCol"):
            #Remove os anúncios já vendidos ou alugados:
            try: 
                if div_ad.find_elements(By.CLASS_NAME, "label.label-danger")[0].text.lower() in ("vendido", "alugado"): continue
            except: pass

            #Preenche o campo "Tipo do Imóvel":
            address_text = div_ad.find_element(By.TAG_NAME, "address").text

            add_type = address_text.split(":")[1].split("\n")[0].lower().strip()

            for index_type, type_add_verify in enumerate(types_of_add[0]):
                if add_type.find(type_add_verify) != -1: 
                    links_types[1].append(types_of_add[1][index_type])
                    break
            else:
                continue
            
            #Remove os imóveis rurais:
            if div_ad.find_elements(By.TAG_NAME, "h2")[0].text.lower().find("rural") != -1: continue
            
            links_types[0].append(div_ad.find_elements(By.TAG_NAME, "a")[0].get_attribute("href"))

        next_button = driver.find_elements(By.CLASS_NAME, "next.page-numbers")[0]
        if next_button.get_attribute("href") == None: break
        next_button.click()

    driver.quit()
    return links_types