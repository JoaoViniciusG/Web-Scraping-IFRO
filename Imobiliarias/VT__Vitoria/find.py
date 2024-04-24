def findVendaVT(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC 
    try: from Imobiliarias.VT__Vitoria.main import linksVendaVT
    except: from main import linksVendaVT
    
    links_infos = linksVendaVT(service, options)

    driver = webdriver.Chrome(options=options, service=service)

    #(0) Url, (1) área total, (2) área do terreno (excluída ao final), (3) área construída, (4) área útil (excluída ao final),(5) dormitórios, (6) suítes, (7) banheiros, (8) vagas garagem, (9) bairro, (10) valor, (11) tipo de imóvel, (12) tipo de negócio, (13) descrição
    infos = [[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

    infos_sub_primary = [["total", "terreno", "construído", "útil", "dormitório", "suíte", "banheiro", "vaga"],
                         [1,2,3,4,5,6,7,8]]
    

    for index_link, link in enumerate(links_infos[0]):
        driver.get(link)
        print(f"{links_infos[0].index(link)+1}/{len(links_infos[0])}", link)
        infos[0].append(link)
        infos[11].append(links_infos[1][index_link])
        infos[12].append(links_infos[2][index_link])

        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By. XPATH, '//*[@id="ContatoCx1"]/div[2]/div[3]/input')))

        for div_info in driver.find_elements(By.CLASS_NAME, "detimo_itensfonte"):
            for info_text in div_info.text.replace(".","").replace(",",".").replace(":","").strip().lower().split("\n"):
                if info_text == "": continue

                for text in info_text.split(" "):
                    try:
                        text = float(text)
                        if text == int(text): text = int(text)

                        info_value = text
                    except:
                        info_title = text

                if info_title[-1] == "s": info_title = info_title[:-1]
                
                index = infos_sub_primary[1][infos_sub_primary[0].index(info_title)]

                infos[index].append(info_value)

        #Bairro:
        for neigh_loop_text in driver.find_element(By.ID, "detimo_titulo").text.split(","):
            if neigh_loop_text.find("bairro ") != -1:
                neigh_text = neigh_loop_text.replace("bairro","").strip()
        
                infos[9].append(neigh_text)
                break


        #Valor:
        try:
            price_text = driver.find_element(By.CLASS_NAME, "detimo_itensfonteval.li_ftcor").text.split("R$")[-1].strip().replace(".","").replace(",",".")

            infos[10].append(float(price_text))
        except: pass


        #Descrição:
        for div_descricao in driver.find_elements(By.ID, "detimo_descricao"):
            if div_descricao.find_element(By.TAG_NAME, "span").text.upper() == "DESCRIÇÃO DO IMÓVEL":
                try:
                    desc_text = div_descricao.find_element(By.TAG_NAME, "h1").text
                except:
                    desc_text = div_descricao.find_element(By.ID, "detimo_descricao3").text

                infos[13].append(desc_text)
                break

        #Adiciona None nos campos sem informações:
        for info_verify in infos:
            if len(info_verify) < links_infos[0].index(link) + 1: info_verify.append("None")

        #Filtra a área total correta entre os campos "Área Total" e "Área do Terreno":
        areaTotal = infos[1][-1]
        areaTerreno = infos[2][-1]
        areaCons = infos[3][-1]
        areaUtil = infos[4][-1] 

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

        elif len(areas) > 1 or (len(areas) == 1 and (areas[0] == areaCons or areas[0] == areaUtil)):
            infos[3][-1] = areas[0]
    
    #Deleta o campo "Área do Terreno" e "Área Privativa" pois todas as suas informações pertinentes já foram movidas para o campo "Área Total":
    del infos[2]
    del infos[3]
    
    driver.quit()
    return infos