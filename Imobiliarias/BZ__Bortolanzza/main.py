def linksVendaBZ(service, options) -> list:
    from selenium.webdriver.common.by import By 
    from selenium import webdriver

    #Links, Tipo do Imóvel, Tipo de Negócio
    links_infos = [[],[],[]]

    driver = webdriver.Chrome(options=options, service=service)
    driver.get("http://www.bortolanzza.com.br/imovel/?finalidade=venda&cidade=Vilhena")

    types_of_add = [["apartamento", "casa", "terreno", "prédio", "comercial"],
                   ["AP", "CA", "TE", "PR", "SA"]]

    while True:
        for td in driver.find_elements(By. TAG_NAME, 'td'):
            if td.get_attribute("width") == "70%":
                if td.find_element(By.TAG_NAME, "h2").text.lower().find("rural") != -1: continue
                links_infos[0].append(td.find_elements(By. TAG_NAME, "a")[0].get_attribute("href"))

                add_title = td.find_element(By.TAG_NAME, "a").get_attribute("title").split(",")[0].lower()

                #Preenche o campo "Tipo do Imóvel":
                add_type = add_title.split("para")[0].strip()

                for index_type, type_add_verify in enumerate(types_of_add[0]):
                    if add_type.find(type_add_verify) != -1: 
                        links_infos[1].append(types_of_add[1][index_type])
                        break

                #Preenche o campo "Tipo de Negócio":
                negc_type = add_title.split("para")[1].strip()

                if negc_type == "venda": links_infos[2].append("VE")
                elif negc_type == "locação": links_infos[2].append("LO")

        next_button = driver.find_element(By. XPATH, '//*[@id="conteudo_bg1"]/table[1]/tbody/tr/td[1]/table[4]/tbody/tr/td').find_elements(By. TAG_NAME, "a")[-1]
        if next_button.get_attribute("title") != "Próxima Página":
            break
        next_button.click()

    driver.quit()
    return links_infos