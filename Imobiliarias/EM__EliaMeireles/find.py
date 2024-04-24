def findVendaEM(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    try: from Imobiliarias.EM__EliaMeireles.main import linksVendaEM
    except: from main import linksVendaEM

    links_type = linksVendaEM(service, options)

    driver = webdriver.Chrome(options=options, service=service)

    #(0) Url, (1) área total, (2) área do terreno (excluída ao final), (3) área construída, (4) dormitórios, (5) suítes, (6) banheiros, (7) vagas garagem, (8) bairro, (9) valor, (10) tipo de imóvel, (11) tipo de negócio, (12) descrição
    infos = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
    
    infos_sub_primary = [["área total", "terreno", "construção", "quarto", "suíte", "banheiro", "vaga"],
                         [1,2,3,4,5,6,7]]
    
    print(len(links_type[0]), len(links_type[1]))

    for index_ad, link in enumerate(links_type[0]):
        driver.get(link)
        print(f"{links_type[0].index(link)+1}/{len(links_type[0])}", link)
        infos[0].append(link)
        infos[10].append(links_type[1][index_ad])

        #Preenche o campo "Tipo de Negócio" com "VE":
        infos[11].append("VE")

        for li_info in driver.find_elements(By.CLASS_NAME, "listpanel-content")[0].find_elements(By.TAG_NAME, "li"):
            try: index = infos_sub_primary[1][infos_sub_primary[0].index(li_info.text.lower().split(":")[0])]
            except: continue

            result = li_info.text.lower().split(":")[-1].replace("m²","").strip()

            try:
                result = float(result)
                if result == int(result): result = int(result)
                if result == 0: continue
            except: continue

            infos[index].append(result)
        
        for div_info in driver.find_elements(By.CLASS_NAME, "listpanel-head")[0].find_elements(By.TAG_NAME, "div"):
            try: index = infos_sub_primary[1][infos_sub_primary[0].index(div_info.text.lower().replace("(s)", "").strip().split(" ")[-1])]
            except: continue

            try: result = int(div_info.text.lower().split(" ")[0].strip())
            except: continue

            if result < 0: result = -result
            infos[index].append(result)

        #Bairro:
        text_neighborhood = driver.find_element(By.XPATH, '//*[@id="pageWrapper"]/div/div[1]/div/main/section[2]/header/div[1]/h1').text.lower()
        if text_neighborhood[text_neighborhood.find(" no ")+4:].replace("vilhena","").replace("venda","").replace("- ro", "").strip() != "":
            infos[8].append(text_neighborhood[text_neighborhood.find(" no ")+4:].replace("venda","").strip())
        
        #Valor: 
        try:
            text_price = float(driver.find_element(By.XPATH, '//*[@id="Detail"]/div[2]/h2').text.replace("R$","").replace(".","").replace(",",".").strip())
            if text_price > 100000000: raise
            infos[9].append(text_price)
        except: pass

        #Descrição:
        for section in driver.find_elements(By.CLASS_NAME, "accountData"):
            try:
                if section.find_element(By.TAG_NAME, "h4").text.lower() != "descrição": continue
            except: continue

            descrip = ""

            for p_descrip in section.find_elements(By.TAG_NAME, "p"):
                descrip += p_descrip.text + "\n"

            infos[12].append(descrip[:-2])

        #Adiciona None nos campos sem informação:
        for info in infos:
            if len(info) < links_type[0].index(link) + 1: info.append("None")

        
        #Filtra a área total correta entre os campos "Área Total" e "Área do Terreno":
        areaTotal = infos[1][-1]
        areaTerreno = infos[2][-1]
        areaCons = infos[3][-1] 

        areas = [infos[1][-1], infos[2][-1], infos[3][-1], infos[4][-1]]

        areas = sorted([val for val in areas if val != "None"])
        
        areas = sorted(list(set(areas)))

        if areaTotal != "None" and areaTotal == areas[-1]: 
            pass

        elif len(areas) > 1 or (len(areas) == 1 and (areas[0] == areaTotal or areas[0] == areaTerreno)):
            infos[1][-1] = areas[-1]

        #Filtra a área construída correta entre todos os campos de área caso o campo "Área Construída" seja igual a "None":
            
        if areaCons != "None" and areaCons == areas[0]:
            pass

        elif len(areas) > 1 or (len(areas) == 1 and areas[0] == areaCons):
            infos[3][-1] = areas[0]

    
    #Deleta o campo "Área do Terreno" pois todas as suas informações pertinentes já foram movidas para o campo "Área Total":
    del infos[2]

    driver.quit()
    return infos