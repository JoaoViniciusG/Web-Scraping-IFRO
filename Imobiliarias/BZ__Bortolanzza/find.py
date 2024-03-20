def findVendaBZ(service, options) -> list:
    from selenium.webdriver.common.by import By
    try: from main import linksVendaBZ
    except: from BZ__Bortolanzza.main import linksVendaBZ
    from selenium import webdriver

    links = linksVendaBZ(service, options)

    driver = webdriver.Chrome(options=options, service=service)

    #Área total (área construída), área do terreno, dormitórios, suítes, banheiros, vagas garagem, descrição,
    #código do imóvel, bairro, valor
    infos = [[],[],[],[],[],[],[],[],[],[]]

    infos_sub_primary = [["Área Total", "Área Terreno", "Código", "Bairro", "Dormitório", "Suíte", "Banheiro", "Vaga"], 
                         [0,1,7,8,2,3,4,5]]

    for link in links:
        driver.get(link)
        print(f"{links.index(link)+1}/{len(links)}", link)

        infos_text = driver.find_element(By. XPATH, '//*[@id="conteudo_bg1"]/table[1]/tbody/tr/td[1]/table[3]/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td').text.split("\n")

        for info in infos_text:
            infos_text_sub = info.split(":")[0]
            if infos_text_sub[-1] == "s": infos_text_sub = infos_text_sub[:-1]
            try: index = infos_sub_primary[1][infos_sub_primary[0].index(infos_text_sub)]
            except: continue

            infos[index].append(info.split(":")[-1].replace("m²","").replace(".","").replace(",",".").strip())

        #Descrição:
        try:
            if driver.find_element(By. XPATH, '//*[@id="conteudo_bg1"]/table[1]/tbody/tr/td[1]/table[6]/tbody/tr[1]').text == "Descrição":
                infos[6].append(driver.find_element(By. XPATH, '//*[@id="conteudo_bg1"]/table[1]/tbody/tr/td[1]/table[6]/tbody/tr[2]').text)
        except: pass

        #Valor:
        try: infos[9].append(float(driver.find_element(By. XPATH, '//*[@id="conteudo_bg1"]/table[1]/tbody/tr/td[1]/table[3]/tbody/tr/td[2]/table/tbody/tr[1]/td').text.replace("R$","").replace(".","").replace(",",".").strip()))
        except: pass

        #Adiciona None nos campos sem informações:
        for info_verify in infos:
            if len(info_verify) < links.index(link) + 1: info_verify.append("None")

    return infos