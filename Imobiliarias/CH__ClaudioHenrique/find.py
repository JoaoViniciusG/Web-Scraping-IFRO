def findVendaCH(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    try: from Imobiliarias.CH__ClaudioHenrique.main import linksVendaCH
    except: from main import linksVendaCH

    links = linksVendaCH(service, options)

    driver = webdriver.Chrome(options=options, service=service)

    #(0) Url, (1) área total, (2) área do terreno (excluída ao final), (3) área construída, (4) dormitórios, (5) suítes, (6) banheiros, (7) vagas garagem, (8) bairro, (9) valor, (10) tipo de imóvel, (11) tipo de negócio, (12) descrição
    infos = [[],[],[],[],[],[],[],[],[],[],[],[],[]]

    infos_sub_primary = [["área total","área terreno","área construída","dormitório","suíte","banheiro","vaga","bairro"],
                         [1,2,3,4,5,6,7,8]]
    
    types_of_add = [["apartamento", "barracao", "galpao", "casa", "residencial e comercial", "sobrado", "terreno", "predio", "sala comercial", "ponto comercial"],
                   ["AP", "BA", "BA", "CA", "CA", "SO", "TE", "PR", "SA", "PT"]]
    
    script_remove_elements = 'const elements = document.getElementsByClassName("fonte_padrao imovel_cx_caracteristicas"),nums = elements.length; for (let num = 0; num < nums; num ++) {elements[0].remove()}'

    for link in links:
        driver.get(link)
        print(f"{links.index(link)+1}/{len(links)}", link)
        infos[0].append(link)

        for div_info in driver.find_elements(By.CLASS_NAME, "imodet_item1")[1:]:
            text_title = div_info.text.lower().split(":")[0]
            if text_title[-1] == "s": text_title = text_title[:-1]

            try: index = infos_sub_primary[1][infos_sub_primary[0].index(text_title)]
            except: continue

            result = div_info.text.split(":")[-1].replace(".","").replace(",",".").replace("m²","").strip()

            try: 
                result = float(result)
                if result == int(result): result = int(result)
            except: pass

            infos[index].append(result)

        #Valor:
        infos[9].append(float(driver.find_element(By.CLASS_NAME, "li_ftcor.imodet_item1val").text.replace(".","").replace(",",".").replace("R$","").strip()))

        #Tipo do Imóvel e Tipo de Negócio:
        types_text = driver.find_element(By.CLASS_NAME, "li_ftcor.blm_pesquisando_item").text.lower().split(",")[0].split(" para ")

        #TI:
        ad_type = types_text[0]

        for index_type, type_add_verify in enumerate(types_of_add[0]):
            if ad_type.find(type_add_verify) != -1: 
                infos[10].append(types_of_add[1][index_type])
                break
        else: infos[10].append("None")

        #TN:
        negc_type = types_text[-1]

        if negc_type == "venda": infos[11].append("VE")
        elif negc_type == "locação": infos[11].append("LO")
        else: infos[11].append("None")


        #Descrição:
        div_master = driver.find_element(By.XPATH, "/html/body/div[9]/div[1]")
        is_descrip = False

        for div_desc in div_master.find_elements(By.TAG_NAME, "div"):
            if div_desc.get_attribute("class") == "detimo_placas":
                if div_desc.text.lower() == "descrição":
                    is_descrip = True
                    continue
            
            elif is_descrip == True and div_desc.get_attribute("class") == "fonte_padrao":
                driver.execute_script(script=script_remove_elements)

                descrip_text = div_desc.text
                infos[12].append(descrip_text)
                break


        #Adiciona None nos campos sem informações:
        for info in infos:
            if len(info) < links.index(link) + 1: info.append("None")


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