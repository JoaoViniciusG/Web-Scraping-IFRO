def linksVendaFB_CF_SR_CR(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from time import sleep

    #Link do Imóvel, Tipo do Imóvel, Tipo de Negócio
    links_type = [[],[],[]]

    links_imob = ["https://www.concretizevha.com.br/imovel/?finalidade=&cidade=Vilhena",
                  "http://www.fbcorretordeimoveis.com.br/imovel/?finalidade=&tipo=&cid=Vilhena&bairro=0&sui=&ban=&gar=&dor=&pag=1",
                  "https://www.caiofernandocorretor.com.br/imovel/?finalidade=&tipo=&cid=Vilhena&bairro=0&sui=&ban=&gar=&dor=&pag=1"]
                  #"http://www.samuelrichard.com.br/imovel/?finalidade=venda&tipo=&cid=Vilhena&bairro=0&sui=&ban=&gar=&dor=&pag=1"]
    
    words_to_search = ["chácara", "sítio", "fazenda"]

    types_of_add = [["apartamento", "galpão", "casa", "terreno", "prédio"],
                   ["AP", "GA", "CA", "TE", "PR"]]
    
    driver = webdriver.Chrome(options=options, service=service)

    for link in links_imob:
        driver.get(link)

        while True:
            for div_a in driver.find_elements(By. CLASS_NAME, "imovelcard")[:-1]:
                add_type = div_a.find_elements(By.CLASS_NAME, "imovelcard__info__ref")[0].text.lower().split("-")[-1].strip()

                #Remove os imóveis rurais:
                for word in words_to_search:
                    if add_type.find(word) != -1: break
                #Adiciona os links dos imóveis válidos:
                else: 
                    links_type[0].append(div_a.find_elements(By. TAG_NAME, "a")[0].get_attribute("href"))
                
                    #Preenche o campo "Tipo do Imóvel":
                    for index_type, type_add_verify in enumerate(types_of_add[0]):
                        if add_type.find(type_add_verify) != -1: 
                            links_type[1].append(types_of_add[1][index_type])
                            break
                    
                    #Preenche o campo "Tipo de Negócio":
                    negc_type = div_a.find_element(By.CLASS_NAME, "imovelcard__info__tag").text.lower()

                    if negc_type == "venda": links_type[2].append("VE")
                    elif negc_type == "locação": links_type[2].append("LO")
            
            next_button = driver.find_elements(By. CLASS_NAME, "lista_imoveis_paginacao")[0].find_elements(By. TAG_NAME, "a")[-1]
            if next_button.text != ">": break
            next_button.click()

    driver.quit()
    return links_type