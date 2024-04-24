def findVendaFT(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    try: from Imobiliarias.FT__Futura.main import linksVendaFT
    except: from main import linksVendaFT

    links_infos = linksVendaFT(service, options)

    driver = webdriver.Chrome(options=options, service=service)
    
    #(0) Url, (1) área total, (2) área do terreno (excluída ao final), (3) área construída, (4) área útil (excluída ao final),(5) dormitórios, (6) suítes, (7) banheiros, (8) vagas garagem, (9) bairro, (10) valor, (11) tipo de imóvel, (12) tipo de negócio, (13) descrição
    infos = [[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

    infos_sub_primary = [["total", "terreno", "construída", "útil", "dormitório", "suíte", "banheiro", "vaga"],
                         [1,2,3,4,5,6,7,8]]

    for index_link, link in enumerate(links_infos[0]):
        driver.get(link)
        print(f"{links_infos[0].index(link)+1}/{len(links_infos[0])}", link)
        
        #Preenche os campos "(0) url", "(10) valor", "(11) tipo do imóvel" e "(12) tipo de negócio":
        infos[0].append(link)
        infos[10].append(links_infos[3][index_link])
        infos[11].append(links_infos[1][index_link])
        infos[12].append(links_infos[2][index_link])

        div_master = driver.find_elements(By. CLASS_NAME, 'infos_imovel')[0]

        for div_info in div_master.find_elements(By. CLASS_NAME, "detalhes")[0].find_elements(By. TAG_NAME, "div"):
            info_text = div_info.find_elements(By. TAG_NAME, "span")[-1].text.split(" ")[-1].strip()

            if info_text[-1] == "s": info_text = info_text[:-1]
            try: index = infos_sub_primary[1][infos_sub_primary[0].index(info_text)]
            except: continue

            res = div_info.find_elements(By. TAG_NAME, "span")[0].text.replace("m²","").replace(".","").replace(",",".").replace("sendo","").strip().split(" ")[0]

            try:
                res = float(res)
                if res == int(res): res = int(res)
            except: pass

            infos[index].append(res)

        #Descrição:
        try: 
            desc_text = driver.find_element(By.CLASS_NAME, 'descricao_imovel').find_element(By.CLASS_NAME, "texto").text
            if desc_text != "": infos[13].append(desc_text)
        except: pass

        #Bairro:
        try: 
            neigh_text = driver.find_element(By.CLASS_NAME, 'localizacao').text.split(" - ")[-2]
            infos[9].append(neigh_text)
        except: pass

        #Adiciona None nos campos sem informações:
        for info_verify in infos:
            if len(info_verify) < links_infos[0].index(link) + 1: info_verify.append("None")


        #Filtra a área total correta entre os campos "Área Total" e "Área do Terreno":
        areaTotal = infos[1][-1]
        areaTerreno = infos[2][-1]
        areaCons = infos[3][-1]
        areaPriv = infos[4][-1] 

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

        elif len(areas) > 1 or (len(areas) == 1 and (areas[0] == areaCons or areas[0] == areaPriv)):
            infos[3][-1] = areas[0]
    
    #Deleta o campo "Área do Terreno" e "Área Privativa" pois todas as suas informações pertinentes já foram movidas para o campo "Área Total":
    del infos[2]
    del infos[3]

    driver.quit()
    return infos