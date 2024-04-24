def findVendaAR(service, options) -> list:
    from selenium.webdriver.common.by import By
    try: from Imobiliarias.AR__Areval.main import linksVendaAR
    except: from main import linksVendaAR
    from selenium import webdriver

    links_infos = linksVendaAR(service, options)

    driver = webdriver.Chrome(options=options, service=service)

    infos_subtitle_primary = [["gross_floor_area", "usable_floor_area", "bedrooms", "suites", "bathrooms", "garages"],
                              [1,2,3,4,5,6]]
    
    #(0) Url, (1) área total, (2) área construída, (3) dormitórios, (4) suítes, (5) banheiros, (6) vagas garagem, (7) bairro, (8) valor, (9) tipo de imóvel, (10) tipo de negócio, (11) descrição
    infos = [[],[],[],[],[],[],[],[],[],[],[],[]]

    #Preenche o campo "Tipo do Imóvel":
    infos[9] = links_infos[1]
    
    #Preenche o campo "Tipo de Negócio":
    infos[10] = links_infos[2]

    for link in links_infos[0]:
        driver.get(link)
        print(f"{links_infos[0].index(link)+1}/{len(links_infos[0])}", link)
        infos[0].append(link)

        infos_primary = driver.find_elements(By. CLASS_NAME, "item-info.digital")

        for info_primary in infos_primary:
            info_primary_type = info_primary.get_attribute("class").split(" ")[-1]

            try:
                index = infos_subtitle_primary[1][infos_subtitle_primary[0].index(info_primary_type)]
            except: continue

            infos_res = float(info_primary.find_element(By.TAG_NAME, "span").text.strip().split(" ")[0])

            if infos_res == int(infos_res): infos_res = int(infos_res)

            infos[index].append(infos_res)

        #Descrição:
        try: infos[11].append(driver.find_element(By. CLASS_NAME, "box-description").text)
        except: pass

        #Bairro:
        neighborhood_local_divs = driver.find_elements(By. CLASS_NAME, "hidden-mobile")[0].find_elements(By. TAG_NAME, "li")
        for i in range(1, len(neighborhood_local_divs) + 1):
            try: 
                infos[7].append(neighborhood_local_divs[-i].find_elements(By. TAG_NAME, "a")[0].get_attribute("text"))
                break   
            except: pass

        #Valor:    
        try:
            sale_price = driver.find_element(By.CLASS_NAME, "sale-price")
            infos[8].append(float(sale_price.text.split(" ")[-1].replace(".","").replace(",",".")))
        except:
            try:
                for sale_price in driver.find_elements(By.CLASS_NAME, "price"):
                    if sale_price.text == "": continue
                    infos[8].append(float(sale_price.text.replace("/ano", "").replace("/mês", "").split(" ")[-1].replace(".","").replace(",",".")))
                    break
            except: pass
        
        #Adiciona None nos campos sem informações
        for info_verify in infos:
            if len(info_verify) < links_infos[0].index(link) + 1: info_verify.append("None")

    driver.quit()
    return infos