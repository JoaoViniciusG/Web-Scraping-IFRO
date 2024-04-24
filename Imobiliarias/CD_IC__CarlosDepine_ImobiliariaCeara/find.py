def findVendaCD_IC(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    try: from main import linksVendaCD_IC
    except: from Imobiliarias.CD_IC__CarlosDepine_ImobiliariaCeara.main import linksVendaCD_IC
    from time import time

    links = linksVendaCD_IC(service, options)

    driver = webdriver.Chrome(options=options, service=service)
    
    #(0) Url, (1) área total, (2) área do terreno (excluída ao final), (3) área útil (área construída), (4) área privativa (excluída ao final),(5) dormitórios, (6) suítes, (7) banheiros, (8) vagas garagem, (9) bairro, (10) valor, (11) tipo de imóvel, (12) tipo de negócio, (13) descrição
    infos = [[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

    infos_sub_primary = [["Área Total", "Área Terreno", "Área Útil", "Área Privativa", "Dormitórios", "Suítes", "Banheiros", "Box (N˚ Garagem)", "Garagem", "Venda", "Locação"],
                         [1,2,3,4,5,6,7,8,8,10,10]]
    
    types_of_add = [["apartamento", "barracão", "galpão", "galpao", "barracao", "casa", "sobrado", "terreno", "lote", "prédio", "sala comercial", "sala", "comercial"],
                   ["AP", "BA", "BA", "BA", "BA", "CA", "CA", "TE", "TE", "PR", "SA", "SA", "PT"]]
    
    for link in links:
        driver.get(link)
        print(f"{links.index(link)+1}/{len(links)}", link)

        try:   
            if driver.find_element(By.CLASS_NAME, "box.text-center").find_element(By.TAG_NAME, "img").get_attribute("src") == "https://meusiteimobiliario.com.br/painel/front/tema01/assets/images/pagina_nao_encontrada.png":
                print("Erro! 404")
                continue
        except: pass

        infos[0].append(link)

        for info_primary in driver.find_elements(By. CLASS_NAME, "col-xs-12.col-sm-6"):
            try: index = infos_sub_primary[1][infos_sub_primary[0].index(info_primary.find_elements(By. TAG_NAME, "span")[0].text)]
            except: continue

            info = info_primary.find_elements(By. CLASS_NAME, "pull-right")[0].text.replace("R$ ","").split(" ")[0].replace(".","").replace(",",".")

            if info.find("-") != -1:
                info = info[:info.index("-")]

            try:
                info = float(info)
                if info == int(info): info = int(info)
            except: 
                continue

            if index == 8 and len(infos[8]) == links.index(link) + 1 and info <= infos[8][-1]: continue
            elif index == 8 and len(infos[8]) == links.index(link) + 1: del infos[8][-1]

            infos[index].append(info)

        #Descrição:
        try:
            desc_text = driver.find_element(By. XPATH, "/html/body/div/main/div/div/div/div/div[4]/div[5]/p").text
            if  desc_text == "": raise

            infos[13].append(desc_text)
        except: 
            try: 
                desc_text = ""
                for div_desc in driver.find_element(By. XPATH, "/html/body/div/main/div/div/div/div/div[4]/div[5]").find_elements(By. TAG_NAME, "div"):
                    if div_desc.get_attribute("class") != "": break
                    if div_desc.text == "": continue
                    desc_text += div_desc.text + "\n"
                
                if desc_text[:-1] == "": raise

                infos[13].append(desc_text[:-1])
            
            except: pass

        #Título:
        ad_title = driver.find_element(By.CLASS_NAME, "row.ajuste").find_element(By.CLASS_NAME, "col-md-9").text.lower()

            #Tipo de Negócio:
        ad_neg_type = ad_title.split("-")[0].strip()

        if ad_neg_type == "venda": infos[12].append("VE")
        elif ad_neg_type == "locação": infos[12].append("LO")
        else: raise Exception("Tipo de negócio inválido!")

            #Tipo de Imóvel:
        add_type = ad_title.split("-")[1]

        for index_type, type_add_verify in enumerate(types_of_add[0]):
            if add_type.find(type_add_verify) != -1: 
                infos[11].append(types_of_add[1][index_type])
                break
        else: pass

            #Bairro:
        infos[9].append(ad_title.split(" - ")[2].strip())

        #Adiciona None nos campos sem informações:
        for info_verify in infos:
            if len(info_verify) < links.index(link) + 1: info_verify.append("None")

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