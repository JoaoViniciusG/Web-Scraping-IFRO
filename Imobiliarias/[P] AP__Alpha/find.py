def findVendaAP(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from findWithCEP import findCep
    try: from AP__Alpha.main import linksVendaAP
    except: from main import linksVendaAP

    links = linksVendaAP(service, options)

    driver = webdriver.Chrome(options=options, service=service)

    #Url, área total, área construída, dormitórios, suítes, banheiros, vagas garagem, bairro, valor, descrição
    infos = [[],[],[],[],[],[],[],[],[],[]]

    infos_sub_primary = [["de lote", "área privativa", "demi-suites", "suíte", "lavabo", "banheiro", "vaga"],
                         [1,2,3,4,5,5,6]]
    
    for link in links:
        driver.get(link)
        print(f"{links.index(link)+1}/{len(links)}", link)
        infos[0].append(link)

        divs_infos_ad = []
        ad_cep = ""
        ad_address = ""

        for div_infos in driver.find_elements(By.CLASS_NAME, "block.imovel-ver-informacoes.width-100"):

            divs_infos_ad.extend(div_infos.find_elements(By.TAG_NAME, "li"))

        for div_info in divs_infos_ad:
            info_title = div_info.text.strip()[div_info.text.find(" "):].lower().replace("m²","").strip()

            try: index = infos_sub_primary[1][infos_sub_primary[0].index(info_title)]
            except: 
                try:
                    if div_info.find_elements(By.TAG_NAME, "i")[0].get_attribute("class") == "icl ic-map-marker-alt":
                        ad_address = div_info.text.strip()
                except: pass
                if div_info.text.find("CEP") != -1: 
                    ad_cep = div_info.text.replace("CEP","").replace("-","").strip()
                continue

            info_content = float(div_info.text.strip()[:div_info.text.find(" ")].replace("m²","").replace(".","").replace(",","."))

            if len(infos[index]) == links.index(link) + 1: infos[index][-1] += info_content
            else: infos[index].append(info_content)

        #Valor:
        try: infos[8].append(float(driver.find_element(By.CLASS_NAME, "imovel-ver-preco.strong").text.replace("Valor: R$","").replace(".","").replace(",",".").strip()))
        except: pass

        #Descrição:
        descrip = driver.find_element(By.CLASS_NAME, "box-editor").text
        infos[9].append(descrip)

        #Bairro por CEP:
        if ad_cep != "":
            res_cep = findCep(ad_cep)
            if res_cep[0] == True:
                infos[7].append(res_cep[1])
    
        #Bairro por endereço:
        if len(infos[7]) < links.index(link) + 1:
            infos[7].append(ad_address)

        #Adiciona None nos campos sem informações e converte para inteiro os valores possíveis:
        for info in infos:
            if len(info) < links.index(link) + 1: info.append("None")
            try: info[-1] = int(info[-1])
            except: pass

    driver.quit()
    return infos