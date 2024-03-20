def findVendaCH(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    try: from CH__ClaudioHenrique.main import linksVendaCH
    except: from main import linksVendaCH

    links = linksVendaCH(service, options)

    driver = webdriver.Chrome(options=options, service=service)

    #Área total, área do terreno, área construída, dormitórios, suítes, banheiros, vagas garagem, bairro, código do imóvel, valor
    infos = [[],[],[],[],[],[],[],[],[],[]]

    infos_sub_primary = [["área total","área terreno","área construída","dormitório","suíte","banheiro","vaga","bairro","código"],
                         [0,1,2,3,4,5,6,7,8]]
    
    for link in links:
        driver.get(link)
        print(f"{links.index(link)+1}/{len(links)}", link)

        for div_info in driver.find_elements(By.CLASS_NAME, "imodet_item1")[1:]:
            text_title = div_info.text.lower().split(":")[0]
            if text_title[-1] == "s": text_title = text_title[:-1]

            try: index = infos_sub_primary[1][infos_sub_primary[0].index(text_title)]
            except: continue

            result = div_info.text.split(":")[-1].replace(".","").replace(",",".").replace("m²","").strip()

            try: 
                result = float(result)
                if result == int(result): result = int(result)
            except: pass

            infos[index].append(result)

        #Valor:
        infos[9].append(float(driver.find_element(By.XPATH, "/html/body/div[9]/div[1]/div[2]/div[2]/div[2]").text.replace(".","").replace(",",".").replace("R$","").strip()))

        #Adiciona None nos campos sem informações:
        for info in infos:
            if len(info) < links.index(link) + 1: info.append("None")

    driver.quit()
    return links