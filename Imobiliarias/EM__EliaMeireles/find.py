def findVendaEM(service, options) -> list:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    try: from EM__EliaMeireles.main import linksVendaEM
    except: from main import linksVendaEM

    links = linksVendaEM(service, options)

    driver = webdriver.Chrome(options=options, service=service)

    #Área total, área do terreno, área construída, dormitórios, suítes, banheiros, vagas garagem, código do imóvel, bairro, valor
    infos = [[],[],[],[],[],[],[],[],[],[]]
    
    infos_sub_primary = [["área total", "terreno", "construção", "ref.", "quarto", "suíte", "banheiro", "vaga"],
                         [0,1,2,7,3,4,5,6]]
    
    for link in links:
        driver.get(link)
        print(f"{links.index(link)+1}/{len(links)}", link)

        for li_info in driver.find_elements(By.CLASS_NAME, "listpanel-content")[0].find_elements(By.TAG_NAME, "li"):
            try: index = infos_sub_primary[1][infos_sub_primary[0].index(li_info.text.lower().split(":")[0])]
            except: pass

            result = li_info.text.lower().split(":")[-1].replace("m²","").strip()

            if li_info.text.lower().find("ref.") == -1:
                try:
                    result = float(result)
                    if result == int(result): result = int(result)
                    if result == 0: continue
                except: continue

            infos[index].append(result)
        
        for div_info in driver.find_elements(By.CLASS_NAME, "listpanel-head")[0].find_elements(By.TAG_NAME, "div"):
            try: index = infos_sub_primary[1][infos_sub_primary[0].index(div_info.text.lower().replace("(s)", "").strip().split(" ")[-1])]
            except: continue

            try: result = int(div_info.text.lower().split(" ")[0].strip())
            except: continue

            if result < 0: result = -result
            infos[index].append(result)

        #Bairro:
        text_neighborhood = driver.find_element(By.XPATH, '//*[@id="pageWrapper"]/div/div[1]/div/main/section[2]/header/div[1]/h1').text.lower()
        if text_neighborhood[text_neighborhood.find(" no ")+4:].replace("vilhena","").replace("venda","").replace("- ro", "").strip() != "":
            print(text_neighborhood[text_neighborhood.find(" no "):].replace("vilhena","").replace("venda","").replace("- ro","").strip())
            infos[8].append(text_neighborhood[text_neighborhood.find(" no ")+4:].replace("venda","").strip())
        
        #Valor: 
        try:
            text_price = float(driver.find_element(By.XPATH, '//*[@id="Detail"]/div[2]/h2').text.replace("R$","").replace(".","").replace(",",".").strip())
            if text_price > 100000000: raise
            infos[9].append(text_price)
        except: pass

        #Adiciona None nos campos sem informação:
        for info in infos:
            if len(info) < links.index(link) + 1: info.append("None")

    driver.quit()
    return infos