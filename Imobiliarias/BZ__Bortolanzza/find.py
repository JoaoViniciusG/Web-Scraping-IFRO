def findVendaBZ(service, options) -> list:
    from selenium.webdriver.common.by import By
    try: from main import linksVendaBZ
    except: from Imobiliarias.BZ__Bortolanzza.main import linksVendaBZ
    from selenium import webdriver

    links_infos = linksVendaBZ(service, options)

    driver = webdriver.Chrome(options=options, service=service)

    #(0) Url, (1) área total, (2) área construída, (3) dormitórios, (4) suítes, (5) banheiros, (6) vagas garagem, (7) bairro, (8) valor, (9) tipo de imóvel, (10) tipo de negócio, (11) descrição
    infos = [[],[],[],[],[],[],[],[],[],[],[],[]]

    infos_sub_primary = [["Área Total", "Área Terreno", "Bairro", "Dormitório", "Suíte", "Banheiro", "Vaga"], 
                         [2,1,7,3,4,5,6]]

    #Preenche o campo "Tipo do Imóvel":
    infos[9] = links_infos[1]
    
    #Preenche o campo "Tipo de Negócio":
    infos[10] = links_infos[2]

    for link in links_infos[0]:
        driver.get(link)
        print(f"{links_infos[0].index(link)+1}/{len(links_infos[0])}", link)
        infos[0].append(link)

        infos_text = driver.find_element(By. XPATH, '//*[@id="conteudo_bg1"]/table[1]/tbody/tr/td[1]/table[3]/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td').text.split("\n")

        for info in infos_text:
            infos_text_sub = info.split(":")[0]
            if infos_text_sub[-1] == "s": infos_text_sub = infos_text_sub[:-1]
            try: index = infos_sub_primary[1][infos_sub_primary[0].index(infos_text_sub)]
            except: continue

            infos[index].append(info.split(":")[-1].replace("m²","").replace(".","").replace(",",".").strip())

        #Valor:
        try: infos[8].append(float(driver.find_element(By. XPATH, '//*[@id="conteudo_bg1"]/table[1]/tbody/tr/td[1]/table[3]/tbody/tr/td[2]/table/tbody/tr[1]/td').text.replace("R$","").replace(".","").replace(",",".").strip()))
        except: pass

        #Descrição:
        try:
            if driver.find_element(By. XPATH, '//*[@id="conteudo_bg1"]/table[1]/tbody/tr/td[1]/table[6]/tbody/tr[1]').text == "Descrição":
                infos[11].append(driver.find_element(By. XPATH, '//*[@id="conteudo_bg1"]/table[1]/tbody/tr/td[1]/table[6]/tbody/tr[2]').text)
        except: pass

        #Adiciona None nos campos sem informações:
        for info_verify in infos:
            if len(info_verify) < links_infos[0].index(link) + 1: info_verify.append("None")

    driver.quit()
    return infos