def findVendaRM(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    try: from ReMax.main import linksVendaRM
    except: from main import linksVendaRM

    links = linksVendaRM(service, options)

    driver = webdriver.Chrome(options=options, service=service)

    #Área total*, área do terreno, área útil, dormitórios, suítes, banheiros, vagas garagem, bairro, endereço, valor
    #*É retirado ao final da coleta, mais informações no README
    infos = [[],[],[],[],[],[],[],[],[],[]]

    infos_sub_primary = [["total m²", "tamanho do lote (m²)", "área útil", "dormitório", "banheiro", "vagas de estacionamento"],
                         [0,1,2,3,5,6]]

    for link in links:
        driver.get(link)
        print(f"{links.index(link)+1}/{len(links)}", link)

        for info_div in driver.find_elements(By.CLASS_NAME, "attributes-icons.attributes-data-col"):
            info_div_title = info_div.find_elements(By.CLASS_NAME, "data-item-label")[0].text.lower()
            if info_div_title[-1] == "s": info_div_title = info_div_title[:-1]

            try:
                index = infos_sub_primary[1][infos_sub_primary[0].index(info_div_title)]
            except: continue
        
            result = info_div.find_elements(By.CLASS_NAME, "data-item-value")[0].text.replace(".","").replace(",",".").strip()

            try:
                result = float(result)
                if result == int(result): result = int(result)
            except: pass

            infos[index].append(result)

        #Suítes:
        for suite_div in driver.find_elements(By.CLASS_NAME, "attributes-no-icons.attributes-data-col"):
            if suite_div.find_elements(By.CLASS_NAME, "data-item-label")[0].text.lower().find("suite") != -1: 
                infos[4].append(int(suite_div.find_elements(By.CLASS_NAME, "data-item-value")[0].text.strip()))

        #Endereço:
        ad_address = driver.find_elements(By.CLASS_NAME, "col-xs-12.key-address.fts-mark")[0].text.strip()
        if ad_address != "": infos[8].append(ad_address)

        #Bairro:
        for index_neigh, neigh_part in enumerate(infos[8][-1].split(",")):
            if neigh_part.lower().strip() == "vilhena": 
                try: 
                    neighborhood = infos[8][-1].split(",")[index_neigh - 1].split("-")[-1].strip()

                    if neighborhood.find("(") != -1: 
                        infos[7].append(neighborhood[neighborhood.find("(")+1 : neighborhood.find(")")])

                    else: infos[7].append(infos[8][-1].split(",")[index_neigh - 1].split("-")[-1].strip())
                except: 
                    infos[7].append(infos[8][-1].split(",")[index_neigh - 1].strip())

        #Valor:
        try:
            price_text = driver.find_element(By.XPATH, '//*[@id="LeftColumn"]/div[2]/div/div[1]/div[1]/div[3]/div/a').text
            infos[9].append(float(price_text.replace("R$","").replace(".","").replace(",",".").strip()))
        except: pass

        #Adiciona None nos campos sem informação:
        for info in infos:
            if len(info) < links.index(link) + 1: info.append("None")

        #Corrige o parâmetro "Área Total"

        #1° IF: não faz nenhuma correção nas áreas caso a área total seja igual a área útil ou a área do terreno 
        if infos[0][-1] in ("None", infos[1][-1], infos[2][-1]): continue

        #1° ELIF: não faz nenhuma correção nas áreas caso a área total seja menor que a área útil
        elif infos[2][-1] != "None" and infos[0][-1] < infos[2][-1]: continue

        #2° ELIF: iguala a área total a área do terreno caso a segunda não seja informada 
        elif infos[0][-1] != "None" and infos[1][-1] == "None": 
            infos[1][-1] = infos[0][-1]; continue

        #3° ELIF: iguala a área total a área útil caso a segunda não seja informada
        elif infos[0][-1] != "None" and infos[2][-1] == "None" and infos[0][-1] < infos[1][-1]: 
            infos[2][-1] = infos[0][-1]; continue
    
    del infos[0]
    driver.quit()
    return infos