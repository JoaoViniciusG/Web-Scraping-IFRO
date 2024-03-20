def findVendaAP(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    try: from AP__Alpha.main import linksVendaAP
    except: from main import linksVendaAP

    links = linksVendaAP(service, options)

    driver = webdriver.Chrome(options=options, service=service)

    #Área do Terreno, área privativa, dormitórios, suítes, banheiros, vagas garagem, endereço, código do imóvel, valor
    infos = [[],[],[],[],[],[],[],[],[]]

    infos_sub_primary = [["de lote", "área privativa", "demi-suites", "suíte", "lavabo", "banheiro", "vaga"],
                         [0,1,2,3,4,4,5]]
    
    for link in links:
        driver.get(link)
        print(f"{links.index(link)+1}/{len(links)}", link)

        divs_infos_ad = []

        for div_infos in driver.find_elements(By.CLASS_NAME, "block.imovel-ver-informacoes.width-100"):

            divs_infos_ad.extend(div_infos.find_elements(By.TAG_NAME, "li"))

        for div_info in divs_infos_ad:
            info_title = div_info.text.strip()[div_info.text.find(" "):].lower().replace("m²","").strip()

            try: index = infos_sub_primary[1][infos_sub_primary[0].index(info_title)]
            except: 
                try:
                    if div_info.find_elements(By.TAG_NAME, "i")[0].get_attribute("class") == "icl ic-map-marker-alt":
                        infos[6].append(div_info.text.strip())
                except: pass
                if div_info.text.find("ID:") != -1: 
                    infos[7].append(div_info.text.replace("ID:","").strip())
                continue

            info_content = float(div_info.text.strip()[:div_info.text.find(" ")].replace("m²","").replace(".","").replace(",","."))

            if len(infos[index]) == links.index(link) + 1: infos[index][-1] += info_content
            else: infos[index].append(info_content)

        #Valor:
        try: infos[8].append(float(driver.find_element(By.CLASS_NAME, "imovel-ver-preco.strong").text.replace("Valor: R$","").replace(".","").replace(",",".").strip()))
        except: pass

        #Adiciona None nos campos sem informações e converte para inteiro os valores possíveis:
        for info in infos:
            if len(info) < links.index(link) + 1: info.append("None")
            try: info[-1] = int(info[-1])
            except: pass

    driver.quit()
    return infos