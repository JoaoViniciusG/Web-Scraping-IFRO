def findVendaFB_CF_SR_CR(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    try: from Imobiliarias.FB_CF_SR_CR__FbCorretor_CaioFernandes_Samuel_Concretize.main import linksVendaFB_CF_SR_CR
    except: from main import linksVendaFB_CF_SR_CR

    links_type = linksVendaFB_CF_SR_CR(service, options)

    driver = webdriver.Chrome(options=options, service=service)

    #(0) Url, (1) área total, (2) área do terreno (excluída ao final), (3) área construída, (4) dormitórios, (5) suítes, (6) banheiros, (7) vagas garagem, (8) bairro, (9) valor, (10) tipo de imóvel, (11) tipo de negócio, (12) descrição
    infos = [[],[],[],[],[],[],[],[],[],[],[],[],[]]

    infos_sub_primary = [["Área Total", "Área Terreno", "Área Construída", "Bairro", "Dormitório", "Suíte", "Banheiro", "Vaga"], 
                         [1,2,3,8,4,5,6,7]]

    for index_ad, link in enumerate(links_type[0]):
        driver.get(link)
        print(f"{links_type[0].index(link)+1}/{len(links_type[0])}", link)
        infos[0].append(link)
        infos[10].append(links_type[1][index_ad])
        infos[11].append(links_type[2][index_ad])

        for tag in driver.find_element(By. ID, "desc_tags").find_elements(By. TAG_NAME, "p"):
            try: index = infos_sub_primary[1][infos_sub_primary[0].index(tag.text.split(":")[0])]
            except: continue
            info = tag.text.split(":")[1].replace(".","").replace(",",".").replace("m²","").strip()
            try: 
                if float(info) == "0": continue
            except: pass

            try:
                info = float(info)
                if info == int(info): info = int(info)
            except: pass

            infos[index].append(info)

        #Cômodos
        for tag_rooms in driver.find_elements(By. CLASS_NAME, "info__tag"):
            text_room = tag_rooms.find_elements(By. TAG_NAME, "p")[-1].text.split(" ")[-1]
            if text_room[-1] == "s": text_room = text_room[:-1]

            try: index = infos_sub_primary[1][infos_sub_primary[0].index(text_room)]
            except: continue

            info = tag_rooms.find_elements(By. TAG_NAME, "p")[-1].text.split(" ")[0]
            try:
                info = float(info)
                if info == int(info): info = int(info)
            except: pass

            infos[index].append(info)

        #Descrição:
        try: 
            text_desc = driver.find_element(By. XPATH, '//*[@id="desc_descricao"]/p[1]').text
            if text_desc != "": infos[12].append(text_desc)
        except: pass
        
        #Valor:
        try: infos[9].append(float(driver.find_element(By. ID, "info__valor").text.replace("R$ ","").replace(".","").replace(",",".")))
        except: pass

        #Adiciona None nos campos sem informações:
        for info_verify in infos:
            if len(info_verify) < links_type[0].index(link) + 1: info_verify.append("None")

        #Retira o Código do Imóvel dos anúncios da imobiliária Samuel Richard, pois estão erroneamente classificados como tal:
        if link.find("samuelrichard.com") != -1:
            infos[8][-1] = "None"
    

        #Filtra a área total correta entre os campos "Área Total" e "Área do Terreno":
        areaTotal = infos[1][-1]
        areaTerreno = infos[2][-1]
        areaCons = infos[3][-1] 

        areas = [infos[1][-1], infos[2][-1], infos[3][-1]]

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