def findVendaDR(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    try: from Deiro.main import linksVendaDR
    except: from main import linksVendaDR

    links = linksVendaDR(service, options)

    driver = webdriver.Chrome(options=options, service=service)
    
    #Área total, área do terreno, área construída, dormitórios, suítes, banheiros, vagas garagem, descrição,
    #código do imóvel, bairro, valor
    infos = [[],[],[],[],[],[],[],[],[],[],[]]

    infos_sub_primary = [["Área Total", "Área Terreno", "Área Construída", "Código", "Bairro", "Dormitório", "Suíte", "Banheiro", "Vaga"], 
                         [0,1,2,8,9,3,4,5,6]]

    for link in links:
        driver.get(link)
        print(f"{links.index(link)+1}/{len(links)}", link)

        for div in driver.find_elements(By. CLASS_NAME, "imodet_item1")[1:]:
            try: 
                text_infos = div.text.split(":")[0]
                if text_infos[-1] == "s": text_infos = text_infos[:-1]
                index = infos_sub_primary[1][infos_sub_primary[0].index(text_infos)]
            except: continue

            infos[index].append(div.find_elements(By. TAG_NAME, "span")[0].text.replace("m²", "").replace(".","").replace(",",".").strip())

        #Descrição:
        if driver.find_element(By. XPATH, '//*[@id="conteudo_bg1"]/table[2]/tbody/tr/td[1]/div[3]/div[6]').find_elements(By. TAG_NAME, "div")[-1].text == "DESCRIÇÃO":
            try: infos[7].append(driver.find_element(By. XPATH, '//*[@id="conteudo_bg1"]/table[2]/tbody/tr/td[1]/div[3]/div[7]').text)
            except: pass

        #Valor:
        try: infos[10].append(float(driver.find_elements(By. CLASS_NAME, "li_ftcor.imodet_item1val")[0].text.replace("R$","").replace(".","").replace(",",".").strip()))
        except: pass

        #Adiciona None nos campos sem informações:
        for info_verify in infos:
            if len(info_verify) < links.index(link) + 1: info_verify.append("None")

    return infos