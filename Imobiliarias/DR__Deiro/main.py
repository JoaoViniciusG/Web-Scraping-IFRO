def linksVendaDR(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    #Links, Tipo do Imóvel, Tipo de Negócio
    links_types = [[],[],[]]

    driver = webdriver.Chrome(options=options, service=service)
    driver.get("http://www.deiroescritorioimobiliario.com.br/imovel/?cidade=Vilhena")

    types_of_add = [["apartamento", "barracão", "casa", "sobrado", "terreno", "lote", "prédio", "sala comercial"],
                   ["AP", "BA", "CA", "SO", "TE", "TE", "PR", "SA"]]
    
    while True:
        for div_a in driver.find_elements(By. CLASS_NAME, "imoveis_listar"):
            links_types[0].append(div_a.find_elements(By. TAG_NAME, "a")[0].get_attribute("href"))

            #Preenche o campo "Tipo do Imóvel":
            add_type = div_a.find_element(By.CLASS_NAME, "conteudo1").text.lower()

            add_type = add_type[add_type.find("/ RO") + 4 :]
            add_type = add_type[: add_type.find("para")].strip()

            for index_type, type_add_verify in enumerate(types_of_add[0]):
                if add_type.find(type_add_verify) != -1: 
                    links_types[1].append(types_of_add[1][index_type])
                    break
            
            #Preenche o campo "Tipo de Negócio":
            neg_type = div_a.find_element(By.CLASS_NAME, "conteudo1").text.lower()

            neg_type = neg_type[neg_type.index(add_type) + len(add_type) + 5:].strip().split("\n")[0]

            if neg_type == "venda": links_types[2].append("VE")
            elif neg_type == "locação": links_types[2].append("LO")
            else: raise Exception("Tipo de negócio inválido!")

        next_button = driver.find_element(By. XPATH, '//*[@id="conteudo_bg1"]/table[2]/tbody/tr/td[1]/table[2]/tbody/tr/td/div[10]').find_elements(By. TAG_NAME, "a")[-1]
        if next_button.get_attribute("title") != "Próxima Página":
            break
        next_button.click()

    driver.quit()
    return links_types