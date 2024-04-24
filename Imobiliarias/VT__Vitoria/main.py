def linksVendaVT(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    
    #Links, Tipo do Imóvel, Tipo de Negócio
    links_infos = [[],[],[]]

    driver = webdriver.Chrome(options=options, service=service)
    driver.get("http://www.vitoriaimoveis.com.br")

    types_of_add = [["apartamento", "barracão", "casa", "terreno", "prédio", "sala", "salao", "ponto"],
                   ["AP", "BA", "CA", "TE", "PR", "SA", "SA", "SA"]]
    
    td_elements = driver.find_elements(By. TAG_NAME, "td")

    for td in td_elements:
        if td.get_attribute("height") == "420": 
            try:
                td.find_element(By.ID, "tarja_texto2")
                continue
            except:
                pass

            url_text = td.find_element(By. TAG_NAME, "a").get_attribute("href")

            #Tipo do Imóvel:
            add_type = url_text.split("/")[-1].split("-")[0]
            
            for index_type, type_add_verify in enumerate(types_of_add[0]):
                if add_type.find(type_add_verify) != -1: 
                    links_infos[1].append(types_of_add[1][index_type])
                    break
            else: 
                continue

            #Tipo de Negócio:

            for word in url_text.split("/")[-1].split("-"):
                if word == "venda": links_infos[2].append("VE")
                elif word == "locacao": links_infos[2].append("LO")

            links_infos[0].append(url_text)

    driver.quit()
    return links_infos