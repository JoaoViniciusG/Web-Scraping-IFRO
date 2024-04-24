def findVendaDC(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    try: from Imobiliarias.DC__DonadoniCorretor.main import linksVendaDC
    except: from main import linksVendaDC

    links = linksVendaDC(service, options)
    
    driver = webdriver.Chrome(options=options, service=service)

    #(0) Url, (1) área total, (2) área do terreno (excluída ao final), (3) área construída, (4) área útil (excluída ao final),(5) dormitórios, (6) suítes, (7) banheiros, (8) vagas garagem, (9) bairro, (10) valor, (11) tipo de imóvel, (12) tipo de negócio, (13) descrição
    infos = [[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    
    infos_sub_primary = [["área total", "área terreno", "área construída", "área útil", "dormitório", "suíte", "banheiro", "vaga", "bairro"],
                         [1,2,3,4,5,6,7,8,9]]
    
    types_of_add = [["apartamento", "casa", "sobrado", "terreno", "comercial"],
                   ["AP", "CA", "SO", "TE", "SA"]]
    
    for link in links:
        driver.get(link)
        print(f"{links.index(link)+1}/{len(links)}", link)
        infos[0].append(link)

        for tr_info in driver.find_element(By.ID, "tb_features1").find_elements(By.TAG_NAME, "tr"):
            info_title = tr_info.text.lower().split(":")[0]
            try: 
                if info_title[-1] == "s": info_title = info_title[:-1]
            except: continue

            try: index = infos_sub_primary[1][infos_sub_primary[0].index(info_title)]
            except: continue
            
            info_result = tr_info.text.split(":")[-1].replace("m²","").replace(".","").replace(",",".").strip()

            if info_title != "código":
                try: 
                    info_result = float(info_result)
                    if info_result == int(info_result): info_result = int(info_result)
                except: pass
            
            infos[index].append(info_result)

        #Valor: 
        try: 
            text_price = driver.find_elements(By.CLASS_NAME, "grid-3.valores")[0].text 
            infos[10].append(float(text_price.replace("R$","").replace(".","").replace(",",".").strip()))
        except: pass

        #Tipo do imóvel (TI) e Tipo do negócio (TN):

        infos_TT_TN = driver.find_element(By.CLASS_NAME, "interna__title").text.split(",")[0].lower()

        #TI:
        ad_type = infos_TT_TN.split("para")[0].strip()

        for index_type, type_add_verify in enumerate(types_of_add[0]):
                if ad_type.find(type_add_verify) != -1: 
                    infos[11].append(types_of_add[1][index_type])
                    break

        #TN:
        ngc_type = infos_TT_TN.split("para")[1].strip()

        if ngc_type == "venda": infos[12].append("VE")
        elif ngc_type == "locação": infos[12].append("LO")


        #Descrição:
        index_desc = -1

        for h3_index, h3_title in enumerate(driver.find_element(By.CLASS_NAME, "grid-9.descricao").find_elements(By.TAG_NAME, "h3")):
            if h3_title.get_attribute("id") == "desc_descricao":
                index_desc = h3_index
                break
        
        if index_desc > -1:
            desc_text = driver.find_element(By.CLASS_NAME, "grid-9.descricao").find_elements(By.TAG_NAME, "div")[index_desc].text.strip()

            if desc_text != "":
                infos[13].append(desc_text)

        #Adiciona None nos campos sem informação:
        for info in infos:
            if len(info) < links.index(link) + 1: info.append("None")

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