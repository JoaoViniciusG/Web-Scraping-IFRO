def linksVendaPC(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    #Links, Tipo do Imóvel, Tipo de Negócio, Bairro
    links_infos = [[],[],[],[]]

    driver = webdriver.Chrome(options=options, service=service)
    driver.get('https://prettocorretoradeimoveis.com.br/comprar-alugar/imoveis/vilhena-ro')

    types_of_add = [["apartamento", "barracão", "galpão", "casa", "sobrado", "terreno", "prédio", "sala comercial", "salao comercial", "ponto comercial"],
                   ["AP", "BA", "BA", "CA", "SO", "TE", "PR", "SA", "SA", "SA"]]

    for div_id in driver.find_elements(By.CLASS_NAME, "src__Box-sc-1sbtrzs-0.sc-hlcmlc-0.jeFFeJ.CardProperty"):
        ad_type = div_id.find_element(By.CLASS_NAME, "sc-hlcmlc-15.NQNSX").text.lower()

        #Remove os imóveis rurais:
        for word in ("sitio", "sítio", "chacara", "chácara", "fazenda"):
            if ad_type.find(word) != -1: break

        else:
            #Preenche o campo "Links":
            links_infos[0].append("https://prettocorretoradeimoveis.com.br"+div_id.get_attribute("href"))

            #Preenche o campo "Tipo do Imóvel":
            for index_type, type_add_verify in enumerate(types_of_add[0]):
                if ad_type.find(type_add_verify) != -1: 
                    links_infos[1].append(types_of_add[1][index_type])
                    break
            else: links_infos[1].append("None")

            #Preenche o campo "Tipo de Negócio":
            negc_type = div_id.find_element(By.CLASS_NAME, "sc-hlcmlc-7").text.lower()

            if negc_type == "venda": links_infos[2].append("VE")
            elif negc_type == "aluguel": links_infos[2].append("LO")
            else: links_infos[2].append("None")

            #Preenche o campo "Bairro":
            neigh_text = div_id.find_element(By.CLASS_NAME, "sc-hlcmlc-1.gQklzn").text.split(" - ")[0]
            links_infos[3].append(neigh_text)

    driver.quit()
    return links_infos