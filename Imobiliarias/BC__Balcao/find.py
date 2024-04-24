def findVendaBC(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    try: from main import linksVendaBC
    except: from Imobiliarias.BC__Balcao.main import linksVendaBC

    links_infos = linksVendaBC(service, options)
    
    driver = webdriver.Chrome(service=service, options=options)

    #(0) Url, (1) área total, (2) área do terreno (excluída ao final), (3) área construída, (4) área útil (excluída ao final), (5) dormitórios, (6) suítes, (7) banheiros, (8) vagas garagem, (9) bairro, (10) valor, (11) tipo de imóvel, (12) tipo de negócio, (13) descrição
    infos = [[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

    infos_sub_primary = [["dormitório", "suíte", "banheiro", "garage"],
                         [5,6,7,8]]
    
    areas_sub = [["Terreno Área Total", "Área Total", "Área Construída", "Área Privativa"],
                 [1,2,3,4]]
    
    for index_link, link in enumerate(links_infos[0]):
        driver.get(link)
        print(f"{links_infos[0].index(link)+1}/{len(links_infos[0])}", link)
        infos[0].append(link)
        infos[11].append(links_infos[1][index_link])
        infos[12].append(links_infos[2][index_link])

        divs_list = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div/div[1]/div[4]/div[2]').find_elements(By.TAG_NAME, "section")[-1].find_elements(By.TAG_NAME, "div")

        #Áreas
        for div in divs_list:
            div_type = div.find_elements(By.TAG_NAME, "span")[0].text

            try: 
                index = areas_sub[1][areas_sub[0].index(div_type)]
            except:
                continue

            infos[index].append(float(div.find_elements(By.TAG_NAME, "span")[1].text.replace(".","").replace(",",".").replace("m²","")))

        #---------------------------------
            
        for section_info in driver.find_elements(By.CLASS_NAME, "sc-1gfn7xh-0.fxLMbR"):
            section_title = section_info.find_element(By.TAG_NAME, "h3").text.lower()

            #Cômodos
            if section_title == "cômodos":
                try:
                    for span in driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div/div[1]/div[4]/div[1]/section[1]/div').find_elements(By.TAG_NAME, "span"):
                        for span_text in span.text.split(","):
                            span_text = span_text.lower().replace("sendo","").strip()

                            for index_sub, info_sub in enumerate(infos_sub_primary[0]):
                                if span_text.find(info_sub) > 0: index = infos_sub_primary[1][index_sub]
                                else: continue

                                res = span_text.split(" ")[0]

                                try:
                                    res = float(res)
                                    if res == int(res): res = int(res)
                                except: pass

                                infos[index].append(res)
                                break
                except: pass

            #Descrição
            if section_title == "descrição do imóvel":
                descrip = section_info.find_element(By.TAG_NAME, "span").text

                infos[13].append(descrip)       

        #Bairro:
        neighborhood = driver.find_elements(By.CLASS_NAME, "sc-sbjl5d-0.ceyUbb")[0].text.split(" - ")

        for index, str_neigh in enumerate(neighborhood):
            if str_neigh.find("Vilhena/RO") == -1: continue

            infos[9].append(neighborhood[index - 1].strip())
            break
        
        #Valor:
        try:
            script_price_lo = 'return document.getElementsByClassName("sc-3hj0n0-0 hRQHtW")[1].textContent'
            script_price_ve = 'return document.getElementsByClassName("sc-3hj0n0-0 hGsMGq")[1].textContent'
            
            if links_infos[2][index_link] == "LO":
                price_sale = driver.execute_script(script_price_lo)
            elif links_infos[2][index_link] == "VE":
                price_sale = driver.execute_script(script_price_ve)

            infos[10].append(float(price_sale.replace(".","").replace(",",".").replace("R$","")))
        except: pass

        #Adiciona None nos campos sem informações:
        for info in infos:
            if len(info) < links_infos[0].index(link) + 1: info.append("None")

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