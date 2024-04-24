def findVendaRM(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    try: from Imobiliarias.RM__ReMax.main import linksVendaRM
    except: from main import linksVendaRM
    from time import sleep

    links_infos = linksVendaRM(service, options)

    driver = webdriver.Chrome(options=options, service=service)

    #(0) Url, (1) área total, (2) área do terreno (excluída ao final), (3) área construída, (4) dormitórios, (5) suítes, (6) banheiros, (7) vagas garagem, (8) bairro, (9) valor, (10) tipo de imóvel, (11) tipo de negócio, (12) descrição
    infos = [[],[],[],[],[],[],[],[],[],[],[],[],[]]

    infos_sub_primary = [["total m²", "tamanho do lote (m²)", "área útil", "dormitório", "banheiro", "vagas de estacionamento"],
                         [1,2,3,4,6,7]]

    #Preenche os campos "(0) Url", "(10) tipo de imóvel" e "(11) tipo de negócio":
    infos[0] = links_infos[0]
    infos[10] = links_infos[1]
    infos[11] = links_infos[2]

    for link in links_infos[0]:
        driver.get(link)
        print(f"{links_infos[0].index(link)+1}/{len(links_infos[0])}", link)
        sleep(.5)

        for info_div in driver.find_elements(By.CLASS_NAME, "attributes-icons.attributes-data-col"):
            info_div_title = info_div.find_elements(By.CLASS_NAME, "data-item-label")[0].text.lower()
            if info_div_title[-1] == "s": info_div_title = info_div_title[:-1]

            try:
                index = infos_sub_primary[1][infos_sub_primary[0].index(info_div_title)]
            except: continue
        
            result = info_div.find_elements(By.CLASS_NAME, "data-item-value")[0].text.replace(".","").replace(",",".").strip()

            try:
                result = float(result)
                if result == int(result): result = int(result)
            except: pass

            infos[index].append(result)


        #Suítes:
        for suite_div in driver.find_elements(By.CLASS_NAME, "attributes-no-icons.attributes-data-col"):
            if suite_div.find_elements(By.CLASS_NAME, "data-item-label")[0].text.lower().find("suite") != -1: 
                infos[5].append(int(suite_div.find_elements(By.CLASS_NAME, "data-item-value")[0].text.strip()))


        #Bairro:
        address_text = driver.find_element(By.CLASS_NAME, "col-xs-12.key-address.fts-mark").text

        for index_neigh, neigh_part in enumerate(address_text.split(",")):
            if neigh_part.lower().strip() == "vilhena": 
                try: 
                    neighborhood = address_text.split(",")[index_neigh - 1].split("-")[-1].strip()

                    if neighborhood.find("(") != -1: 
                        infos[8].append(neighborhood[neighborhood.find("(")+1 : neighborhood.find(")")])

                    else: infos[8].append(address_text.split(",")[index_neigh - 1].split("-")[-1].strip())
                except: 
                    infos[8].append(address_text.split(",")[index_neigh - 1].strip())


        #Valor:
        try:
            price_text = driver.find_element(By.XPATH, '//*[@id="LeftColumn"]/div[2]/div/div[1]/div[1]/div[3]/div/a').text
            infos[9].append(float(price_text.replace("R$","").replace(".","").replace(",",".").strip()))
        except: pass


        #Descrição:
        descrip_text = driver.find_element(By.CLASS_NAME, "desc-short.fts-mark.tab-pane").text
        infos[12].append(descrip_text)


        #Adiciona None nos campos sem informação:
        for info in infos:
            if len(info) < links_infos[0].index(link) + 1: info.append("None")


        #Filtra a área total correta entre os campos "Área Total" e "Área do Terreno":
        areaTotal = infos[1][-1]

        areas = [infos[1][-1], infos[2][-1]]

        areas = sorted([val for val in areas if val != "None"])
        
        areas = sorted(list(set(areas)))

        if areaTotal != "None" and areaTotal == areas[-1]: 
            pass

        elif len(areas) > 1:
            infos[1][-1] = areas[-1]
    
    #Deleta o campo "Área do Terreno" pois todas as suas informações pertinentes já foram movidas para o campo "Área Total":
    del infos[2]

    driver.quit()
    return infos