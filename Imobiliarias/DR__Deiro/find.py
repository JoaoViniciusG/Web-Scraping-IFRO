def findVendaDR(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    try: from Imobiliarias.DR__Deiro.main import linksVendaDR
    except: from main import linksVendaDR

    links_types = linksVendaDR(service, options)

    driver = webdriver.Chrome(options=options, service=service)
    
    #(0) Url, (1) área total, (2) área do terreno (excluída ao final), (3) área construída, (4) dormitórios, (5) suítes, (6) banheiros, (7) vagas garagem, (8) bairro, (9) valor, (10) tipo de imóvel, (11) tipo de negócio, (12) descrição
    infos = [[],[],[],[],[],[],[],[],[],[],[],[],[]]

    infos_sub_primary = [["Área Total", "Área Terreno", "Área Construída", "Bairro", "Dormitório", "Suíte", "Banheiro", "Vaga"], 
                         [1,2,3,8,4,5,6,7]]

    for index_ad, link in enumerate(links_types[0]):
        driver.get(link)
        print(f"{links_types[0].index(link)+1}/{len(links_types[0])}", link)
        infos[0].append(link)
        infos[10].append(links_types[1][index_ad])
        infos[11].append(links_types[2][index_ad])

        for div in driver.find_elements(By. CLASS_NAME, "imodet_item1")[1:]:
            try: 
                text_infos = div.text.split(":")[0]
                if text_infos[-1] == "s": text_infos = text_infos[:-1]
                index = infos_sub_primary[1][infos_sub_primary[0].index(text_infos)]
            except: continue

            infos[index].append(div.find_elements(By. TAG_NAME, "span")[0].text.replace("m²", "").replace(".","").replace(",",".").strip())

        #Descrição:
        if driver.find_element(By. XPATH, '//*[@id="conteudo_bg1"]/table[2]/tbody/tr/td[1]/div[3]/div[6]').find_elements(By. TAG_NAME, "div")[-1].text == "DESCRIÇÃO":
            try: infos[12].append(driver.find_element(By. XPATH, '//*[@id="conteudo_bg1"]/table[2]/tbody/tr/td[1]/div[3]/div[7]').text)
            except: pass

        #Valor:
        try: infos[9].append(float(driver.find_elements(By. CLASS_NAME, "li_ftcor.imodet_item1val")[0].text.replace("R$","").replace(".","").replace(",",".").strip()))
        except: pass

        #Adiciona None nos campos sem informações:
        for info_verify in infos:
            if len(info_verify) < links_types[0].index(link) + 1: info_verify.append("None")

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