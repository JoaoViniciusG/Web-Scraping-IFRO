def findVendaDC(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    try: from DC__DonadoniCorretor.main import linksVendaDC
    except: from main import linksVendaDC

    links = linksVendaDC(service, options)

    driver = webdriver.Chrome(options=options, service=service)

    #Área total, área do terreno, área construída, área útil, dormitórios, suítes, banheiros, vagas garagem, código do imóvel, bairro,
    #endereço, valor 
    infos = [[],[],[],[],[],[],[],[],[],[],[],[]]
    
    infos_sub_primary = [["área total", "área terreno", "área construída", "área útil", "dormitório", "suíte", "banheiro", "vaga", "código", "bairro", "endereço"],
                         [0,1,2,3,4,5,6,7,8,9,10]]
    
    for link in links:
        driver.get(link)
        print(f"{links.index(link)+1}/{len(links)}", link)

        for tr_info in driver.find_element(By.ID, "tb_features1").find_elements(By.TAG_NAME, "tr"):
            info_title = tr_info.text.lower().split(":")[0]
            try: 
                if info_title[-1] == "s": info_title = info_title[:-1]
            except: continue

            try: index = infos_sub_primary[1][infos_sub_primary[0].index(info_title)]
            except: continue
            
            info_result = tr_info.text.split(":")[-1].replace("m²","").replace(".","").replace(",",".").strip()

            if info_title != "código":
                try: 
                    info_result = float(info_result)
                    if info_result == int(info_result): info_result = int(info_result)
                except: pass
            
            infos[index].append(info_result)

        #Valor: 
        try: 
            text_price = driver.find_elements(By.CLASS_NAME, "grid-3.valores")[0].text 
            infos[11].append(float(text_price.replace("R$","").replace(".","").replace(",",".").strip()))
        except: pass

        #Adiciona None nos campos sem informação:
        for info in infos:
            if len(info) < links.index(link) + 1: info.append("None")

    driver.quit()
    return infos