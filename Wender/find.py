def findVendaWE(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    try: from Wender.main import linksVendaWE
    except: from main import linksVendaWE

    links = linksVendaWE(service, options)

    driver = webdriver.Chrome(options=options, service=service)

    #Área do terreno, área construída, dormitórios, banheiros, vagas garagem, bairro, código do imóvel, valor
    infos = [[],[],[],[],[],[],[],[]]

    infos_sub_primary = [["tamanho do terreno", "área construída", "quartos", "dormitórios", "banheiros", "garages", "propriedade id", "preço"],
                         [0,1,2,2,3,4,6,7]]

    for link in links:
        driver.get(link)
        print(f"{links.index(link)+1}/{len(links)}", link)

        ul_infos = driver.find_elements(By.CLASS_NAME, "list-2-col.ere-property-list")[0]

        for div_info in ul_infos.find_elements(By.TAG_NAME, "li"):
            text_title = div_info.find_elements(By.TAG_NAME, "strong")[0].text.lower()
            
            try: index = infos_sub_primary[1][infos_sub_primary[0].index(text_title)]
            except: continue

            result = div_info.find_elements(By.TAG_NAME, "span")[0].text.replace("m2","").replace(".","").replace(",",".").replace("R$","").strip()

            if text_title == "preço":
                result = result.split(" ")[0]

            if text_title != "propriedade id":
                try:
                    result = float(result)
                    if result == int(result): result = int(result)
                except: pass

            if len(infos[2]) == links.index(link) + 1 and index == 2:
                if result > infos[2][-1]: 
                    infos[index].append(result); continue
                else: continue

            if result != 0: 
                infos[index].append(result)

        #Coleta o bairro caso apareça no módulo "Endereço":
        for li_info_address in driver.find_elements(By.CLASS_NAME, "list-2-col")[0].find_elements(By.TAG_NAME, "li"):
            if li_info_address.text.lower().find("bairro:") != -1:
                infos[5].append(li_info_address.find_elements(By.TAG_NAME,"span")[0].text.strip())

        #Adiciona None nos campos sem inforação:
        for info in infos:
            if len(info) < links.index(link) + 1: info.append("None")
        
    driver.quit()
    return infos